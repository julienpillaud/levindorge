import {
  getCheckedArticles,
  setCheckedArticles,
  toggleQuantityInput,
} from "./checkboxes.js";
import { showToast, updateArticlesPage } from "./utils.js";
import { getStores } from "./cache/stores.js";

// -----------------------------------------------------------------------------
export const showSelectedArticles = () => {
  const articles = getCheckedArticles();
  const params = new URLSearchParams();

  articles.forEach((article) => {
    params.append("article_ids", article.id);
  });

  const url = `/articles/ids?${params.toString()}`;

  updateArticlesPage(url);
};

// -----------------------------------------------------------------------------
export const unselectArticles = () => {
  const checkboxes = document.querySelectorAll("table tbody .checkbox");

  checkboxes.forEach((checkbox) => {
    checkbox.checked = false;
    toggleQuantityInput(checkbox);
  });

  const priceTagsDropdown = document.getElementById("price-labels-dropdown");
  priceTagsDropdown.classList.add("hidden");

  setCheckedArticles([]);
};

// -----------------------------------------------------------------------------
export const initializePriceTagsDropdown = async () => {
  const dropdown = document.getElementById("price-labels-dropdown");
  if (!dropdown) {
    return;
  }
  const ul = dropdown.querySelector("ul");

  const stores = await getStores();
  stores.forEach((store) => {
    const li = document.createElement("li");
    const link = document.createElement("a");
    link.dataset.slug = store.slug;
    link.textContent = store.name;
    li.appendChild(link);
    ul.appendChild(li);

    link.addEventListener("click", () => {
      const { slug } = link.dataset;
      createPriceLabels(slug);
    });
  });
};

// -----------------------------------------------------------------------------
const createPriceLabels = async (slug) => {
  const articles = getCheckedArticles();
  if (articles.length === 0) {
    showToast("Aucun produit sélectionné", { type: "warning" });
    return;
  }

  const body = {
    data: articles.map((article) => ({
      article_id: article.id, // eslint-disable-line
      label_count: article.quantity, // eslint-disable-line
    })),
    store_slug: slug, // eslint-disable-line
  };
  const options = {
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
    method: "POST",
  };
  const response = await fetch("/price-labels", options);
  if (!response.ok) {
    showToast("Erreur lors de la création des étiquettes !");
    const error = await response.json();
    console.error(error); // eslint-disable-line
    return;
  }
  showToast("Etiquettes créées !", { type: "success" });
};
