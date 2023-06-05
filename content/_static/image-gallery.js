/**
 * Improve the search box UX.
 *
 * When the search box contains text, then it shows "Enter", instead of the default
 * keyboard shortcut.
 */
(function() {
    window.addEventListener('DOMContentLoaded', () => {
      for (const gallery of document.querySelectorAll('.image-gallery')) {
        for (const item of gallery.querySelectorAll('.sd-card')) {
            const footer = item.querySelector('.sd-card-footer .sd-card-text');
            footer.classList.add('text-truncate');
            const link = footer.querySelector('.sd-card-text a');
            link.setAttribute('title', link.innerText);
            const bodyText = item.querySelector('.sd-card-body .sd-card-text');
            const imgLink = document.createElement('a');
            imgLink.setAttribute('href', link.getAttribute('href'));
            imgLink.setAttribute('title', link.getAttribute('title'));
            bodyText.appendChild(imgLink);
            const image = item.querySelector('.sd-card-body img');
            imgLink.appendChild(image);
        }
      }
    });
  })();
