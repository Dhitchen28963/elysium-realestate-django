const { updateCarousel } = require('../../static/js/functions/carousel');

document.body.innerHTML = `
    <div class="carousel">
        <div class="large-image">
            <img src="" alt="large image">
        </div>
        <div class="thumbnails">
            <div class="thumbnail-item"><img src="img1.jpg" alt="thumbnail 1"></div>
            <div class="thumbnail-item"><img src="img2.jpg" alt="thumbnail 2"></div>
            <div class="thumbnail-item"><img src="img3.jpg" alt="thumbnail 3"></div>
        </div>
        <div class="small-images">
            <div class="small-image-item"><img src="" alt="small image 1"></div>
            <div class="small-image-item"><img src="" alt="small image 2"></div>
            <div class="small-image-item"><img src="" alt="small image 3"></div>
        </div>
        <button class="carousel-control-prev">Prev</button>
        <button class="carousel-control-next">Next</button>
    </div>
`;

describe('updateCarousel', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        updateCarousel();
    });

    test('should initialize the carousel with the first thumbnail as the active image', () => {
        const largeImage = document.querySelector('.large-image img');
        expect(largeImage.src).toContain('img1.jpg');
        const activeThumbnail = document.querySelector('.thumbnail-item img.active');
        expect(activeThumbnail.src).toContain('img1.jpg');
    });

    test('should update the large image and active thumbnail on next button click', () => {
        const nextButton = document.querySelector('.carousel-control-next');
        nextButton.click();
        const largeImage = document.querySelector('.large-image img');
        expect(largeImage.src).toContain('img2.jpg');
        const activeThumbnail = document.querySelector('.thumbnail-item img.active');
        expect(activeThumbnail.src).toContain('img2.jpg');
    });

    test('should update the large image and active thumbnail on prev button click', () => {
        const nextButton = document.querySelector('.carousel-control-next');
        nextButton.click();
        nextButton.click();
        const prevButton = document.querySelector('.carousel-control-prev');
        prevButton.click();
        const largeImage = document.querySelector('.large-image img');
        expect(largeImage.src).toContain('img2.jpg');
        const activeThumbnail = document.querySelector('.thumbnail-item img.active');
        expect(activeThumbnail.src).toContain('img2.jpg');
    });

    test('should update the large image and active thumbnail on thumbnail click', () => {
        const thumbnail = document.querySelectorAll('.thumbnail-item img')[2];
        thumbnail.click();
        const largeImage = document.querySelector('.large-image img');
        expect(largeImage.src).toContain('img3.jpg');
        const activeThumbnail = document.querySelector('.thumbnail-item img.active');
        expect(activeThumbnail.src).toContain('img3.jpg');
    });
});
