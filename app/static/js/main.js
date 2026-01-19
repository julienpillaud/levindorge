import {
  initializeCheckboxes,
  updateArticleQuantity,
  updateCheckedArticles,
} from "./checkboxes.js";
import {
  initializePriceTagsDropdown,
  showSelectedArticles,
  unselectArticles,
} from "./price-labels.js";
import { buildCreateDropdownMenu } from "./menu.js";
import { initArticles } from "./articles/init.js";
import { initInventoriesTable } from "./inventories.js";
import { initItemsManager } from "./items.js";
import { initSearch } from "./search.js";

document.addEventListener("DOMContentLoaded", () => {
  initSearch();
  initArticles();
  buildCreateDropdownMenu();

  // ---------------------------------------------------------------------------
  // Articles table checkboxes
  initializeCheckboxes();

  document.addEventListener("change", (event) => {
    if (event.target.matches("#articles-table tbody .checkbox")) {
      updateCheckedArticles(event.target);
    }
  });
  document.addEventListener("input", (event) => {
    if (event.target.matches('#articles-table tbody [data-type="quantity"]')) {
      updateArticleQuantity(event.target);
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
  initItemsManager({ endpoint: "producers", name: "producer" });
  // ---------------------------------------------------------------------------
  // Distributors
  initItemsManager({ endpoint: "distributors", name: "distributor" });
  // ---------------------------------------------------------------------------
  // Deposits
  initItemsManager({ endpoint: "deposits", name: "deposit" });
  // ---------------------------------------------------------------------------
  // Volumes
  initItemsManager({ endpoint: "volumes", name: "volume" });
});
