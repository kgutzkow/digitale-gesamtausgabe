/**
 * Improve the image gallery UX.
 *
 * Add a link around the image itself and ensure the images are square.
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
          bodyText.setAttribute('style', 'height: ' + bodyText.clientWidth + 'px');
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

/**
 * Improve the image gallery item UX.
 *
 * Ensure it is not a download link that is used.
 */
(function() {
  window.addEventListener('DOMContentLoaded', () => {
    for (const link of document.querySelectorAll('.image-gallery-item .sd-card-body a')) {
      link.removeAttribute('download');
      link.classList.remove('download');
    }
  });
})();
