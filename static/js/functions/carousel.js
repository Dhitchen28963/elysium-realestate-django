function updateCarousel() {
    const largeImage = document.querySelector('.large-image img');
    const thumbnails = document.querySelectorAll('.thumbnail-item img');
    let currentIndex = 0;

    function setActiveThumbnail(index) {
        thumbnails.forEach((thumbnail, i) => {
            if (i === index) {
                thumbnail.classList.add('active');
            } else {
                thumbnail.classList.remove('active');
            }
        });
    }

    function updateSmallImages() {
        const smallImages = document.querySelectorAll('.small-image-item img');
        smallImages.forEach((smallImage, i) => {
            const index = (currentIndex + i + 1) % thumbnails.length;
            smallImage.src = thumbnails[index].src;
        });
    }

    function handlePrevButtonClick() {
        const prevButton = document.querySelector('.carousel-control-prev');
        if (prevButton) {
            prevButton.addEventListener('click', function () {
                currentIndex = (currentIndex > 0) ? currentIndex - 1 : thumbnails.length - 1;
                updateCarouselState();
            });
        }
    }

    function handleNextButtonClick() {
        const nextButton = document.querySelector('.carousel-control-next');
        if (nextButton) {
            nextButton.addEventListener('click', function () {
                currentIndex = (currentIndex < thumbnails.length - 1) ? currentIndex + 1 : 0;
                updateCarouselState();
            });
        }
    }

    function handleThumbnailClick() {
        thumbnails.forEach((thumbnail, index) => {
            thumbnail.addEventListener('click', function () {
                currentIndex = index;
                updateCarouselState();
            });
        });
    }

    handlePrevButtonClick();
    handleNextButtonClick();
    handleThumbnailClick();

    function updateCarouselState() {
        if (largeImage && thumbnails.length > 0) {
            largeImage.src = thumbnails[currentIndex].src;
            setActiveThumbnail(currentIndex);
            updateSmallImages();
        }
    }

    updateCarouselState();
    setActiveThumbnail(currentIndex);
}

module.exports = {
    updateCarousel,
};
