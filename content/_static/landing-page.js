/**
 * Landing page animations and styling
 */
(function() {
  function sleep(length) {
    return new Promise((resolve) => {
      setTimeout(resolve, length);
    });
  }

  async function slideshow(items, interval) {
    items = new Array(...items);
    for (let idx = items.length - 1; idx > 0; idx--) {
      const randomIdx = Math.floor(Math.random() * idx);
      const tmp = items[idx];
      items[idx] = items[randomIdx];
      items[randomIdx] = tmp;
    }
    let idx = -1;
    while (true) {
      if (idx >= 0) {
        items[idx].classList.remove('current');
      }
      idx = (idx + 1) % items.length;
      items[idx].classList.add('current');
      await sleep(interval);
    }
  }

  window.addEventListener('DOMContentLoaded', () => {
    const imageContainer = document.querySelector('.gutzkow-landing-image');
    if (imageContainer !== null) {
      // Ensure the image is corretly sized
      imageContainer.setAttribute('style', 'height: ' + imageContainer.clientWidth + 'px');
      window.addEventListener('resize', () => {
        imageContainer.setAttribute('style', 'height: ' + imageContainer.clientWidth + 'px');
      });
      // Add the slideshow
      slideshow(imageContainer.querySelectorAll('img'), 30000);
    }
    const quotes = document.querySelectorAll('.gutzkow-landing-quotes blockquote');
    if (quotes.length > 0) {
      slideshow(quotes, 13000);
    }
  });
})();
