import {updateArticlesPage} from "./utils.js";

let searchTimer = null;

// -----------------------------------------------------------------------------
export const initSearch = () => {
  const searchInputs = document.querySelectorAll(
    "#search-mobile, #search-desktop",
  );
  setupSearch(searchInputs);
  setupClearSearch(searchInputs);
};

// -----------------------------------------------------------------------------
// Add event listeners to the search inputs
const setupSearch = (inputs) => {
  inputs.forEach((input) => {
    input.addEventListener("keyup", (event) => {
      performSearch(event.target.value);
    });
  });
};

// -----------------------------------------------------------------------------
// Add event listeners to the clear search buttons
const setupClearSearch = (inputs) => {
  const clearButtons = document.querySelectorAll(
    "#clear-search-mobile, #clear-search-desktop",
  );

  clearButtons.forEach((button) => {
    button.addEventListener("click", () => {
      inputs.forEach((input) => {
        input.value = "";
      });
      performSearch("");
    });
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
