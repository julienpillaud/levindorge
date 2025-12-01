import {getCachedData, setCachedData} from "./localStorage.js";

const CACHE_KEY = "categories";

export async function getCategories() {
  const cached = getCachedData(CACHE_KEY);
  if (cached) {
    return cached;
  }

  const fresh = await fetchCategories();
  setCachedData(CACHE_KEY, fresh);
  return fresh;
}

async function fetchCategories() {
  const result = await fetch('/categories');
  const categories = await result.json();

  return Object.fromEntries(
    categories.map(category => [category.name, category])
  );
}
