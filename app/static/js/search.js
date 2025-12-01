let searchTimer = null;

// -----------------------------------------------------------------------------
export const initSearch = () => {
  const searchInputs = document.querySelectorAll(
    "#search-mobile, #search-desktop",
  );
  setupSearch(searchInputs);
  setupClearSearch(searchInputs);
}

// -----------------------------------------------------------------------------
// Add event listeners to the search inputs
const setupSearch = (inputs) => {
  inputs.forEach((input) => {
    input.addEventListener("keyup", (event) => {
      performSearch(event.target.value);
    });
  });
}

// -----------------------------------------------------------------------------
// Add event listeners to the clear search buttons
const setupClearSearch = (inputs) => {
  const clearButtons = document.querySelectorAll(
    "#clear-search-mobile, #clear-search-desktop"
  );

  clearButtons.forEach((button) => {
    button.addEventListener("click", () => {
      inputs.forEach((input) => {
        input.value = ""
      });
      performSearch("");
    });
  });
}

// -----------------------------------------------------------------------------
const performSearch = (query) => {
  clearTimeout(searchTimer);

  searchTimer = setTimeout(() => {
    const url = buildSearchUrl(query);
    updatePage(url);
  }, 300);
}

// -----------------------------------------------------------------------------
const buildSearchUrl = (query) => {
  const trimmed = query.trim();
  if (!trimmed) {
    return "/articles";
  }
  return `/articles?search=${encodeURIComponent(trimmed)}`;
}

// -----------------------------------------------------------------------------
const updatePage = async (url) => {
  const res = await fetch(url);
  const html = await res.text();
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');

  updateElement('#articles-table', doc);
  updateElement('#items-count', doc);
  updateElement('#pagination', doc);

  history.pushState(null, '', url);
}

// -----------------------------------------------------------------------------
const updateElement = (selector, newDoc) => {
  const newElement = newDoc.querySelector(selector);
  const currentElement = document.querySelector(selector);

  if (newElement && currentElement) {
    currentElement.innerHTML = newElement.innerHTML;
  }
}
