import { fetchWithCache } from "./local-storage.js";

const CACHE_KEY = "stores";

export const getStores = async () =>
  await fetchWithCache(CACHE_KEY, fetchCategoryGroups);

const fetchCategoryGroups = async () => {
  const result = await fetch("/stores");
  return await result.json();
};
