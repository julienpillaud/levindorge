import { colorStockQuantities, swapDeleteButton } from "./utils.js";
import { createItem, deleteItems } from "./api/items.js";
import { createInventory, resetStocks } from "./api/inventories.js";

export function initCreateItemListener() {
  const modalOpen = document.getElementById("item-create-button");
  const modal = document.getElementById("item-create-modal");
  const modalForm = document.getElementById("item-create-form");
  const modalClose = document.getElementById("item-create-modal-close");
  if (!modalOpen || !modal || !modalForm || !modalClose) {
    console.log("initCreateItemListener: skipping listener initialization");
    return;
  }

  modalOpen.addEventListener("click", () => {
    modal.showModal();
  });
  modalClose.addEventListener("click", () => {
    modal.close();
    modalForm.reset();
  });

  modalForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await createItem(modalForm);
  });
}

export function initDeleteItemsListener() {
  const itemsTable = document.getElementById("items-table");
  const itemsDeleteBtn = document.getElementById("items-delete-button");
  if (!itemsTable || !itemsDeleteBtn) {
    console.log("initDeleteItemsListener: skipping listener initialization");
    return;
  }

  itemsTable.addEventListener("change", (event) => {
    if (event.target.matches(".checkbox")) {
      swapDeleteButton();
    }
  });

  const { category } = itemsDeleteBtn.dataset;
  itemsDeleteBtn.addEventListener("click", async () => {
    await deleteItems(category);
  });
}

export function initCreateInventoryListener() {
  const createInventoryBtns = document.querySelectorAll(
    '[data-action="create-inventory"]',
  );
  if (!createInventoryBtns.length) {
    return;
  }

  createInventoryBtns.forEach((elem) => {
    elem.addEventListener("click", async (event) => {
      event.preventDefault();
      const { shop } = event.target.dataset;
      await createInventory(shop);
    });
  });
}

export function initResetStocksListener() {
  const modalOpen = document.getElementById("reset-stocks-button");
  const modal = document.getElementById("reset-stocks-modal");
  const modalForm = document.getElementById("reset-stocks-form");
  const modalClose = document.getElementById("reset-stocks-modal-close");
  if (!modalOpen || !modal || !modalForm || !modalClose) {
    console.log("initResetStocksListener: skipping listener initialization");
    return;
  }

  modalOpen.addEventListener("click", () => {
    modal.showModal();
  });
  modalClose.addEventListener("click", () => {
    modal.close();
    modalForm.reset();
  });

  modalForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await resetStocks(modalForm);
  });
}

export function initSelectShopListener() {
  const shopSelect = document.getElementById("shop-select");
  if (!shopSelect) {
    return;
  }

  shopSelect.addEventListener("change", (event) => {
    const shop = event.target.value;
    const articlesData = JSON.parse(
      document.getElementById("articles-data").textContent,
    );

    document.querySelectorAll("tr[data-id]").forEach((row) => {
      const articleId = row.dataset.id;
      const data = articlesData[articleId][shop];
      row.querySelector('td[data-field="recommended_price"]').textContent =
        data.recommended_price;
      row.querySelector('td[data-field="sell_price"]').textContent =
        data.sell_price;
      row.querySelector('td[data-field="margin"]').textContent =
        data.margins.margin;
      row.querySelector('td[data-field="markup"]').textContent =
        data.margins.markup;
      const cell = row.querySelector('td[data-field="stock_quantity"]');
      const div = cell.querySelector("div");
      div.textContent = data.stock_quantity === 0 ? "" : data.stock_quantity;
      colorStockQuantities();
    });
  });
}

export function initArticleModalListener() {
  const articlesTableRows = document.querySelectorAll("#articles-table tbody tr");
  const modal = document.getElementById("article-modal");
  const modalContent = modal.querySelector("div");

  articlesTableRows.forEach(row => {
    row.addEventListener("click", async () => {
      const {id} = row.dataset;
      const response = await fetch(`/articles/update/${id}`);
      const html = await response.text();
      modalContent.innerHTML = html;
      modal.showModal();
    });
  });
}
