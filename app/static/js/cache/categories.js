import { fetchWithCache } from "./local-storage.js";

const CACHE_KEY = "categories";

export const getCategories = async () => {
  const categories = await fetchWithCache(CACHE_KEY, fetchCategories);
  return Object.fromEntries(
    categories.map((category) => [category.name, category]),
  );
};

const fetchCategories = async () => {
  const result = await fetch("/categories");
  return await result.json();
};
