(function() {
    function initViewer(viewer) {
        const links = viewer.querySelectorAll('nav a');
        const images = viewer.querySelectorAll('ul.image-viewer-images li');
        let currentIdx = 0;
        let autoNavTimeout = null;
        let hideHeaderTimeout = null;

        function hideImage() {
            const image = images[currentIdx];
            image.setAttribute('aria-current', 'false');
            image.classList.remove('hide-heading');
            links[currentIdx].setAttribute('aria-current', 'false');
        }

        function showImage() {
            clearTimeout(autoNavTimeout);
            clearTimeout(hideHeaderTimeout);
            const image = images[currentIdx];
            image.querySelector('div').classList.remove('minimised');
            image.setAttribute('aria-current', 'true');
            links[currentIdx].setAttribute('aria-current', 'true');
            autoNavTimeout = setTimeout(nextImage, 10000);
            hideHeaderTimeout = setTimeout(() => {
                image.classList.add('hide-heading');
            }, 5000);
        }

        function nextImage() {
            hideImage();
            currentIdx = currentIdx + 1;
            if (currentIdx >= images.length) {
                currentIdx = 0;
            }
            showImage();
        }

        for (let idx = 0; idx < images.length; idx++) {
            const image = images[idx];
            image.querySelector('a:first-child').addEventListener('click', function(ev) {
                ev.preventDefault();
                image.querySelector('div').classList.toggle('minimised');
            });
            image.querySelector('a:last-child').addEventListener('click', function(ev) {
                ev.preventDefault();
                image.querySelector('div').classList.toggle('minimised');
            });
            image.addEventListener('mouseover', function(ev) {
                clearTimeout(autoNavTimeout);
                clearTimeout(hideHeaderTimeout);
                image.classList.remove('hide-heading');
            });
            image.addEventListener('mouseout', function(ev) {
                hideHeaderTimeout = setTimeout(() => {
                    image.classList.add('hide-heading');
                }, 5000);
                autoNavTimeout = setTimeout(nextImage, 10000);
            });
        }
        for (let idx = 0; idx < links.length; idx++) {
            const link = links[idx];
            link.addEventListener('click', function(ev) {
                ev.preventDefault();
                hideImage();
                currentIdx = idx;
                showImage();
            });
        }
        showImage();
    }

    const viewers = document.querySelectorAll('.image-viewer');
    for (let idx = 0; idx < viewers.length; idx++) {
        initViewer(viewers[idx]);
    }
})();
