import { getCheckedArticleIds, setCheckedArticleIds } from "./checkboxes.js";
import { showToast, updateArticlesPage } from "./utils.js";
import { getStores } from "./cache/stores.js";

// -----------------------------------------------------------------------------
export const showSelectedArticles = () => {
  const ids = getCheckedArticleIds();
  const params = new URLSearchParams();

  ids.forEach((id) => params.append("article_ids", id));
  const url = `/articles/ids?${params.toString()}`;

  updateArticlesPage(url);
};

// -----------------------------------------------------------------------------
export const unselectArticles = () => {
  const checkboxes = document.querySelectorAll("table tbody .checkbox");
  checkboxes.forEach((checkbox) => (checkbox.checked = false));

  const priceTagsDropdown = document.getElementById("price-labels-dropdown");
  priceTagsDropdown.classList.add("hidden");

  setCheckedArticleIds([]);
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
  const ids = getCheckedArticleIds();
  if (ids.length === 0) {
    showToast("Aucun produit sélectionné", { type: "warning" });
    return;
  }

  const body = {
    data: ids.map((id) => ({
      article_id: id, // eslint-disable-line
      label_count: 1, // eslint-disable-line
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
