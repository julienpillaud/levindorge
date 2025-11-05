import {searchTable} from "./utils.js";
import {
    initCreateInventoryListener,
    initCreateItemListener,
    initDeleteItemsListener, initResetStocksListener
} from "./listener.js";
import {initToggleDeleteButton} from "./listener/global.js";
import {initDeletePriceLabels} from "./listener/price_labels.js";


document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------------------
    // Search
    const searchInputs = document.querySelectorAll('#search-mobile, #search-desktop');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', (event) => {
            searchTable(event.target.value);
        });
    });
    // Clear search
    const clearSearchButtons = document.querySelectorAll('#clear-search-mobile, #clear-search-desktop');
    clearSearchButtons.forEach(button => {
        button.addEventListener('click', () => {
            searchInputs.forEach(input => {
                input.value = '';
            });
            searchTable('');
        });
    });
    // -------------------------------------------------------------------------
    initCreateItemListener();
    initDeleteItemsListener();
    initCreateInventoryListener();
    initResetStocksListener();

    initToggleDeleteButton();
    initDeletePriceLabels();
    // -------------------------------------------------------------------------
});
