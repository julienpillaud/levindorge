function normalizeString(str) {
    return str
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();
}


export function searchTable(query) {
    const normalizedQuery = normalizeString(query);
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach((row) => {
        const rowText = normalizeString(row.textContent);
        row.style.display = rowText.includes(normalizedQuery) ? '' : 'none';
    });
}


export function resetCheckBoxes(checkedBoxes) {
    checkedBoxes.forEach(cb => cb.checked = false);
}


export function resetDeleteButton(deleteButton) {
    deleteButton.classList.add('hidden');
}


export function updateCountBadge(table) {
    const itemsCount = table.querySelectorAll('tbody tr').length;
    const badge = document.getElementById('items-count');
    badge.textContent = String(itemsCount);
}


export function swapDeleteButton() {
    const deleteBtn = document.getElementById('items-delete-button');
    const allCheckboxes = document.querySelectorAll('.checkbox');
    const anyChecked = Array.from(allCheckboxes).some(checkbox => checkbox.checked);
    deleteBtn.classList.toggle('hidden', !anyChecked);
}


export function showToast(message, type = 'error', timeout = 5000) {
    const container = document.querySelector('.toast');
    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, timeout);
}


export function setOverlayVisible(show) {
  const overlay = document.getElementById('loading-overlay');
  overlay.classList.toggle('hidden', !show);
}
