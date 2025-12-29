import {showToast} from "./utils.js";

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
