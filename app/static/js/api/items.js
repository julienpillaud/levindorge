import {swapDeleteButton, showToast} from "../utils.js";


function updateCountBadge() {
    const table = document.getElementById('items-table');
    const itemsCount = table.querySelectorAll('tbody tr').length;

    const badge = document.getElementById('items-count');
    badge.textContent = String(itemsCount);
}


export async function createItem(form) {
    const {category} = form.dataset;
    const formData = new FormData(form);

    let url;
    if (category === 'volumes' || category === 'deposits') {
        url = `/${category}`;
    } else {
        url = `/items/${category}`;
    }
    const response = await fetch(url, {
        method: 'POST',
        body: formData,
    });

    // Close the modal
    document.getElementById('item-create-modal').close();

    // Handle errors
    if (!response.ok) {
        const error = await response.json();
        showToast(error.detail);
        return;
    }

    // Insert the new item at the top of the table
    const html = await response.text();
    const tbody = document.getElementById('items-table').querySelector('tbody');
    tbody.insertAdjacentHTML('afterbegin', html);
    form.reset();

    updateCountBadge();
}


export async function deleteItems(category) {
    // Delete selected items from the table
    const table = document.getElementById('items-table');
    const checkboxes = Array.from(table.querySelectorAll('input[type="checkbox"]:checked'));
    for (let checkbox of checkboxes) {
        const row = checkbox.closest('tr');
        const {id} = row.dataset;

        let url;
        if (category === 'volumes' || category === 'deposits') {
            url = `/${category}/${id}`;
        } else {
            url = `/items/${category}/${id}`;
        }
        const response = await fetch(url, {method: 'DELETE'});
        if (response.ok) {
            row.remove()
        } else {
            const error = await response.json();
            showToast(error.detail);
        }
    }

    // Uncheck all checkboxes
    const allCheckboxes = document.querySelectorAll('.checkbox');
    allCheckboxes.forEach(checkbox => checkbox.checked = false);

    swapDeleteButton();
    updateCountBadge();
}
