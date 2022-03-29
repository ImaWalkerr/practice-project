const slider = document.querySelector('.swiper-container');

let mySlider = new Swiper(slider, {
    slidesPerView: 5,
    spaceBetween: 15,
    mousewheel: {
        enabled: true,
        sensitivity: 5.5,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
})
