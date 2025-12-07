import {
  calculationOnCostChange,
  calculationOnPriceChange, createArticle,
  fillAndShowModal,
  updateArticle,
} from "./main.js";
import { getCategories } from "../cache/categories.js";

export const initArticles = () => {
  const modal = document.getElementById("article-modal");
  if (!modal) {
    return;
  }

  initArticlesTable(modal);
  initModalClose(modal);
  initFormSubmit(modal);
  initFormCalculations(modal);
};

// -----------------------------------------------------------------------------
const initArticlesTable = (modal) => {
  const table = document.getElementById("articles-table");
  table.addEventListener("click", (event) => {
    const row = event.target.closest("tbody tr");
    if (!row) {
      return;
    }

    fillAndShowModal(row, modal);
  });
};

// -----------------------------------------------------------------------------
const initModalClose = (modal) => {
  const form = document.getElementById("article-form");
  form.addEventListener("reset", () => modal.close());
};

// -----------------------------------------------------------------------------
const initFormSubmit = (modal) => {
  const form = document.getElementById("article-form");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const {action} = event.submitter.dataset;
    if (action === "update") {
      updateArticle(form);
    } else {
      createArticle(form);
    }
    modal.close();
  });
};

// -----------------------------------------------------------------------------
const initFormCalculations = async (modal) => {
  const categories = await getCategories();
  modal.addEventListener("input", (event) => {
    const input = event.target;

    if (
      input.matches(
        "#cost_price, #vat_rate, #excise_duty, #social_security_contribution",
      )
    ) {
      calculationOnCostChange(categories);
    }

    if (input.matches('[data-store-field="gross_price"]')) {
      const storeCard = input.closest("[data-store]");
      const grossPrice = input.value || 0;
      calculationOnPriceChange(storeCard, grossPrice);
    }
  });
};
