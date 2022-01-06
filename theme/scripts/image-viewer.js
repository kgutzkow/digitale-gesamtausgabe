(function() {
    function initViewer(viewer) {
        const imageViewerImage = viewer.querySelector('.image-viewer-image');
        const detailsToggles = imageViewerImage.querySelectorAll('a');
        detailsToggles[0].addEventListener('click', function(ev) {
            ev.preventDefault();
            imageViewerImage.classList.toggle('minimised');
        });
        detailsToggles[1].addEventListener('click', function(ev) {
            ev.preventDefault();
            imageViewerImage.classList.toggle('minimised');
        });
    }

    const viewers = document.querySelectorAll('.image-viewer');
    for (let idx = 0; idx < viewers.length; idx++) {
        initViewer(viewers[idx]);
    }
})();
