import { getCheckedArticleIds } from "./checkboxes.js";
import { updateArticlesPage } from "./utils.js";
import { getStores } from "./cache/stores.js";

// -----------------------------------------------------------------------------
export const showSelectedArticles = async () => {
  const ids = getCheckedArticleIds();
  const params = new URLSearchParams();

  ids.forEach((id) => params.append("article_ids", id));
  const url = `/articles/ids?${params.toString()}`;

  updateArticlesPage(url);
};

// -----------------------------------------------------------------------------
export const initializePriceTagsDropdown = async () => {
  const dropdown = document.getElementById("price-labels-dropdown");
  const ul = dropdown.querySelector("ul");

  const stores = await getStores();
  stores.forEach((store) => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.dataset.slug = store.slug;
    a.textContent = store.name;
    li.appendChild(a);
    ul.appendChild(li);
  });
};
