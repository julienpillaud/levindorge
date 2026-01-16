import { updateArticlesPage } from "./utils.js";

let searchTimer = null;

// -----------------------------------------------------------------------------
export const initSearch = () => {
  const searchInput = document.getElementById("search");
  const clearSearchButton = document.getElementById("clear-search");
  if (!searchInput || !clearSearchButton) {
    return;
  }

  searchInput.addEventListener("input", (event) => {
    performSearch(event.target.value);
  });

  clearSearchButton.addEventListener("click", () => {
    searchInput.value = "";
    performSearch("");
  });
};

// -----------------------------------------------------------------------------
const performSearch = (query) => {
  clearTimeout(searchTimer);

  searchTimer = setTimeout(() => {
    const url = buildSearchUrl(query);
    updateArticlesPage(url);
  }, 300);
};

// -----------------------------------------------------------------------------
const buildSearchUrl = (query) => {
  const trimmed = query.trim();
  if (!trimmed) {
    return "/articles";
  }
  return `/articles?search=${encodeURIComponent(trimmed)}`;
};
