import { getCachedData, setCachedData } from "./localStorage.js";

const CACHE_KEY = "stores";

export const getStores = async () => {
  const cached = getCachedData(CACHE_KEY);
  if (cached) {
    return cached;
  }

  const fresh = await fetchStores();
  setCachedData(CACHE_KEY, fresh);
  return fresh;
};

const fetchStores = async () => {
  const result = await fetch("/stores");
  const stores = await result.json();

  return Object.fromEntries(stores.map((store) => [store.slug, store]));
};
