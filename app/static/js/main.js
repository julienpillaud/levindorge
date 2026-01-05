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
import { initInventoriesTable } from "./inventories.js";
import { createItem, deleteItems, initItemsManager } from "./items.js";

document.addEventListener("DOMContentLoaded", () => {
  initSearch();
  initArticles();
  buildCreateDropdownMenu();

  // ---------------------------------------------------------------------------
  // Articles table checkboxes
  initializeCheckboxes();

  document.addEventListener("change", (event) => {
    if (event.target.matches("#articles-table tbody .checkbox")) {
      updateCheckedArticleIds(event);
      updateDropdownVisibility();
    }
  });
  // ---------------------------------------------------------------------------
  // Price labels
  const priceTagsSelected = document.getElementById("price-labels-selected");
  if (priceTagsSelected) {
    priceTagsSelected.addEventListener("click", () => {
      showSelectedArticles();
    });
  }

  const priceTagsUnselect = document.getElementById("price-labels-unselect");
  if (priceTagsUnselect) {
    priceTagsUnselect.addEventListener("click", () => {
      unselectArticles();
    });
  }

  initializePriceTagsDropdown();

  // ---------------------------------------------------------------------------
  // Inventories
  initInventoriesTable();

  const inventoryModalClose = document.getElementById("inventory-modal-close");
  if (inventoryModalClose) {
    inventoryModalClose.addEventListener("click", () => {
      document.getElementById("inventory-modal").close();
    });
  }

  // ---------------------------------------------------------------------------
  // Producers
  initItemsManager({ name: "producer", endpoint: "producers" });
  // ---------------------------------------------------------------------------
  // Distributors
  initItemsManager({ name: "distributor", endpoint: "distributors" });
  // ---------------------------------------------------------------------------
  // Deposits
  initItemsManager({ name: "deposit", endpoint: "deposits" });
});
