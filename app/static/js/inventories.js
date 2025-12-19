export const initInventoriesTable = () => {
  const table = document.getElementById("inventories-table");
  if (!table) {
    return;
  }

  table.addEventListener("click", async (event) => {
    const row = event.target.closest("tbody tr");
    if (!row) {
      return;
    }

    const modalContent = document.getElementById("inventory-modal-content");
    modalContent.innerHTML = await fetchInventory(row.dataset.id);

    const modal = document.getElementById("inventory-modal");
    modal.showModal();
  });
};

const fetchInventory = async (id) => {
  const response = await fetch(`/inventories/${id}`);
  return await response.text();
};
