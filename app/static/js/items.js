import { showToast } from "./utils.js";

// -----------------------------------------------------------------------------
export const initItemsManager = ({ name, endpoint }) => {
  const modal = document.getElementById(`${name}-modal`);
  const tableBody = document.querySelector(`#${name}s-table tbody`);
  const createBtn = document.getElementById(`create-${name}-button`);
  const deleteBtn = document.getElementById(`delete-${name}-button`);
  const form = document.getElementById(`${name}-form`);

  if (!tableBody || !modal) return;

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
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
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
};

// -----------------------------------------------------------------------------
export const deleteItems = async (tbody, endpoint) => {
  const checked = tbody.querySelectorAll(".checkbox:checked");

  for (const checkbox of checked) {
    const row = checkbox.closest("tr");
    const { id, name } = row.dataset;

    const response = await fetch(`/${endpoint}/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      const message =
        response.status === 409
          ? `'${name}' ne peut pas être supprimé`
          : "Erreur lors de la suppression";

      showToast(message, { type: "warning" });
      continue;
    }

    showToast(`'${name}' supprimé !`, { type: "success" });
    row.remove();
  }

  tbody.querySelectorAll(".checkbox").forEach((cb) => (cb.checked = false));
};
