import { showToast } from "./utils.js";

// -----------------------------------------------------------------------------
export const initItemsManager = ({ name, endpoint }) => {
  const modal = document.getElementById(`${name}-modal`);
  const tableBody = document.querySelector(`#${name}s-table tbody`);
  const createBtn = document.getElementById(`create-${name}-button`);
  const deleteBtn = document.getElementById(`delete-${name}-button`);
  const form = document.getElementById(`${name}-form`);

  if (!tableBody || !modal) {
    return;
  }

  // Modal opening - closing
  createBtn?.addEventListener("click", () => modal.showModal());
  form?.addEventListener("reset", () => modal.close());

  // Form submission
  form?.addEventListener("submit", (event) => {
    event.preventDefault();
    createItem(form, tableBody, endpoint);
    modal.close();
  });

  // Delete button visibility
  tableBody.addEventListener("change", (event) => {
    if (event.target.matches(".checkbox")) {
      const hasChecked = tableBody.querySelector(".checkbox:checked") !== null;
      deleteBtn?.classList.toggle("hidden", !hasChecked);
    }
  });

  // Delete button action
  deleteBtn?.addEventListener("click", async () => {
    await deleteItems(tableBody, endpoint);
    deleteBtn.classList.toggle("hidden", true);
  });
};

// -----------------------------------------------------------------------------
export const createItem = async (form, tbody, endpoint) => {
  const data = Object.fromEntries(new FormData(form));

  const response = await fetch(`/${endpoint}`, {
    body: JSON.stringify(data),
    headers: { "Content-Type": "application/json" },
    method: "POST",
  });

  if (!response.ok) {
    const errorData = await response.json();
    const message = errorData.detail || "Erreur lors de la création";
    showToast(message, { type: "warning" });
    form.reset();
    return;
  }

  const displayName = response.headers.get("X-Display-Name") || "Élément";
  const html = await response.text();
  tbody.insertAdjacentHTML("afterbegin", html);
  showToast(`'${displayName}' créé !`, { type: "success" });
  form.reset();

  const counter = document.getElementById("items-count");
  counter.textContent = String(parseInt(counter.textContent, 10) + 1);
};

// -----------------------------------------------------------------------------
export const deleteItems = async (tbody, endpoint) => {
  const checked = Array.from(tbody.querySelectorAll(".checkbox:checked"));

  const results = await Promise.all(
    checked.map((cb) => deleteSingleItem(cb, endpoint)),
  );

  const counter = document.getElementById("items-count");
  const successCount = results.filter(Boolean).length;
  if (successCount > 0) {
    counter.textContent = String(Number(counter.textContent) - successCount);
  }

  tbody.querySelectorAll(".checkbox").forEach((cb) => (cb.checked = false));
};

// -----------------------------------------------------------------------------
const deleteSingleItem = async (checkbox, endpoint) => {
  const row = checkbox.closest("tr");
  const { id, name } = row.dataset;
  const response = await fetch(`/${endpoint}/${id}`, { method: "DELETE" });

  if (!response.ok) {
    const message =
      response.status === 409
        ? `'${name}' ne peut pas être supprimé`
        : "Erreur lors de la suppression";
    showToast(message, { type: "warning" });
    return false;
  }

  showToast(`'${name}' supprimé !`, { type: "success" });
  row.remove();
  return true;
};
