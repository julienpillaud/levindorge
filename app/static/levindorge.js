document.addEventListener('DOMContentLoaded', () => {
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
