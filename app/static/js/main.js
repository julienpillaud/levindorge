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
import { createItem, deleteItems } from "./items.js";

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
  const producerModal = document.getElementById("producer-modal");
  const producersTableBody = document.querySelector("#producers-table tbody");

  const createProducerButton = document.getElementById(
    "create-producer-button",
  );
  createProducerButton?.addEventListener("click", () => {
    producerModal?.showModal();
  });

  const producerForm = document.getElementById("producer-form");
  producerForm?.addEventListener("reset", () => {
    producerModal.close();
  });
  producerForm?.addEventListener("submit", (event) => {
    event.preventDefault();
    createItem(producerForm, producersTableBody, "producers");
    producerModal?.close();
  });

  const deleteProducersButton = document.getElementById(
    "delete-producer-button",
  );
  producersTableBody?.addEventListener("change", (event) => {
    if (event.target.matches(".checkbox")) {
      const hasChecked =
        producersTableBody.querySelector(".checkbox:checked") !== null;
      deleteProducersButton?.classList.toggle("hidden", !hasChecked);
    }
  });
  deleteProducersButton?.addEventListener("click", async () => {
    await deleteItems(producersTableBody, "producers");
    deleteProducersButton?.classList.toggle("hidden", true);
  });
  // ---------------------------------------------------------------------------
  // Distributors
  const distributorModal = document.getElementById("distributor-modal");
  const distributorTableBody = document.querySelector(
    "#distributors-table tbody",
  );

  const createDistributorButton = document.getElementById(
    "create-distributor-button",
  );
  createDistributorButton?.addEventListener("click", () => {
    distributorModal?.showModal();
  });

  const distributorForm = document.getElementById("distributor-form");
  distributorForm?.addEventListener("reset", () => {
    distributorModal.close();
  });
  distributorForm?.addEventListener("submit", (event) => {
    event.preventDefault();
    createItem(distributorForm, distributorTableBody, "distributors");
    distributorModal?.close();
  });

  const deleteDistributorsButton = document.getElementById(
    "delete-distributor-button",
  );
  distributorTableBody?.addEventListener("change", (event) => {
    if (event.target.matches(".checkbox")) {
      const hasChecked =
        distributorTableBody.querySelector(".checkbox:checked") !== null;
      deleteDistributorsButton?.classList.toggle("hidden", !hasChecked);
    }
  });
  deleteDistributorsButton?.addEventListener("click", async () => {
    await deleteItems(distributorTableBody, "distributors");
    deleteDistributorsButton?.classList.toggle("hidden", true);
  });
  // ---------------------------------------------------------------------------
});
