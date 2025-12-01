import {initSearch} from "./search.js";
import {initArticles} from "./articles/init.js";

document.addEventListener("DOMContentLoaded", () => {
  initSearch();
  initArticles();
});
