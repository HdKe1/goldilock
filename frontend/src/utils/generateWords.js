// utils/generateWords.js
import { WORD_LIST } from "./wordList";

export function generateRandomWords(count) {
  const result = [];
  for (let i = 0; i < count; i++) {
    const randomIndex = Math.floor(Math.random() * WORD_LIST.length);
    result.push(WORD_LIST[randomIndex]);
  }
  return result;
}
