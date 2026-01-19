/**
 * Synchronizes checkboxes and quantity inputs with stored article data on page load.
 */
export const initializeCheckboxes = () => {
  const articles = getCheckedArticles();
  // Get all checkboxes in the DOM
  const checkboxes = document.querySelectorAll("table tbody .checkbox");

  // Check the checkboxes that correspond to the stored article IDs
  checkboxes.forEach((checkbox) => {
    const articleId = checkbox.closest("tr").dataset.id;
    const checkedArticle = articles.find((article) => article.id === articleId);

    checkbox.checked = Boolean(checkedArticle);

    const quantityToDisplay = checkedArticle?.quantity ?? 1;
    toggleQuantityInput(checkbox, quantityToDisplay);
  });

  updateDropdownVisibility();
};

// -----------------------------------------------------------------------------
/**
 * Updates the checked articles list when a checkbox is clicked.
 */
export const updateCheckedArticles = (checkbox) => {
  const row = checkbox.closest("tr");
  const articleId = row.dataset.id;

  let articles = getCheckedArticles();

  if (checkbox.checked) {
    if (!articles.find((article) => article.id === articleId)) {
      articles.push({ id: articleId, quantity: 1 });
    }
  } else {
    articles = articles.filter((article) => article.id !== articleId);
  }

  setCheckedArticles(articles);
  updateDropdownVisibility();
  toggleQuantityInput(checkbox);
};

// -----------------------------------------------------------------------------
export const getCheckedArticles = () => {
  const data = localStorage.getItem("checkedArticles");
  return data ? JSON.parse(data) : [];
};

// -----------------------------------------------------------------------------
export const setCheckedArticles = (articles) => {
  localStorage.setItem("checkedArticles", JSON.stringify(articles));
};

// -----------------------------------------------------------------------------
export const updateDropdownVisibility = () => {
  const priceTagsDropdown = document.getElementById("price-labels-dropdown");
  if (!priceTagsDropdown) {
    return;
  }
  const checkedArticles = getCheckedArticles();
  const isVisible = checkedArticles.length > 0;
  priceTagsDropdown.classList.toggle("hidden", !isVisible);
};

// -----------------------------------------------------------------------------
export const toggleQuantityInput = (checkbox, qty = 1) => {
  const row = checkbox.closest("tr");
  const quantityInput = row.querySelector('[data-type="quantity"]');
  quantityInput.classList.toggle("invisible", !checkbox.checked);
  quantityInput.value = qty;
};

// -----------------------------------------------------------------------------
/**
 * Updates the quantity of a specific article in the storage when the input value changes.
 */
export const updateArticleQuantity = (quantityInput) => {
  const articleId = quantityInput.closest("tr").dataset.id;

  const newQuantity = parseInt(quantityInput.value, 10) || 1;
  const articles = getCheckedArticles();
  const selectedArticle = articles.find((article) => article.id === articleId);

  if (selectedArticle) {
    selectedArticle.quantity = newQuantity;
    setCheckedArticles(articles);
  }
};
