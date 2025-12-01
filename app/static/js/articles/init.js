import {calculationOnCostChange, calculationOnPriceChange, fillAndShowModal} from "./main.js";
import {getCategories} from "../categories.js";

export function initArticles() {
  const modal = document.getElementById("article-modal");
  if (!modal) return;

  initArticlesTable(modal);
  initModalClose(modal);
  initFormSubmit(modal);
  initFormCalculations(modal);
}

// -----------------------------------------------------------------------------
function initArticlesTable(modal) {
  const table = document.getElementById("articles-table");
  table.addEventListener("click", async (event) => {
    const row = event.target.closest("tbody tr");
    if (!row) return;

    fillAndShowModal(row, modal);
  });
}

// -----------------------------------------------------------------------------
function initModalClose(modal) {
  const closeButton = modal.querySelector("#article-modal-close");
  closeButton.addEventListener("click", () => modal.close());
}

// -----------------------------------------------------------------------------
function initFormSubmit(modal) {
  const form = document.getElementById("article-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.target;
    const data = Object.fromEntries(new FormData(form).entries());
    console.log(data);
    // TODO
  });
}

// -----------------------------------------------------------------------------
async function initFormCalculations(modal) {
  const categories = await getCategories();
  modal.addEventListener("input", (event) => {
    const input = event.target;

    if (input.matches("#cost_price, #vat_rate, #excise_duty, #social_security_contribution")) {
      calculationOnCostChange(categories);
    }

    if (input.matches('[data-store-field="gross_price"]')) {
      const storeCard = input.closest('[data-store]');
      const grossPrice = input.value || 0;
      calculationOnPriceChange(storeCard, grossPrice);
    }
  });
}
