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
import {createProducer} from "./producers.js";

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
  // Items
  const producerModal = document.getElementById("producer-modal");

  const createProducerButton = document.getElementById("create-producer-button");
  if (createProducerButton && producerModal) {
    createProducerButton.addEventListener("click", () => {
      producerModal.showModal();
    });
  }

  const producerForm = document.getElementById("producer-form");
  if (producerForm) {
    producerForm.addEventListener("reset", (event) => {
      producerModal.close();
    });

    producerForm.addEventListener("submit", (event) => {
      event.preventDefault();
      createProducer(producerForm);
      producerModal.close();
    })
  }

});
