import {fetchWithCache} from "./local-storage.js";

const CACHE_KEY = "category-groups";

export const getCategoryGroups = async () => {
  return await fetchWithCache(CACHE_KEY, fetchCategoryGroups);
};

const fetchCategoryGroups = async () => {
  const result = await fetch("/categories/groups");
  return await result.json();
};
