export const initializeCheckboxes = () => {
  const ids = getCheckedArticleIds();
  // Get all checkboxes in the DOM
  const checkboxes = document.querySelectorAll("table tbody .checkbox");

  // Check the checkboxes that correspond to the stored article IDs
  checkboxes.forEach((checkbox) => {
    const articleId = checkbox.closest("tr").dataset.id;
    checkbox.checked = ids.includes(articleId);
  });

  updateDropdownVisibility();
};

// -----------------------------------------------------------------------------
export const updateCheckedArticleIds = (event) => {
  const articleId = event.target.closest("tr").dataset.id;
  const isChecked = event.target.checked;
  let ids = getCheckedArticleIds();

  if (isChecked) {
    if (!ids.includes(articleId)) {
      ids = [...ids, articleId];
    }
  } else {
    ids = ids.filter((id) => id !== articleId);
  }

  setCheckedArticleIds(ids);
};

// -----------------------------------------------------------------------------
export const getCheckedArticleIds = () =>
  JSON.parse(localStorage.getItem("checkedArticleIds") || "[]");

// -----------------------------------------------------------------------------
export const setCheckedArticleIds = (ids) => {
  localStorage.setItem("checkedArticleIds", JSON.stringify(ids));
};

// -----------------------------------------------------------------------------
export const updateDropdownVisibility = () => {
  const priceTagsDropdown = document.getElementById("price-labels-dropdown");
  const ids = getCheckedArticleIds();
  const isVisible = ids.length > 0;
  priceTagsDropdown.classList.toggle("invisible", !isVisible);
};
