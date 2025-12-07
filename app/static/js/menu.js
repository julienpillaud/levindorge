import {getCategoryGroups} from "./cache/category-groups.js";

export const buildCreateDropdownMenu = async () => {
  const dropdowns = document.querySelectorAll('ul[data-id="new-article-dropdown"]')
  const categoryGroups = await getCategoryGroups();
  const html = Object.values(categoryGroups)
    .map(category => `
      <li>
        <a
          data-action="create-article"
          data-category="${category.name}"
        >
          ${category.display_name}
        </a>
      </li>
    `)
    .join('');
  dropdowns.forEach(dropdown => dropdown.innerHTML = html);

  const createArticleLinks = document.querySelectorAll("a[data-action='create-article']");
  const modal = document.getElementById("article-modal");
  createArticleLinks.forEach(link => {
    const {category} = link.dataset;
    link.addEventListener("click", () => {
      articleCreateModal(modal, category);
    })
  })
}

const articleCreateModal = async (modal, category) => {
  const modalContent = document.getElementById("article-modal-content");
  const response = await fetch(`/articles/create/${category}`);
  const html = await response.text();
  modalContent.innerHTML = html
  modal.showModal();
}
