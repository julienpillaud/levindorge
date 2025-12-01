import {getCachedData, setCachedData} from "./localStorage.js";

const CACHE_KEY = "stores";

export async function getStores() {
  const cached = getCachedData(CACHE_KEY);
  if (cached) {
    return cached;
  }

  const fresh = await fetchStores();
  setCachedData(CACHE_KEY, fresh);
  return fresh;
}

async function fetchStores() {
  const result = await fetch('/stores');
  const stores = await result.json();

  return Object.fromEntries(
    stores.map(store => [store.slug, store])
  );
}
