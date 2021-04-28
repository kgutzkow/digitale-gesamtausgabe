(function() {
    function initViewer(viewer) {
        const nav = viewer.querySelector('nav ul');
        const links = viewer.querySelectorAll('nav a');
        const images = viewer.querySelectorAll('ul.image-viewer-images li');
        let currentIdx = 0;
        let autoNavTimeout = null;
        let hideHeaderTimeout = null;

        if (window.location.hash && window.location.hash.length > 1) {
            const hashIdx = Number.parseInt(window.location.hash.substring(1));
            if (!Number.isNaN(hashIdx) && hashIdx >= 0 && hashIdx < images.length) {
                currentIdx = hashIdx;
            }
        }

        function hideImage() {
            const image = images[currentIdx];
            image.setAttribute('aria-current', 'false');
            image.classList.remove('hide-heading');
            links[currentIdx].setAttribute('aria-current', 'false');
        }

        function showImage(autoMove) {
            clearTimeout(autoNavTimeout);
            clearTimeout(hideHeaderTimeout);
            const image = images[currentIdx];
            image.setAttribute('aria-current', 'true');
            links[currentIdx].setAttribute('aria-current', 'true');
            femtoTween.tween(nav.scrollTop, links[currentIdx].parentElement.offsetTop, (value) => { nav.scrollTop = value; });
            autoNavTimeout = setTimeout(nextImage, 10000);
            image.querySelector('div').classList.remove('minimised');
            if (autoMove) {
                image.classList.add('hide-heading');
            } else {
                hideHeaderTimeout = setTimeout(() => {
                    image.classList.add('hide-heading');
                }, 5000);
            }
            window.location.hash = currentIdx;
        }

        function nextImage() {
            hideImage();
            currentIdx = currentIdx + 1;
            if (currentIdx >= images.length) {
                currentIdx = 0;
            }
            viewer.classList.add('automove');
            showImage(true);
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
                viewer.classList.remove('automove');
            });
            image.addEventListener('mouseout', function(ev) {
                hideHeaderTimeout = setTimeout(() => {
                    image.classList.add('hide-heading');
                }, 5000);
                autoNavTimeout = setTimeout(nextImage, 10000);
            });
            let startX = null;
            let startY = null;
            let offsetX = null;
            let offsetY = null;
            image.addEventListener('touchstart', function(ev) {
                if (ev.touches && ev.touches[0]) {
                    startX = ev.touches[0].clientX;
                    startY = ev.touches[0].clientY;
                }
            });
            image.addEventListener('touchmove', function(ev) {
                if (ev.touches && ev.touches[0]) {
                    offsetX = startX - ev.touches[0].clientX;
                    offsetY = startY - ev.touches[0].clientY;
                }
            });
            image.addEventListener('touchend', function(ev) {
                if (Math.abs(offsetY) < 100) {
                    if (offsetX <= -100) {
                        hideImage();
                        currentIdx = currentIdx - 1;
                        if (currentIdx < 0) {
                            currentIdx = images.length - 1;
                        }
                        viewer.classList.add('automove');
                        showImage(true);
                    } else if (offsetX >= 100) {
                        hideImage();
                        currentIdx = currentIdx + 1;
                        if (currentIdx >= images.length) {
                            currentIdx = 0;
                        }
                        viewer.classList.add('automove');
                        showImage(true);
                    }
                }
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
