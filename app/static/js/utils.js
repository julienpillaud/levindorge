function normalizeString(str) {
  return str
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

let searchTimer;

export function searchTable(query) {
  clearTimeout(searchTimer);

  searchTimer = setTimeout(() => {
    const trimmed = query.trim();
    let url = "/articles";

    if (trimmed) {
      url += "?search=" + encodeURIComponent(trimmed);
    }

    window.location = url;
  }, 500);
}

export function setCursor() {
  const inputs = document.querySelectorAll("#search-mobile, #search-desktop");

  inputs.forEach((input) => {
    input.focus();
    input.setSelectionRange(input.value.length, input.value.length);
  });
}

export function resetCheckBoxes(checkedBoxes) {
  checkedBoxes.forEach((cb) => (cb.checked = false));
}

export function resetDeleteButton(deleteButton) {
  deleteButton.classList.add("hidden");
}

export function updateCountBadge(table) {
  const itemsCount = table.querySelectorAll("tbody tr").length;
  const badge = document.getElementById("items-count");
  badge.textContent = String(itemsCount);
}

export function swapDeleteButton() {
  const deleteBtn = document.getElementById("items-delete-button");
  const allCheckboxes = document.querySelectorAll(".checkbox");
  const anyChecked = Array.from(allCheckboxes).some(
    (checkbox) => checkbox.checked,
  );
  deleteBtn.classList.toggle("hidden", !anyChecked);
}

export function showToast(message, type = "error", timeout = 5000) {
  const container = document.querySelector(".toast");
  const toast = document.createElement("div");
  toast.className = `alert alert-${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, timeout);
}

export function setOverlayVisible(show) {
  const overlay = document.getElementById("loading-overlay");
  overlay.classList.toggle("hidden", !show);
}

export function colorStockQuantities() {
  document
    .querySelectorAll('td[data-field="stock_quantity"]')
    .forEach((elem) => {
      const div = elem.querySelector("div");
      const value = parseFloat(div?.textContent.trim()) || 0;

      div.classList.remove(
        "badge",
        "badge-sm",
        "badge-soft",
        "badge-success",
        "badge-error",
      );

      if (value > 0) {
        div.classList.add("badge", "badge-sm", "badge-soft", "badge-success");
      } else if (value < 0) {
        div.classList.add("badge", "badge-sm", "badge-soft", "badge-error");
      }
    });
}
