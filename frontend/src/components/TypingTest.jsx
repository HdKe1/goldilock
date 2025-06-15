import React, { useEffect, useState } from "react";
import { generateRandomWords } from "../utils/generateWords";
import { useNavigate } from "react-router-dom";
import { updateKeyStats } from "../utils/updateKeyStats";
import { saveWPMAttempt } from "../api"; // Import your API function - adjust path as needed

const TypingTest = () => {
  const [words, setWords] = useState([]);
  const [input, setInput] = useState("");
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [typedWords, setTypedWords] = useState([]);
  const [startTime, setStartTime] = useState(null);
  const [correctCharCount, setCorrectCharCount] = useState(0);
  const [hasStarted, setHasStarted] = useState(false);
  const [keyStats, setKeyStats] = useState({});

  const navigate = useNavigate();

  const initializeTest = () => {
    setWords(generateRandomWords(50));
    setInput("");
    setCurrentWordIndex(0);
    setTypedWords([]);
    setStartTime(null);
    setCorrectCharCount(0);
    setHasStarted(false);
    setKeyStats({});
  };

  useEffect(() => {
    initializeTest();
  }, []);

  const handleStart = () => {
    setHasStarted(true);
    setStartTime(Date.now());
  };

  useEffect(() => {
    const handleKeyDown = async (e) => { // Made this async
      if (!hasStarted) return;
      
      if (e.key === " ") {
        e.preventDefault();
        const trimmed = input.trim();
        const currentWord = words[currentWordIndex];
        const isCorrect = trimmed === currentWord;

        let correctChars = 0;

        for (let i = 0; i < trimmed.length; i++) {
          const expectedChar = currentWord[i];
          const typedChar = trimmed[i];

          if (typedChar === expectedChar) correctChars++;

          setKeyStats((prev) =>
            updateKeyStats(prev, expectedChar, typedChar)
          );
        }

        setCorrectCharCount((prev) => prev + correctChars);
        setTypedWords((prev) => [...prev, isCorrect]);

        const nextIndex = currentWordIndex + 1;
        setCurrentWordIndex(nextIndex);
        setInput("");

        if (nextIndex === words.length) {
          const endTime = Date.now();
          const timeInMinutes = (endTime - startTime) / 1000 / 60;
          const totalWordsTyped = (correctCharCount + correctChars) / 5;
          const finalWPM = Math.round(totalWordsTyped / timeInMinutes);

          try {
            // Save WPM to backend
            const response = await saveWPMAttempt(finalWPM);
            console.log('WPM saved successfully:', response);

            // Navigate to results with additional stats data
            navigate("/results", {
              state: { 
                wpm: finalWPM, 
                keyStats,
                avgWpm: response.data.avg_wpm,
                totalAttempts: response.data.total_attempts,
                saveSuccess: true
              },
            });
          } catch (error) {
            // Handle error - still navigate but show error
            console.error('Failed to save WPM:', error);
            
            navigate("/results", {
              state: { 
                wpm: finalWPM, 
                keyStats,
                saveError: true,
                errorMessage: error.message
              },
            });
          }
        }
      } else if (e.key.length === 1) {
        setInput((prev) => prev + e.key);
      } else if (e.key === "Backspace") {
        setInput((prev) => prev.slice(0, -1));
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [input, hasStarted, currentWordIndex, correctCharCount, words, startTime, navigate, keyStats]);

  const renderWord = (word, index) => {
    const isActive = index === currentWordIndex;
    const hasBeenTyped = index < currentWordIndex;
    const wasCorrect = typedWords[index];

    let wordClass = "";

    if (hasBeenTyped) {
      wordClass = wasCorrect
        ? "text-green-700"
        : "text-red-700";
    } else if (isActive) {
      wordClass = "text-white-700";
    }

    return (
      <span key={index} className={`px-1 rounded ${wordClass}`}>
        {isActive
          ? word.split("").map((char, i) => {
              let colorClass = "";
              if (i < input.length) {
                colorClass = input[i] === char ? "text-green-600" : "text-red-500";
              } else {
                colorClass = "text-gray-400";
              }

              return (
                <span key={i} className={colorClass}>
                  {char}
                </span>
              );
            })
          : word}
      </span>
    );
  };

  return (
    <div className="min-h-screen flex flex-col items-top justify-top px-4 py-8">
      {!hasStarted && (
        <div className="flex flex-col items-center gap-4">
          <button
            onClick={handleStart}
            className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded text-lg font-semibold"
          >
            Start Test
          </button>
        </div>
      )}

      {hasStarted && (
        <>
          <div className="flex flex-col items-center gap-6 w-full">
            <div className="flex flex-wrap gap-2 text-xl font-mono text-gray-800 max-w-4xl justify-center">
              {words.map((word, index) => renderWord(word, index))}
            </div>

            <button
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded font-semibold"
              onClick={initializeTest}
            >
              Restart Test
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default TypingTest;