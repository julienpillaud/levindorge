import {buildCreateDropdownMenu} from "./menu.js";
import {initArticles} from "./articles/init.js";
import {initSearch} from "./search.js";
import {initializeCheckboxes, updateCheckedArticleIds, updateDropdownVisibility} from "./checkboxes.js";
import {showSelectedArticles, initializePriceTagsDropdown} from "./price-labels.js";

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
  const priceTagsSelected = document.getElementById("price-labels-selected")
  priceTagsSelected.addEventListener("click", () => {
    showSelectedArticles();
  });

  initializePriceTagsDropdown();
});
