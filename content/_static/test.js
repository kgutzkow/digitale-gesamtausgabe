function processHash() {
  const hash = window.location.hash;
  const oldFootnote = document.querySelector('.footnote.active');
  if (oldFootnote) {
    oldFootnote.classList.remove('active');
  }
  const footnote = document.querySelector(hash + '.footnote');
  if (footnote) {
    footnote.classList.add('active');
  }
}

window.addEventListener('hashchange', processHash);
processHash();
