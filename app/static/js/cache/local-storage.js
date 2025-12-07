const CACHE_DURATION = 1000 * 60 * 60;

export const fetchWithCache = async (
  key,
  fetcher,
  duration = CACHE_DURATION,
) => {
  const item = localStorage.getItem(key);

  if (item) {
    const { data, timestamp } = JSON.parse(item);
    const now = Date.now();
    if (now - timestamp < duration) {
      return data;
    }
  }

  const data = await fetcher();
  setCachedData(key, data);
  return data;
};

export const setCachedData = (key, data) => {
  const item = { data, timestamp: Date.now() };
  localStorage.setItem(key, JSON.stringify(item));
};
