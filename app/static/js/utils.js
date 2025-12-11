import {initializeCheckboxes} from "./checkboxes.js";

export const showToast = (message, options = {}) => {
  const {
    type = "error",
    timeout = 5000,
    containerId = "main-toast-container",
  } = options;
  const container = document.getElementById(containerId);
  const toast = document.createElement("div");
  toast.className = `alert alert-${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, timeout);
};

// -----------------------------------------------------------------------------
export const updateArticlesPage = async (url) => {
  const response = await fetch(url);
  const responseText = await response.text();
  const parser = new DOMParser();
  const newDocument = parser.parseFromString(responseText, "text/html");

  updateElement("#articles-table", newDocument);
  updateElement("#items-count", newDocument);
  updateElement("#pagination", newDocument);
  initializeCheckboxes();
}

const updateElement = (selector, newDocument) => {
  const element = document.querySelector(selector);
  const newElement = newDocument.querySelector(selector);
  if (element && newElement) {
    element.innerHTML = newElement.innerHTML;
  }
}
