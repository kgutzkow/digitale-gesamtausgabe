(function() {
  let popupWrapper = null;
  let popupBox = null;
  let popupContent = null;
  let popupClose = null;
  let articleContainer = null;
  let inertable = [];
  let documentFocus = null;

  function closeFootnote() {
    history.pushState(null, null, window.location.pathname + window.location.search);
    if (popupWrapper !== null) {
      popupWrapper.classList.remove('active');
      // Remove inert maker
      for (const elem of inertable) {
        elem.removeAttribute('inert');
      }
    }
    if (documentFocus !== null) {
      documentFocus.focus();
      documentFocus = null;
    }
  }

  function showFootnote(content) {
    if (popupWrapper === null) {
      // Create the popup HTML structure
      popupWrapper = document.createElement('div');
      popupWrapper.classList.add('popup-overlay');
      document.body.appendChild(popupWrapper);
      popupBox = document.createElement('div');
      popupBox.classList.add('popup-box');
      popupWrapper.appendChild(popupBox);
      popupContent = document.createElement('div');
      popupContent.classList.add('popup-content');
      popupContent.setAttribute('role', 'note');
      popupContent.setAttribute('tabindex', '-1');
      popupBox.appendChild(popupContent);
      popupClose = document.createElement('button');
      popupClose.innerHTML = '<i class="fa-solid fa-close"/>';
      popupClose.classList.add('popup-close');
      popupBox.appendChild(popupClose);
      // Select base structural elements
      articleContainer = document.querySelector('.bd-article-container');
      inertable = document.querySelectorAll('.skip-link, .bd-header, .bd-container, .bd-footer');
      // Handle close events
      popupWrapper.addEventListener('click', closeFootnote);
      popupWrapper.addEventListener('keyup', (ev) => {
        if (ev.key == 'Escape') {
          closeFootnote();
        }
      });
      popupContent.addEventListener('click', (ev) => {
        ev.stopPropagation();
      });
    }
    // Activate the popup and its contents
    popupWrapper.classList.add('active');
    popupContent.innerHTML = content;
    popupContent.focus();
    const boundingRect = articleContainer.getBoundingClientRect();
    popupBox.setAttribute('style', 'left:' + boundingRect.left + 'px;width:calc(' + (boundingRect.right -boundingRect.left) + 'px + 1rem);');
    // Mark the main content as inert
    for (const elem of inertable) {
      elem.setAttribute('inert', '');
    }
  }

  function onHashChange() {
    if (window.location.hash !== '') {
      try {
        const annotation = document.querySelector(window.location.hash);
        if (annotation !== null && (annotation.getAttribute('data-type') === 'esv' || annotation.getAttribute('data-type') === 'footnote')) {
          showFootnote(annotation.innerHTML);
        } else {
          closeFootnote();
        }
      } catch(err) {
        console.error(err);
      }
    } else {
      closeFootnote();
    }
  }

  window.addEventListener('hashchange', onHashChange);
  window.addEventListener('DOMContentLoaded', () => {
    for (const elem of document.querySelectorAll('a[data-type="esv"], a[data-type="footnote"]')) {
      elem.addEventListener('click', () => {
        documentFocus = elem;
      })
    }
    onHashChange();
  });
})();
