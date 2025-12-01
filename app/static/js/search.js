// -----------------------------------------------------------------------------
export function initSearch() {
  const searchInputs = document.querySelectorAll(
    "#search-mobile, #search-desktop",
  );
  let searchTimer;
  setupSearch(searchInputs, searchTimer);
  setupClearSearch(searchInputs, searchTimer);
}

// -----------------------------------------------------------------------------
// Add event listeners to the search inputs
function setupSearch(inputs, timer) {
  inputs.forEach((input) => {
    input.addEventListener("keyup", (event) => {
      performSearch(event.target.value, timer);
    });
  });
}

// -----------------------------------------------------------------------------
// Add event listeners to the clear search buttons
function setupClearSearch(inputs, timer) {
  const clearButtons = document.querySelectorAll(
    "#clear-search-mobile, #clear-search-desktop"
  );

  clearButtons.forEach((button) => {
    button.addEventListener("click", () => {
      inputs.forEach(input => input.value = "");
      performSearch("", timer);
    });
  });
}

// -----------------------------------------------------------------------------
function performSearch(query, timer) {
  clearTimeout(timer);

  timer = setTimeout(() => {
    const url = buildSearchUrl(query);
    updatePage(url);
  }, 300);
}

// -----------------------------------------------------------------------------
function buildSearchUrl(query) {
  const trimmed = query.trim();
  if (!trimmed) return "/articles";
  return `/articles?search=${encodeURIComponent(trimmed)}`;
}

// -----------------------------------------------------------------------------
async function updatePage(url) {
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
function updateElement(selector, newDoc) {
  const newElement = newDoc.querySelector(selector);
  const currentElement = document.querySelector(selector);

  if (newElement && currentElement) {
    currentElement.innerHTML = newElement.innerHTML;
  }
}
