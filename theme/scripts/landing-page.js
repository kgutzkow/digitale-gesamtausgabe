(function() {
    function randomImageOrder() {
        let ids = [];
        while (ids.length < 15) {
            let random = Math.floor(Math.random() * 15) + 1;
            if (ids.indexOf(random) < 0) {
                ids.push(random);
            }
        }
        return ids.map((id) => {
            if (id < 10) {
                return 'landing_0' + id + '.jpg';
            } else {
                return 'landing_' + id + '.jpg';
            }
        });
    }

    const landingPage = document.querySelector('.landing-page');
    if (landingPage) {
        const imageContainer = landingPage.querySelector('.images');
        const imageElements = landingPage.querySelectorAll('img');
        const imageElementRoles = [0, 1];
        let imageIdx = 0;
        const images = randomImageOrder();
        let imageTimeout = -1;

        function nextImage() {
            imageElements[imageElementRoles[0]].setAttribute('src', landingPage.getAttribute('data-image-base-url') + images[imageIdx]);
            imageElements[imageElementRoles[0]].setAttribute('aria-current', 'true');
            imageIdx = imageIdx + 1;
            if (imageIdx >= 15) {
                imageIdx = 0;
            }
            imageElements[imageElementRoles[0]].setAttribute('src', landingPage.getAttribute('data-image-base-url') + images[imageIdx]);
            imageElements[imageElementRoles[1]].setAttribute('aria-current', 'false');
            imageElementRoles.reverse();
            imageTimeout = setTimeout(nextImage, 30000);
        }

        nextImage();
        imageContainer.addEventListener('mouseover', () => {
            clearTimeout(imageTimeout);
        });
        imageContainer.addEventListener('mouseout', () => {
            imageTimeout = setTimeout(nextImage, 30000);
        });

        const quoteSource = landingPage.querySelector('.quote-source');
        const leftQuote = landingPage.querySelector('.left-quote');
        const rightQuote = landingPage.querySelector('.right-quote');
        let target = 0;
        const totalQuotes = quoteSource.children.length;
        while (quoteSource.children.length > 0) {
            let randomQuote = Math.floor(Math.random() * quoteSource.children.length);
            if (target === 0 && Foundation.MediaQuery.is('large')) {
                leftQuote.appendChild(quoteSource.children[randomQuote]);
                target = 1;
            } else {
                rightQuote.appendChild(quoteSource.children[randomQuote]);
                target = 0;
            }
        }
        let quoteIdx = -1;
        let quoteTimeout = -1;

        function nextQuote() {
            if (quoteIdx !== -1) {
                if (Foundation.MediaQuery.is('large')) {
                    if (quoteIdx % 2 === 0) {
                        leftQuote.children[Math.floor(quoteIdx / 2)].setAttribute('aria-current', 'false');
                    } else {
                        rightQuote.children[Math.floor(quoteIdx / 2)].setAttribute('aria-current', 'false');
                    }
                } else {
                    rightQuote.children[quoteIdx].setAttribute('aria-current', 'false');
                }
            }
            quoteIdx++;
            if (quoteIdx >= totalQuotes) {
                quoteIdx = 0;
            }
            if (Foundation.MediaQuery.is('large')) {
                if (quoteIdx % 2 === 0) {
                    leftQuote.children[Math.floor(quoteIdx / 2)].setAttribute('aria-current', 'true');
                } else {
                    rightQuote.children[Math.floor(quoteIdx / 2)].setAttribute('aria-current', 'true');
                }
            } else {
                rightQuote.children[quoteIdx].setAttribute('aria-current', 'true');
            }

            quoteTimeout = setTimeout(nextQuote, 13000);
        }

        nextQuote();

        leftQuote.addEventListener('mouseover', () => {
            clearTimeout(quoteTimeout);
        });
        leftQuote.addEventListener('mouseout', () => {
            quoteTimeout = setTimeout(nextQuote, 13000);
        });
        rightQuote.addEventListener('mouseover', () => {
            clearTimeout(quoteTimeout);
        });
        rightQuote.addEventListener('mouseout', () => {
            quoteTimeout = setTimeout(nextQuote, 13000);
        });

        window.addEventListener('resize', () => {
            if (Foundation.MediaQuery.is('large') && leftQuote.children.length === 0) {
                for (let idx = totalQuotes - 1; idx >= 0; idx = idx - 2) {
                    rightQuote.children[idx].setAttribute('aria-current', 'false');
                    leftQuote.prepend(rightQuote.children[idx])
                }
                clearTimeout(quoteTimeout);
                nextQuote();
            } else if (!Foundation.MediaQuery.is('large') && leftQuote.children.length !== 0) {
                for (let idx = leftQuote.children.length - 1; idx >= 0; idx--) {
                    rightQuote.children[idx].setAttribute('aria-current', 'false');
                    leftQuote.children[idx].setAttribute('aria-current', 'false');
                    rightQuote.insertBefore(leftQuote.children[idx], rightQuote.children[idx]);
                }
                clearTimeout(quoteTimeout);
                nextQuote();
            }
        });
    }
})();
