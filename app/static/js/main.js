import { buildCreateDropdownMenu } from "./menu.js";
import { initArticles } from "./articles/init.js";
import { initSearch } from "./search.js";

document.addEventListener("DOMContentLoaded", () => {
  initSearch();
  initArticles();
  buildCreateDropdownMenu();
});
