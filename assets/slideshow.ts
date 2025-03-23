// assets/slideshow.ts

document.addEventListener('DOMContentLoaded', () => {
    const slider = document.getElementById('slider') as HTMLInputElement;
    const slideshow = document.getElementById('slideshow') as HTMLImageElement;

    slider.addEventListener('input', () => {
        const index = slider.value;
        slideshow.src = `/assets/image${index}.jpg`;
    });
});