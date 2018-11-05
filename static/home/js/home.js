$(function () {
    // 隐藏滚动条后，导致页面过大的一个处理
    $('.home').width(innerWidth)

    new Swiper('#topSwiper', {
        pagination: '.swiper-pagination',
        // nextButton: '.swiper-button-next',
        // prevButton: '.swiper-button-prev',

        //使能点击
        paginationClickable: true,
        //中间间隔
        spaceBetween: 5,

        centeredSlides: true,
        autoplay: 2500,
        autoplayDisableOnInteraction: false,
        loop: true
    });


     new Swiper('#mustbuySwiper', {
        slidesPerView: 3,
        spaceBetween: 10,
         loop: true
    });
})