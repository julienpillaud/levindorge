import {showToast} from "./utils.js";

// -----------------------------------------------------------------------------
export const createProducer = async (form) => {
  const data = Object.fromEntries(new FormData(form));
  const options = {
    body: JSON.stringify(data),
    method: "POST",
    headers: {"Content-Type": "application/json"},
  };
  const response = await fetch("/producers", options);
  if (!response.ok) {
    let message = "Erreur lors de la création"
    if (response.status === 409) {
      message = `${data.name} existe déjà`
    }
    showToast(message, {type: "warning"});
    form.reset();

    const error = await response.json();
    console.error(error); // eslint-disable-line
    return;
  }

  const html = await response.text();
  const tbody = document.querySelector("table tbody");
  tbody.insertAdjacentHTML("afterbegin", html);
  showToast(`${data.name} créé !`, {type: "success"})
  form.reset();
}

// -----------------------------------------------------------------------------
export const deleteProducers = async (tbody) => {
  const checked = tbody.querySelectorAll(".checkbox:checked");
  for (const checkbox of checked) {
    const row = checkbox.closest("tr");
    const {id, name} = row.dataset;

    const response = await fetch(`/producers/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      let message = "Erreur lors de la suppression"
      if (response.status === 409) {
        message = `${name} ne peut pas être supprimé`
      }
      showToast(message, {type: "warning"});
      continue;
    }

    showToast(`${name} supprimé !`, {type: "success"})
    row.remove();
  }
  tbody.querySelectorAll(".checkbox").forEach(cb => cb.checked = false);
}
