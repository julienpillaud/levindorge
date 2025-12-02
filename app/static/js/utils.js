export const showToast = (message, type = "error", timeout = 5000) => {
  const container = document.querySelector(".toast");
  const toast = document.createElement("div");
  toast.className = `alert alert-${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, timeout);
};
