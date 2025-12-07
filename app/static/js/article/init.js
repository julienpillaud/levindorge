export const initArticleCreate = () => {
  const createArticleLinks = document.querySelectorAll("a[data-action='create-article']");
  console.log(createArticleLinks);
  const modal = document.getElementById("article-modal");

  createArticleLinks.forEach(link => {
    const {category} = link.dataset;
    link.addEventListener("click", () => {
      articleCreateModal(modal, category);
    })
  })
}

export const articleCreateModal = (modal, category) => {
  console.log(category);
}
