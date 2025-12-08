import {
  colorGrossPrices,
  colorMarginAmounts,
  colorMarginRates,
  fetchArticleTemplate,
  fetchMargins,
  fetchRecommendedPrices,
  getTotalCost,
  updateMargins,
  updateRecommendedPrice,
} from "./utils.js";
import { showToast } from "../utils.js";

// -----------------------------------------------------------------------------
export const fillAndShowModal = async (row, modal) => {
  const modalContent = document.getElementById("article-modal-content");
  modalContent.innerHTML = await fetchArticleTemplate(row.dataset.id);
  modal.showModal();
  colorGrossPrices();
  colorMarginAmounts();
  colorMarginRates();
};

// -----------------------------------------------------------------------------
export const calculationOnCostChange = async (categories, input) => {
  // Total cost
  const totalCost = getTotalCost();
  const totalCostInput = document.getElementById("total_cost");
  totalCostInput.value = `${parseFloat(totalCost.toFixed(4))} €`;

  // Recommended price
  const articleCategory = document.querySelector('[name="category"]').value;
  if (!articleCategory) {
    input.value = "";
    totalCostInput.value = "";
    showToast("Choisis une catégorie !", {
      containerId: "modal-toast-container",
    });
    return;
  }
  const pricingGroup = categories[articleCategory].pricing_group;
  const vatRate = parseFloat(document.getElementById("vat_rate").value) || 0;

  const recommendedPrices = await fetchRecommendedPrices({
    pricingGroup,
    totalCost,
    vatRate,
  });

  // Margins
  const entries = Object.entries(recommendedPrices);

  const promises = entries.map(async ([storeSlug, value]) => {
    updateRecommendedPrice(storeSlug, value);
    const margins = await fetchMargins({
      grossPrice: value,
      totalCost,
      vatRate,
    });
    updateMargins(storeSlug, margins);
  });

  await Promise.all(promises);

  // Colors
  colorGrossPrices();
  colorMarginAmounts();
  colorMarginRates();
};

// -----------------------------------------------------------------------------
/**
 * Update margins for a given store
 */
export const calculationOnPriceChange = async (storeCard, value) => {
  const storeSlug = storeCard.dataset.store;
  const totalCost = getTotalCost();
  const vatRate = parseFloat(document.getElementById("vat_rate").value) || 0;

  const margins = await fetchMargins({
    grossPrice: value,
    totalCost,
    vatRate,
  });

  updateMargins(storeSlug, margins);
  colorGrossPrices();
  colorMarginAmounts();
  colorMarginRates();
};

// -----------------------------------------------------------------------------
export const updateArticle = async (form) => {
  const articleId = document.getElementById("article-id").value;
  const formData = new FormData(form);
  const options = {
    body: formData,
    method: "POST",
  };
  const response = await fetch(`/articles/update/${articleId}`, options);
  if (!response.ok) {
    showToast("Erreur lors de la mise à jour");
    const error = await response.json();
    console.error(error); // eslint-disable-line
    return;
  }
  const html = await response.text();

  const oldRow = document.querySelector(`tr[data-id="${articleId}"]`);
  const temp = document.createElement("tbody");
  temp.innerHTML = html.trim();
  const newRow = temp.firstElementChild;
  oldRow.replaceWith(newRow);

  showToast("Produit mis à jour !", { type: "success" });
};

export const createArticle = async (form) => {
  const formData = new FormData(form);
  const options = {
    body: formData,
    method: "POST",
  };
  const response = await fetch("/articles/create", options);
  if (!response.ok) {
    showToast("Erreur lors de la création");
    const error = await response.json();
    console.error(error); // eslint-disable-line
    return;
  }
  const html = await response.text();

  const temp = document.createElement("tbody");
  temp.innerHTML = html.trim();
  const newRow = temp.firstElementChild;

  const tbody = document.querySelector("table tbody");
  tbody.prepend(newRow);

  const counter = document.getElementById("items-count");
  counter.textContent = String(parseInt(counter.textContent, 10) + 1);

  showToast("Produit créé !", { type: "success" });
};
