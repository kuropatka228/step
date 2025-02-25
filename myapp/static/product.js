// продукт
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".collection").forEach((collection) => {
        let currentIndex = 0;
        const sliderContainer = collection.querySelector(".custom-slider-container");
        const slider = sliderContainer.querySelector(".custom-slider");
        const slides = slider.querySelectorAll(".custom-slide");
        const progress = sliderContainer.querySelector(".custom-progress");
        const prevButton = sliderContainer.querySelector(".custom-slider-button#custom-prev");
        const nextButton = sliderContainer.querySelector(".custom-slider-button#custom-next");

        const slidesPerView = 4;
        const totalGroups = Math.ceil(slides.length / slidesPerView);

        function showSlide(index) {
            if (index >= totalGroups) {
                currentIndex = 0;
            } else if (index < 0) {
                currentIndex = totalGroups - 1;
            } else {
                currentIndex = index;
            }

            slider.style.transform = `translateX(${-currentIndex * 100}%)`;

            if (currentIndex === 0) {
                progress.style.width = "0%";
            } else {
                progress.style.width = `${(currentIndex + 1) * (100 / totalGroups)}%`;
            }
        }

        nextButton.addEventListener("click", function () {
            showSlide(currentIndex + 1);
        });

        prevButton.addEventListener("click", function () {
            showSlide(currentIndex - 1);
        });
    });
});