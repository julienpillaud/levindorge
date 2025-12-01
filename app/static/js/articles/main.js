import {fetchArticleTemplate, getTotalCost, fetchRecommendedPrices, fetchMargins, updateMargins, colorGrossPrices, colorMarginRates, updateRecommendedPrice} from "./utils.js";

// -----------------------------------------------------------------------------
export async function fillAndShowModal(row, modal) {
  const modalContent = document.getElementById("article-modal-content");
  modalContent.innerHTML = await fetchArticleTemplate(row.dataset.id);
  modal.showModal();
  colorGrossPrices();
  colorMarginRates();
}

// -----------------------------------------------------------------------------
export async function calculationOnCostChange(categories) {
  // Total cost
  const totalCost = getTotalCost();
  document.getElementById("total_cost").value = `${parseFloat(totalCost.toFixed(4))} €`;

  // Recommended price
  const articleCategory = document.getElementById('article-category').dataset.category;
  const pricingGroup = categories[articleCategory]["pricing_group"];
  const vatRate = parseFloat(document.getElementById("vat_rate").value);

  const recommendedPrices = await fetchRecommendedPrices({
    totalCost: totalCost,
    vatRate: vatRate,
    pricingGroup: pricingGroup
  })

  // Margins
  for (const [storeSlug, value] of Object.entries(recommendedPrices)) {
    updateRecommendedPrice(storeSlug, value);
    const margins = await fetchMargins({
      totalCost: totalCost,
      vatRate: vatRate,
      grossPrice: value
    });
    updateMargins(storeSlug, margins);
  }

  // Colors
  colorGrossPrices();
  colorMarginRates();
}

// -----------------------------------------------------------------------------
/**
 * Update margins for a given store
 */
export async function calculationOnPriceChange(storeCard, value) {
  const storeSlug = storeCard.dataset.store;
  const totalCost = getTotalCost();
  const vatRate = parseFloat(document.getElementById("vat_rate").value) || 0;

  const margins = await fetchMargins({
    totalCost: totalCost,
    vatRate: vatRate,
    grossPrice: value
  });

  updateMargins(storeSlug, margins);
  colorGrossPrices();
  colorMarginRates();
}
