import { initArticles } from "./articles/init.js";
import { initSearch } from "./search.js";
import {initArticleCreate} from "./article/init.js";
import {buildCreateDropdownMenu} from "./menu.js";

document.addEventListener("DOMContentLoaded", () => {
  initSearch();
  initArticles();
  buildCreateDropdownMenu();
});
