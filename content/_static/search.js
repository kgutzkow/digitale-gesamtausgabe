/**
 * Improve the search box UX.
 *
 * When the search box contains text, then it shows "Enter", instead of the default
 * keyboard shortcut.
 */
(function() {
  window.addEventListener('DOMContentLoaded', () => {
    for (const searchInput of document.querySelectorAll('input[type="search"]')) {
      if (searchInput.value !== '') {
        searchInput.nextElementSibling.innerHTML = '<kbd>Enter</kbd>';
      }
      searchInput.addEventListener('keyup', (ev) => {
        if (searchInput.value !== '') {
          searchInput.nextElementSibling.innerHTML = '<kbd>Enter</kbd>';
        } else {
          searchInput.nextElementSibling.innerHTML = '<kbd class="kbd-shortcut__modifier">Ctrl</kbd>+<kbd>K</kbd>';
        }
      });
    }
  });
})();
