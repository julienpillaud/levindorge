export const showToast = (message, options = {}) => {
  const {
    type = "error",
    timeout = 5000,
    containerId = "main-toast-container",
  } = options;
  const container = document.getElementById(containerId);
  const toast = document.createElement("div");
  toast.className = `alert alert-${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, timeout);
};
