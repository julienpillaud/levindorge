import { colorStockQuantities, searchTable, setCursor } from "./utils.js";
import {
  initCreateInventoryListener,
  initCreateItemListener,
  initDeleteItemsListener,
  initResetStocksListener,
  initSelectShopListener,
} from "./listener.js";
import { initToggleDeleteButton } from "./listener/global.js";
import { initDeletePriceLabels } from "./listener/price_labels.js";

document.addEventListener("DOMContentLoaded", () => {
  // ---------------------------------------------------------------------------
  // Search
  const searchInputs = document.querySelectorAll(
    "#search-mobile, #search-desktop",
  );
  searchInputs.forEach((input) => {
    input.addEventListener("keyup", (event) => {
      searchTable(event.target.value);
    });
  });

  // Set cursor at the end of the search input on page load
  window.addEventListener("load", setCursor);

  // Clear search
  const clearSearchButtons = document.querySelectorAll(
    "#clear-search-mobile, #clear-search-desktop",
  );
  clearSearchButtons.forEach((button) => {
    button.addEventListener("click", () => {
      searchInputs.forEach((input) => {
        input.value = "";
      });
      searchTable("");
    });
  });
  // ---------------------------------------------------------------------------
  initSelectShopListener();
  colorStockQuantities();

  initCreateItemListener();
  initDeleteItemsListener();
  initCreateInventoryListener();
  initResetStocksListener();

  initToggleDeleteButton();
  initDeletePriceLabels();
  // ---------------------------------------------------------------------------
});
