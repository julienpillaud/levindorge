import { showToast } from "./utils.js";

// -----------------------------------------------------------------------------
export const createItem = async (form, tbody, endpoint) => {
  const data = Object.fromEntries(new FormData(form));

  const response = await fetch(`/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    let message = "Erreur lors de la création";
    if (response.status === 409) {
      message = `${data.name} existe déjà`;
    }
    showToast(message, { type: "warning" });
    form.reset();
    return;
  }

  const html = await response.text();
  tbody.insertAdjacentHTML("afterbegin", html);
  showToast(`${data.name} créé !`, { type: "success" });
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
          ? `${name} ne peut pas être supprimé`
          : "Erreur lors de la suppression";

      showToast(message, { type: "warning" });
      continue;
    }

    showToast(`${name} supprimé !`, { type: "success" });
    row.remove();
  }

  tbody.querySelectorAll(".checkbox").forEach((cb) => (cb.checked = false));
};
