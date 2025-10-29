import {swapDeleteButton} from "./utils.js";
import {createItem, deleteItems} from './api/items.js';
import {createInventory, resetStocks} from "./api/inventories.js";


export function initCreateItemListener() {
    const modalOpen = document.getElementById('item-create-button');
    const modal = document.getElementById('item-create-modal');
    const modalForm = document.getElementById('item-create-form');
    const modalClose = document.getElementById('item-create-modal-close');
    if (!modalOpen || !modal || !modalForm || !modalClose) {
        console.log('initCreateItemListener: skipping listener initialization');
        return;
    }

    modalOpen.addEventListener('click', () => {
        modal.showModal();
    });
    modalClose.addEventListener('click', () => {
        modal.close();
        modalForm.reset();
    });

    modalForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        await createItem(modalForm);
    });
}


export function initDeleteItemsListener() {
    const itemsTable = document.getElementById('items-table');
    const itemsDeleteBtn = document.getElementById('items-delete-button');
    if (!itemsTable || !itemsDeleteBtn) {
        console.log('initDeleteItemsListener: skipping listener initialization');
        return;
    }

    itemsTable.addEventListener('change', (event) => {
        if (event.target.matches('.checkbox')) {
            swapDeleteButton();
        }
    });

    const {category} = itemsDeleteBtn.dataset;
    itemsDeleteBtn.addEventListener('click', async () => {
        await deleteItems(category);
    });
}


export function initCreateInventoryListener() {
    const createInventoryBtns = document.querySelectorAll('[data-action="create-inventory"]')
    if (!createInventoryBtns.length) {
        return;
    }

    createInventoryBtns.forEach(elem => {
        elem.addEventListener('click', async (event) => {
            event.preventDefault();
            const {shop} = event.target.dataset;
            await createInventory(shop)
        });
    });
}


export function initResetStocksListener() {
    const modalOpen = document.getElementById('reset-stocks-button');
    const modal = document.getElementById('reset-stocks-modal');
    const modalForm = document.getElementById('reset-stocks-form');
    const modalClose = document.getElementById('reset-stocks-modal-close');
    if (!modalOpen || !modal || !modalForm || !modalClose) {
        console.log('initResetStocksListener: skipping listener initialization');
        return;
    }

    modalOpen.addEventListener('click', () => {
        modal.showModal();
    });
    modalClose.addEventListener('click', () => {
        modal.close();
        modalForm.reset();
    });

    modalForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        await resetStocks(modalForm);
    });
}
