import {colorGrossPrices, colorMarginRates, fetchArticleTemplate, fetchMargins, fetchRecommendedPrices, getTotalCost, updateMargins, updateRecommendedPrice} from "./utils.js";

// -----------------------------------------------------------------------------
export const fillAndShowModal = async (row, modal) => {
  const modalContent = document.getElementById("article-modal-content");
  modalContent.innerHTML = await fetchArticleTemplate(row.dataset.id);
  modal.showModal();
  colorGrossPrices();
  colorMarginRates();
}

// -----------------------------------------------------------------------------
export const calculationOnCostChange =  async (categories) => {
  // Total cost
  const totalCost = getTotalCost();
  document.getElementById("total_cost").value = `${parseFloat(totalCost.toFixed(4))} €`;

  // Recommended price
  const articleCategory = document.getElementById('article-category').dataset.category;
  const pricingGroup = categories[articleCategory].pricing_group;
  const vatRate = parseFloat(document.getElementById("vat_rate").value);

  const recommendedPrices = await fetchRecommendedPrices({
    pricingGroup,
    totalCost,
    vatRate,
  })

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
  colorMarginRates();
}

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
  colorMarginRates();
}
