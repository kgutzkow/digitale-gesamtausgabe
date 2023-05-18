(function() {
  let popupWrapper = null;
  let popupContent = null;
  let articleContainer = null;

  function showTooltip(ev) {
    ev.preventDefault();
    try {
      const content = document.querySelector(ev.target.getAttribute('href'));
      if (content) {
        if (popupWrapper === null) {
          // Create the popup HTML structure
          popupWrapper = document.createElement('div');
          popupWrapper.classList.add('popup-overlay');
          document.body.appendChild(popupWrapper);
          popupContent = document.createElement('div');
          popupContent.classList.add('popup-content');
          popupWrapper.appendChild(popupContent);
          articleContainer = document.querySelector('.bd-article-container');
          // Handle close events
          popupWrapper.addEventListener('click', () => {
            popupWrapper.classList.remove('active');
          });
          popupContent.addEventListener('click', (ev) => {
            ev.stopPropagation();
          });
        }
        // Activate the popup and its contents
        popupWrapper.classList.add('active');
        popupContent.innerHTML = content.innerHTML;
        const boundingRect = articleContainer.getBoundingClientRect();
        popupContent.setAttribute('style', 'left:' + boundingRect.left + 'px;width:calc(' + (boundingRect.right -boundingRect.left) + 'px + 1rem);');
        // Set event listeners on the children
        for (let esvLink of popupContent.querySelectorAll('a.reference.esv')) {
          esvLink.addEventListener('click', showTooltip);
        }
      }
    } catch(err) {
      console.error(err);
    }
  }

  // Handle reference clicks
  window.addEventListener('DOMContentLoaded', () => {
    for (let esvLink of document.querySelectorAll('a.reference.esv')) {
      esvLink.addEventListener('click', showTooltip);
    }
  });
})();
