import {searchTable, swapDeleteButton} from "./utils.js";
import {createItem, deleteItems} from './api/items.js';


document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------------------
    // Search input
    const searchInput = document.getElementById('search');
    searchInput.addEventListener('keyup', (event) => {
        searchTable(event.target.value);
    });
    const clearSearchBtn = document.getElementById('clear-search')
    clearSearchBtn.addEventListener('click', () => {
        document.getElementById('search').value = '';
        searchTable('');
    });
    // -------------------------------------------------------------------------
    // Create item
    const itemCreateBtn = document.getElementById('item-create-button');
    const itemCreateModal = document.getElementById('item-create-modal');
    itemCreateBtn.addEventListener('click', () => {
        itemCreateModal.showModal();
    });
    const itemModalCloseBtn = document.getElementById('item-create-modal-close');
    const itemForm = document.getElementById('item-create-form');
    itemModalCloseBtn.addEventListener('click', () => {
        itemCreateModal.close();
        itemForm.reset();
    });
    itemForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        await createItem(itemForm);
    });
    // -------------------------------------------------------------------------
    // Delete items
    const itemsTable = document.getElementById('items-table');
    itemsTable.addEventListener('change', (event) => {
        if (event.target.matches('.checkbox')) {
            swapDeleteButton();
        }
    });
    const itemsDeleteBtn = document.getElementById('items-delete-button')
    const {category} = itemsDeleteBtn.dataset;
    itemsDeleteBtn.addEventListener('click', async () => {
        await deleteItems(category);
    });
    // -------------------------------------------------------------------------
});
