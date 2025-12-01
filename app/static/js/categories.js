import { getCachedData, setCachedData } from "./localStorage.js";

const CACHE_KEY = "categories";

export const getCategories = async () => {
  const cached = getCachedData(CACHE_KEY);
  if (cached) {
    return cached;
  }

  const fresh = await fetchCategories();
  setCachedData(CACHE_KEY, fresh);
  return fresh;
};

const fetchCategories = async () => {
  const result = await fetch("/categories");
  const categories = await result.json();

  return Object.fromEntries(
    categories.map((category) => [category.name, category]),
  );
};
