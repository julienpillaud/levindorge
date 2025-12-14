import {
  initializeCheckboxes,
  updateCheckedArticleIds,
  updateDropdownVisibility,
} from "./checkboxes.js";
import {
  initializePriceTagsDropdown,
  showSelectedArticles,
  unselectArticles,
} from "./price-labels.js";
import { buildCreateDropdownMenu } from "./menu.js";
import { initArticles } from "./articles/init.js";
import { initSearch } from "./search.js";

document.addEventListener("DOMContentLoaded", () => {
  initSearch();
  initArticles();
  buildCreateDropdownMenu();

  // ---------------------------------------------------------------------------
  // Articles table checkboxes
  initializeCheckboxes();

  document.addEventListener("change", (event) => {
    if (event.target.matches("table tbody .checkbox")) {
      updateCheckedArticleIds(event);
      updateDropdownVisibility();
    }
  });
  // ---------------------------------------------------------------------------
  const priceTagsSelected = document.getElementById("price-labels-selected");
  priceTagsSelected.addEventListener("click", () => {
    showSelectedArticles();
  });

  const priceTagsUnselct = document.getElementById("price-labels-unselect");
  priceTagsUnselct.addEventListener("click", () => {
    unselectArticles();
  });

  initializePriceTagsDropdown();
});
