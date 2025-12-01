// Toggle the visibility of the delete button based on checkbox selection in a table
export function initToggleDeleteButton() {
  const table = document.querySelector("table[data-scope]");
  const deleteButton = table.querySelector('[data-role="delete"]');
  if (!table || !deleteButton) {
    return;
  }

  table.addEventListener("change", (event) => {
    if (event.target.matches(".checkbox")) {
      const anyChecked = table.querySelectorAll(".checkbox:checked").length > 0;
      deleteButton.classList.toggle("hidden", !anyChecked);
    }
  });
}
