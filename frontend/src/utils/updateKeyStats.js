export function updateKeyStats(prevStats, expectedChar, typedChar) {
    if (!expectedChar) return prevStats;
  
    const current = prevStats[expectedChar] || {
      totalTyped: 0,
      correctTyped: 0,
    };
  
    return {
      ...prevStats,
      [expectedChar]: {
        totalTyped: current.totalTyped + 1,
        correctTyped: current.correctTyped + (typedChar === expectedChar ? 1 : 0),
      },
    };
  }
  