import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Keyboard from "../components/Keyboard";

const ResultScreen = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const wpm = location.state?.wpm;
  const keyStats = location.state?.keyStats || {};
  const avgWpm = location.state?.avgWpm;
  const totalAttempts = location.state?.totalAttempts;
  const saveSuccess = location.state?.saveSuccess;
  const saveError = location.state?.saveError;
  const errorMessage = location.state?.errorMessage;

  const handleTryAgain = () => {
    navigate("/");
  };

  const renderKeyStats = () => {
    const entries = Object.entries(keyStats);
    if (entries.length === 0) return <p>No key stats available.</p>;

    return (
      <div className="mt-6 text-sm text-left w-full">
        <h2 className="text-lg font-semibold mb-2">Character Accuracy</h2>
        <div className="grid grid-cols-4 gap-2 max-h-64 overflow-y-auto">
          {entries.map(([char, stats]) => {
            const { totalTyped, correctTyped } = stats;
            const accuracy = ((correctTyped / totalTyped) * 100).toFixed(1);
            return (
              <div
                key={char}
                className="bg-gray-100 p-2 rounded shadow text-center"
              >
                <strong>{char === " " ? "[space]" : char}</strong>
                <div>{accuracy}%</div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderWpmStats = () => {
    return (
      <div className="mb-6 space-y-4">
        {/* Current Test WPM */}
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-800 mb-2">Current Test</h3>
          <p className="text-2xl font-bold text-blue-600">
            {wpm !== undefined ? `${wpm} WPM` : "No data"}
          </p>
        </div>

        {/* Statistics from Backend */}
        {saveSuccess && (
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-green-50 p-4 rounded-lg text-center">
              <h4 className="text-sm font-semibold text-green-800 mb-1">Average WPM</h4>
              <p className="text-xl font-bold text-green-600">
                {avgWpm !== undefined ? `${avgWpm}` : "N/A"}
              </p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg text-center">
              <h4 className="text-sm font-semibold text-purple-800 mb-1">Total Tests</h4>
              <p className="text-xl font-bold text-purple-600">
                {totalAttempts !== undefined ? totalAttempts : "N/A"}
              </p>
            </div>
          </div>
        )}

        {/* Error Message */}
        {saveError && (
          <div className="bg-red-50 p-4 rounded-lg">
            <h4 className="text-sm font-semibold text-red-800 mb-1">Note</h4>
            <p className="text-sm text-red-600">
              Results not saved: {errorMessage || "Connection error"}
            </p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black-100 p-4">
      <div className="bg-white shadow-lg rounded-2xl p-8 text-center max-w-md w-full">
        <h1 className="text-3xl font-bold mb-4 text-black-600">
          Your Result. Well done
        </h1>
        
        {renderWpmStats()}

        {renderKeyStats()}

        <button
          onClick={handleTryAgain}
          className="mt-6 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition duration-200"
        >
          Try Again
        </button>
      </div>

      <Keyboard keyStats={keyStats} />
    </div>
  );
};

export default ResultScreen;