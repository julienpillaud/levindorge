const CACHE_DURATION = 1000 * 60 * 60;

export const getCachedData = (key, duration = CACHE_DURATION) => {
  const item = localStorage.getItem(key);
  if (!item) {
    return null;
  }

  const { data, timestamp } = JSON.parse(item);
  const now = Date.now();

  if (now - timestamp < duration) {
    return data;
  }
  return null;
};

export const setCachedData = (key, data) => {
  const item = {
    data,
    timestamp: Date.now(),
  };
  localStorage.setItem(key, JSON.stringify(item));
};
