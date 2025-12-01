import { deletePriceLabelsFile } from "../api/price_labels.js";
import {
  resetCheckBoxes,
  resetDeleteButton,
  showToast,
  updateCountBadge,
} from "../utils.js";

export function initDeletePriceLabels() {
  const table = document.querySelector('table[data-scope="price-labels"]');
  const deleteButton = table.querySelector('[data-role="delete"]');
  if (!table || !deleteButton) {return;}

  deleteButton.addEventListener("click", async () => {
    await handleDeletePriceLabels(table, deleteButton);
  });
}

async function handleDeletePriceLabels(table, deleteButton) {
  const checkedBoxes = table.querySelectorAll("tr .checkbox:checked");
  const rows = Array.from(checkedBoxes).map((cb) => cb.closest("tr"));

  for (const row of rows) {
    const { file } = row.dataset;
    const response = await deletePriceLabelsFile(file);

    if (response.ok) {
      row.remove();
    } else {
      const error = await response.json();
      showToast(error.detail);
    }
  }
  resetCheckBoxes(checkedBoxes);
  resetDeleteButton(deleteButton);
  updateCountBadge(table);
}
