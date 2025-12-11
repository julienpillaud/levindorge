import { getCheckedArticleIds } from "./checkboxes.js";
import { getStores } from "./cache/stores.js";
import { updateArticlesPage } from "./utils.js";

// -----------------------------------------------------------------------------
export const showSelectedArticles = () => {
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
    const link = document.createElement("a");
    link.dataset.slug = store.slug;
    link.textContent = store.name;
    li.appendChild(link);
    ul.appendChild(li);
  });
};
