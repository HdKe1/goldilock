import React from "react";

const KEY_ROWS = [
  ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
  ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
  ["z", "x", "c", "v", "b", "n", "m"],
  [" "], // space key
];

const getColorClass = (accuracy) => {
  if (accuracy === null) return "bg-gray-300 text-black"; // not typed
  if (accuracy > 90) return "bg-green-500 text-white";
  if (accuracy > 70) return "bg-yellow-400 text-black";
  if (accuracy > 50) return "bg-orange-400 text-white";
  return "bg-red-500 text-white";
};

const Keyboard = ({ keyStats = {} }) => {
  return (
    <div className="mt-8 flex flex-col items-center gap-2">
      {KEY_ROWS.map((row, rowIndex) => (
        <div key={rowIndex} className="flex gap-1">
          {row.map((key) => {
            const stats = keyStats[key] || null;
            const accuracy = stats
              ? (stats.correctTyped / stats.totalTyped) * 100
              : null;
            const colorClass = getColorClass(accuracy);

            const displayKey = key === " " ? "[space]" : key;

            return (
              <div
                key={key}
                className={`w-10 h-12 flex items-center justify-center rounded ${colorClass} font-semibold text-sm`}
              >
                {displayKey}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default Keyboard;
