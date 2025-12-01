// -----------------------------------------------------------------------------
export async function fetchArticleTemplate(articleId) {
  const response = await fetch(`/articles/update/${articleId}`);
  return await response.text();
}

// -----------------------------------------------------------------------------
export function getTotalCost() {
  const costPrice = parseFloat(document.getElementById("cost_price").value) || 0;
  const exciseDuty = parseFloat(document.getElementById("excise_duty").value) || 0;
  const socialSecurityContribution = parseFloat(document.getElementById("social_security_contribution").value) || 0;
  return  costPrice + exciseDuty + socialSecurityContribution;
}

// -----------------------------------------------------------------------------
export async function fetchRecommendedPrices({totalCost, vatRate, pricingGroup}) {
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      total_cost: totalCost,
      vat_rate: vatRate,
      pricing_group: pricingGroup
    })
  }
  const response = await fetch("/articles/recommended_prices", options);
  return  await response.json();
}

// -----------------------------------------------------------------------------
export async function fetchMargins({totalCost, vatRate, grossPrice}) {
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      total_cost: totalCost,
      vat_rate: vatRate,
      gross_price: grossPrice
    })
  }
  const response = await fetch("/articles/margins", options);
  return  await response.json();
}

// -----------------------------------------------------------------------------
export function updateRecommendedPrice(storeSlug, value) {
  const storeCard = document.querySelector(`[data-store="${storeSlug}"]`);

  const selector = '[data-store-field="recommended_price"]';
  storeCard.querySelector(`div${selector}`).textContent = `${value} €`;
  storeCard.querySelector(`input${selector}`).value = value;

  storeCard.querySelector('input[data-store-field="gross_price"]').value = value;
}


// -----------------------------------------------------------------------------
export function updateMargins(storeSlug, margins) {
  const storeCard = document.querySelector(`[data-store="${storeSlug}"]`);

  // Margin amount
  let selector = '[data-store-field="margin_amount"]';
  let value = margins.margin_amount;
  storeCard.querySelector(`div${selector}`).textContent = `${value} €`;
  storeCard.querySelector(`input${selector}`).value = value;

  // Margin rate
  selector = '[data-store-field="margin_rate"]';
  value = margins.margin_rate;
  storeCard.querySelector(`div${selector}`).textContent = `${value} %`;
  storeCard.querySelector(`input${selector}`).value = value;
}

// -----------------------------------------------------------------------------
export function colorGrossPrices() {
  const storeCards = document.querySelectorAll('[data-store]');
  storeCards.forEach(card => {
    const grossPriceInput = card.querySelector('input[data-store-field="gross_price"]');
    const recommendedPriceInput = card.querySelector('input[data-store-field="recommended_price"]');
    const grossPriceValue = parseFloat(grossPriceInput.value) || 0;
    const recommendedPriceValue = parseFloat(recommendedPriceInput.value);
    const labelContainer = grossPriceInput.closest('label');

    // Reset badge and classes
    labelContainer.classList.remove('input-success', 'input-error');
    const existingBadge = labelContainer.querySelector('.badge.dynamic-badge');
    if (existingBadge) {
      existingBadge.remove();
    }

    const difference = grossPriceValue - recommendedPriceValue;
    if (difference === 0) return;

    const sign = difference > 0 ? '+' : '';
    const badgeClass = difference > 0 ? 'badge-success' : 'badge-error';
    const labelClass = difference > 0 ? 'input-success' : 'input-error';
    const badgeSpan = document.createElement('span');
    badgeSpan.textContent = `${sign}${parseFloat(difference.toFixed(2))} €`;
    badgeSpan.className = `badge ${badgeClass} badge-xs dynamic-badge`;
    labelContainer.classList.add(labelClass);
    labelContainer.appendChild(badgeSpan);
  });
}

// -----------------------------------------------------------------------------
export function colorMarginRates() {
  const selector = '[data-store-field="margin_rate"]';
  const storeCards = document.querySelectorAll('[data-store]');

  storeCards.forEach(card => {
    const div = card.querySelector(`div${selector}`);
    const input = card.querySelector(`input${selector}`);

    // Reset classes
    div.classList.remove("text-success", "text-error");

    if (input.value > 5) {
      div.classList.add("text-success");
    } else {
      div.classList.add("text-error");
    }
  })
}
