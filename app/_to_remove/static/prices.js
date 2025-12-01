window.addEventListener("DOMContentLoaded", () => {
  // -------------------------------------------------------------------------
  if (document.getElementById("create-update-article-form")) {
    computeAll(true);
  }

  // -------------------------------------------------------------------------
  const buyPriceArray = document.querySelectorAll(
    "#tax, #buy_price, #excise_duty, #social_security_levy",
  );
  buyPriceArray.forEach((elem) => {
    elem.addEventListener("input", () => {
      computeAll();
    });
  });

  // -------------------------------------------------------------------------
  const sellPriceArray = document.querySelectorAll("[id^='sell_price_']");
  sellPriceArray.forEach((elem) => {
    // Disable hidden input to avoid validation errors
    elem.disabled =
      window.getComputedStyle(elem.closest(".row"), null).display === "none";

    elem.addEventListener("input", () => {
      const shop = elem.id.split("sell_price_")[1];
      // Fill hidden input with the same value
      document.getElementById(`_sell_price_${  shop}`).value = elem.value;

      computeMargins(elem.value, shop);
    });
  });

  // -------------------------------------------------------------------------
  const sellPriceArray_ = document.querySelectorAll("[id^='_sell_price_']");
  sellPriceArray_.forEach((elem) => {
    // Disable hidden input to avoid validation errors
    elem.disabled =
      window.getComputedStyle(elem.closest(".row"), null).display === "none";

    elem.addEventListener("input", () => {
      const shop = elem.id.split("_sell_price_")[1];
      // Fill hidden input with the same value
      document.getElementById(`sell_price_${  shop}`).value = elem.value;

      computeMargins(elem.value, shop);
    });
  });
});

// =============================================================================
function calculateTaxfreePrice() {
  const buy_price = document.getElementById("buy_price");
  const buy_price_value = buy_price ? buy_price.value : 0;

  const excise_duty = document.getElementById("excise_duty");
  const excise_duty_value = excise_duty ? excise_duty.value : 0;

  const social_security_levy = document.getElementById("social_security_levy");
  const social_security_levy_value = social_security_levy
    ? social_security_levy.value
    : 0;

  const value =
    Number(buy_price_value) +
    Number(excise_duty_value) +
    Number(social_security_levy_value);

  return Math.round(value * 10000) / 10000;
}

// =============================================================================
function fetchRecommendedPrices() {
  const ratioCategory = document.getElementById("ratio_category").value;
  const tax = document.getElementById("tax").value;
  const taxfreePrice = document.getElementById("taxfree_price").value;

  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ratio_category: ratioCategory,
      taxfree_price: Number(taxfreePrice),
      tax: Number(tax),
    }),
  };
  return fetch("/articles/recommended_prices", options).then((response) =>
    response.json(),
  );
}

function fillRecommendedPrices(shop, recommendedPrice, on_load) {
  document.getElementById(`recommended_price_${  shop}`).value = recommendedPrice;
  document.getElementById(`_recommended_price_${  shop}`).value =
    recommendedPrice;
  if (!on_load) {
    document.getElementById(`sell_price_${  shop}`).value = recommendedPrice;
    document.getElementById(`_sell_price_${  shop}`).value = recommendedPrice;
  }
}

// =============================================================================
function fetchMargins(sellPrice) {
  const taxfreePrice = document.getElementById("taxfree_price").value;
  const tax = document.getElementById("tax").value;

  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      sell_price: Number(sellPrice),
      taxfree_price: Number(taxfreePrice),
      tax: Number(tax),
    }),
  };
  return fetch("/articles/margins", options).then((response) =>
    response.json(),
  );
}

function fillMargins(shop, margins) {
  document.getElementById(`profit_${  shop}`).value = margins.margin;
  document.getElementById(`margin_${  shop}`).value = margins.markup;
  document.getElementById(`_profit_${  shop}`).value = margins.margin;
  document.getElementById(`_margin_${  shop}`).value = margins.markup;
}

// =============================================================================
function colorPrices(shop, markup) {
  const recommendedPrice = document.getElementById(
    `recommended_price_${  shop}`,
  ).value;

  const sellPriceElem = document.getElementById(`sell_price_${  shop}`);
  colorPrice(sellPriceElem, recommendedPrice, markup);

  const sellPriceElem_ = document.getElementById(`_sell_price_${  shop}`);
  colorPrice(sellPriceElem_, Number(recommendedPrice), markup);
}

function colorPrice(sellPriceElem, recommendedPrice, markup) {
  if (markup < 5) {
    sellPriceElem.style.background = "darkred";
  } else if (Number(sellPriceElem.value) < recommendedPrice) {
      sellPriceElem.style.background = "crimson";
    } else if (Number(sellPriceElem.value) > recommendedPrice) {
      sellPriceElem.style.background = "darkgreen";
    } else {
      sellPriceElem.style.background = "";
    }
}

// =============================================================================
function computeAll(on_load = false) {
  const taxfreePrice = calculateTaxfreePrice();
  if (taxfreePrice === 0) {
    return;
  }
  document.getElementById("taxfree_price").value = taxfreePrice;

  fetchRecommendedPrices().then((response) => {
    Object.keys(response).forEach((shop) => {
      const recommendedPrice = response[shop];
      console.log("PVC", shop, recommendedPrice);
      fillRecommendedPrices(shop, recommendedPrice, on_load);

      const sellPrice = document.getElementById(`sell_price_${  shop}`).value;
      fetchMargins(sellPrice).then((response) => {
        fillMargins(shop, response);
        colorPrices(shop, response.markup);
      });
    });
  });
}

function computeMargins(sellPrice, shop) {
  fetchMargins(sellPrice).then((response) => {
    fillMargins(shop, response);
    colorPrices(shop, response.markup);
  });
}

function showOverlay() {
  document.getElementById("overlay").style.display = "flex";
}
