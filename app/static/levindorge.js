document.addEventListener('DOMContentLoaded', () => {

    // Auto-hide alerts after 2 seconds
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            alert.animate(
                [{opacity: 0}],
                {duration: 500, easing: 'ease-out'}
            ).finished.then(() => {
                alert.style.display = 'none';
            });
        });
    }, 2000);

    const shopItems = document.querySelectorAll('.shop-item-navbar');

    shopItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const shopName = item.textContent.trim();
            const shopUserName = item.getAttribute('data-item-navbar');
            switchShop(shopName, shopUserName, item);
        });
    });

    colorStockQuantities();
    colorSellPrices();
    setupTableFilter();
    setupTableSorting();
});

function switchShop(shopName, shopUserName, item) {
    item.closest('.dropdown').querySelector('.dropdown-toggle').textContent = shopName;

    document.querySelectorAll('[data-shop]').forEach(cell => {
        cell.style.display = 'none';
    });
    document.querySelectorAll(`[data-shop="${shopUserName}"]`).forEach(cell => {
        cell.style.display = 'table-cell';
    });
}

function colorSellPrices() {
    document.querySelectorAll('tbody tr').forEach(row => {

        const shops = row.querySelectorAll('[data-shop]');
        const shopNames = [...new Set([...shops].map(s => s.dataset.shop))];

        shopNames.forEach(shopName => {
            const recommendedPriceElem = row.querySelector(`.recommended_price[data-shop="${shopName}"]`);
            const sellPriceElem = row.querySelector(`.sell_price[data-shop="${shopName}"]`);

            if (recommendedPriceElem && sellPriceElem) {
                const recommendedPrice = parseFloat(recommendedPriceElem.textContent) || 0;
                const sellPrice = parseFloat(sellPriceElem.textContent) || 0;

                sellPriceElem.style.backgroundColor = '';

                if (sellPrice > recommendedPrice) {
                    sellPriceElem.style.backgroundColor = 'darkgreen';
                } else if (sellPrice < recommendedPrice) {
                    sellPriceElem.style.backgroundColor = 'darkred';
                }
            }
        });
    });
}

function colorStockQuantities() {
    document.querySelectorAll('.stock_quantity').forEach(elem => {
        const value = parseFloat(elem.textContent) || 0;

        elem.style.backgroundColor = '';

        if (value > 0) {
            elem.style.backgroundColor = 'darkgreen';
        } else if (value < 0) {
            elem.style.backgroundColor = 'darkred';
        }
    });
}

function setupTableFilter() {
    const searchInput = document.getElementById('search');
    const table = document.querySelector('.filterable');
    if (!searchInput || !table) {
        return;
    }

    const tableRows = table.querySelectorAll('tbody tr');

    searchInput.addEventListener('keyup', (event) => {
        const searchTerm = event.target.value.toLowerCase();

        tableRows.forEach((row) => {
            const rowText = row.textContent.toLowerCase();
            row.style.display = rowText.includes(searchTerm) ? '' : 'none';
        });
    });
}

function setupTableSorting() {
    const table = document.querySelector('.sortable');
    if (!table) {
        return;
    }

    const headers = table.querySelectorAll('th:not(.not-sortable)');

    headers.forEach(th => {
        th.addEventListener('click', () => {
            sortTableByColumn(table, th);
        });
    });
}

function sortTableByColumn(table, th) {
    const tbody = table.querySelector('tbody');
    const columnIndex = Array.from(th.parentElement.children).indexOf(th);
    const currentDirection = th.dataset.direction || 'desc';
    const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
    th.dataset.direction = newDirection;

    const rows = Array.from(tbody.querySelectorAll('tr'));

    const sortedRows = rows.sort((a, b) => {
        const aText = a.children[columnIndex].textContent.trim();
        const bText = b.children[columnIndex].textContent.trim();

        const aNum = parseFloat(aText.replace(',', '.'));
        const bNum = parseFloat(bText.replace(',', '.'));

        let comparison = 0;
        if (!isNaN(aNum) && !isNaN(bNum)) {
            comparison = aNum - bNum;
        } else {
            comparison = aText.localeCompare(bText, 'fr');
        }

        return newDirection === 'asc' ? comparison : -comparison;
    });

    tbody.append(...sortedRows);
}

function toggleEmptyRows() {
    const table = document.querySelector('#priceLabelsTable');
    if (!table) {
        return;
    }

    const rows = table.querySelectorAll('tbody tr');
    const isFiltered = table.dataset.filtered === 'true';

    if (isFiltered) {
        rows.forEach(row => {
            row.style.display = '';
        });
        table.dataset.filtered = 'false';
    } else {
        rows.forEach(row => {
            const inputInLastCell = row.querySelector('td:last-child input, td:last-child select, td:last-child textarea');

            if (inputInLastCell && !inputInLastCell.value) {
                row.style.display = 'none';
            }
        });
        table.dataset.filtered = 'true';
    }
}
