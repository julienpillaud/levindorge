import { setOverlayVisible, showToast } from "../utils.js";

export async function createInventory(shop) {
  // Close the dropdown
  document
    .querySelectorAll("details[open]")
    .forEach((d) => d.removeAttribute("open"));

  setOverlayVisible(true);

  // Call the API
  const response = await fetch("/inventories", {
    method: "POST",
    body: shop,
  });

  // Handle errors
  if (!response.ok) {
    const error = await response.json();
    showToast(error.detail);
    setOverlayVisible(false);
    return;
  }

  // Insert the new item at the top of the table
  const html = await response.text();
  const tbody = document.getElementById("items-table").querySelector("tbody");
  tbody.insertAdjacentHTML("afterbegin", html);

  setOverlayVisible(false);
}

export async function resetStocks(form) {
  const formData = new FormData(form);

  setOverlayVisible(true);

  // Call the API
  const response = await fetch("/inventories/stocks/reset", {
    method: "POST",
    body: formData,
  });

  // Close the modal
  document.getElementById("reset-stocks-modal").close();

  // Handle errors
  if (!response.ok) {
    const error = await response.json();
    showToast(error.detail);
    setOverlayVisible(false);
    return;
  }

  setOverlayVisible(false);
}
