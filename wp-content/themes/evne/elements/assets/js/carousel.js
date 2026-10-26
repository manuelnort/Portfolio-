( function( $ ) {
    "use strict";
    $( window ).on( 'elementor/frontend/init', function() {
        elementorFrontend.hooks.addAction( 'frontend/element_ready/pxl_post_carousel.default', function( $scope ) {
            pxl_swiper_handler($scope);
        } );
        elementorFrontend.hooks.addAction( 'frontend/element_ready/pxl_slider_carousel.default', function( $scope ) {
            pxl_swiper_handler($scope);
        } );
        elementorFrontend.hooks.addAction( 'frontend/element_ready/pxl_testimonial_carousel.default', function( $scope ) {
            pxl_swiper_handler($scope);
        } );

        elementorFrontend.hooks.addAction( 'frontend/element_ready/pxl_team_carousel.default', function( $scope ) {
            pxl_swiper_handler($scope);
        } );

        elementorFrontend.hooks.addAction( 'frontend/element_ready/pxl_partner_carousel.default', function( $scope ) {
            pxl_swiper_handler($scope);
        } );

        elementorFrontend.hooks.addAction( 'frontend/element_ready/pxl_image_carousel.default', function( $scope ) {
            pxl_swiper_handler($scope);
        } );
  
    } );
    
    const slideChangeByTestimonialUser = ($this, swiper) => {
        if(!$this.hasClass('pxl-testimonial-carousel1') ) return;
        let users = $this.find('.testimonial-content-user');
        users.each((i, user) => {
            if (i === 0) {
                $(user).addClass('active');
            }
            
            $(user).on('click', function() {
                users.removeClass('active');
                $(user).addClass('active');
                swiper.slideTo(i);
            })
        })
    }
      
     //end forflolio
    function pxl_swiper_handler($scope){
        $scope.find('.pxl-swiper-slider').each(function(index, element) {
            var $this = $(this);

            var settings = $this.find(".pxl-swiper-container").data().settings;

            var carousel_settings = {
                direction: settings['slide_direction'],
                effect: settings['slide_mode'],
                wrapperClass : 'pxl-swiper-wrapper',
                slideClass: 'pxl-swiper-slide',
                slidesPerView: settings['slides_to_show'],
                slidesPerGroup: settings['slides_to_scroll'],
                slidesPerColumn: settings['slide_percolumn'],
                spaceBetween: 0,
                observer: true,
                mousewheel: {
                    forceToAxis: true,
                    sensitivity: 3,
                    releaseOnEdges: true,
                },
                parallax: true,
                centeredSlides: true,
                observeParents: true,
                navigation: {
                    nextEl: $this.find('.pxl-swiper-arrow-next')[0],
                    prevEl: $this.find('.pxl-swiper-arrow-prev')[0],
                },
                pagination : {
                    type: settings['pagination_type'],
                    el: $this.find('.pxl-swiper-dots')[0],
                    clickable : true,
                    modifierClass: 'pxl-swiper-pagination-',
                    bulletClass : 'pxl-swiper-pagination-bullet',
                    renderCustom: function (swiper, element, current, total) {
                        return current + ' of ' + total;
                    },
                    renderBullet: function (index, className) {
                        return '<span class="' + className + '"><span></span></span>';
                    }
                },
                speed: settings['speed'],
                watchSlidesProgress: true,
                watchSlidesVisibility: true,
                breakpoints: {
                    0 : {
                        slidesPerView: settings['slides_to_show_xs'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    },
                    576 : {
                        slidesPerView: settings['slides_to_show_sm'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    },
                    768 : {
                        slidesPerView: settings['slides_to_show_md'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    },
                    992 : {
                        slidesPerView: settings['slides_to_show_lg'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    },
                    1200 : {
                        slidesPerView: settings['slides_to_show'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    },
                    1400 : {
                        slidesPerView: settings['slides_to_show_xxl'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    }
                },
                on: {
                    init: function (swiper){ 
                        var active_index = this.activeIndex;
                        var number_first = active_index < 10 ? '0' + (active_index + 1) : active_index + 1;
                        var number_total = this.slides.length < 10 ? '0' + this.slides.length : this.slides.length;
                        $('.pxl-swiper-fraction-first').html(number_first);
                        $('.pxl-swiper-fraction-last').html(number_total);
                        setBoxHeight();

                        var $hero = $this.find('.pxl-slider--hero');
                        if($hero.length){
                            $hero.find('[data-key]').each(function(idx){
                                $(this).css('z-index', idx === active_index ? '100' : '');
                                var $thisItem = $(this);
                                if(typeof gsap !== 'undefined'){
                                    gsap.set($thisItem.find('.slide-title, .link-one'), { autoAlpha: 0, y: "100%" });
                                }
                            });
                        }

                        animateSlideText($this, active_index);
                        
                        slideChangeByTestimonialUser($this, swiper);
                    },
    
                    slideChangeTransitionStart: function (swiper){
                        var activeIndex = this.activeIndex;
                        $(this.slides).each(function(index){
                            if(index == activeIndex)
                                $(this).find('.wow').removeClass('pxl-invisible').addClass('animated');
                            else
                                $(this).find('.wow').removeClass('animated').addClass('pxl-invisible');
                        });
                        
                        var $hero = $this.find('.pxl-slider--hero');
                        if($hero.length){
                            $hero.find('[data-key]').each(function(idx){
                                $(this).css('z-index', idx === activeIndex ? '100' : '');
                            });
                        }
                    },
    
                    slideChange: function (swiper) { 
                        var activeIndex = this.activeIndex; 
                        $(this.slides).each(function(index){
                            if(index == activeIndex)
                                $(this).find('.wow').removeClass('pxl-invisible').addClass('animated');
                            else
                                $(this).find('.wow').removeClass('animated').addClass('pxl-invisible');
                        });
                        
                        var number_first = activeIndex < 10 ? '0' + (activeIndex + 1) : activeIndex + 1;
                        $('.pxl-swiper-fraction-first').html(number_first);
                        //swiper images
                        if($this.hasClass('pxl-slider-carousel2')){
                            const imageCarousel = $this.find('.pxl-swiper-images').get(0).swiper;
                            imageCarousel.slideTo(activeIndex);
                            if (activeIndex === (this.slides.length - 1)) {
                                $('.circle-link')
                                    .addClass('active')
                                    .removeClass('transparent-on-dark');
                            
                                $('.slider-scroll-contact')
                                    .stop()
                                    .animate({ bottom: '40px' }, 300);
                            } else {
                                $('.circle-link')
                                    .removeClass('active')
                                    .addClass('transparent-on-dark');
                            
                                $('.slider-scroll-contact')
                                    .stop()
                                    .animate({ bottom: '-180px' }, 300);
                            }
                        }

                        if($this.hasClass('pxl-testimonial-carousel1')){
                            var users = $this.find('.testimonial-content-user');
                            users.removeClass('active');
                            $(users[activeIndex]).addClass('active');
                        }
                        
                        // Cập nhật z-index cho slider hero
                        var $hero = $this.find('.pxl-slider--hero');
                        if($hero.length){
                            $hero.find('[data-key]').each(function(idx){
                                $(this).css('z-index', idx === activeIndex ? '100' : '');
                            });
                        }
                        
                        // Chạy hiệu ứng cho text slide mới
                        animateSlideText($this, activeIndex);
                    },
    
                    sliderMove: function (swiper) { 
                        var activeIndex = this.activeIndex; 
                        $(this.slides).each(function(index){
                            if(index == activeIndex)
                                $(this).find('.wow').removeClass('pxl-invisible').addClass('animated');
                            else
                                $(this).find('.wow').removeClass('animated').addClass('pxl-invisible');
                        });
                        // Cập nhật z-index trong quá trình kéo slide nếu cần
                        var $hero = $this.find('.pxl-slider--hero');
                        if($hero.length){
                            $hero.find('[data-key]').each(function(idx){
                                $(this).css('z-index', idx === activeIndex ? '100' : '');
                            });
                        }
                    },
                }
            };

            if(settings['center_slide'] || settings['center_slide'] == 'true')
                carousel_settings['centeredSlides'] = true;

            if(settings['loop'] || settings['loop'] === 'true'){
                carousel_settings['loop'] = true;
            }

            if($this.find('.pxl-slider-carousel2').length > 0){
                carousel_settings['mousewheel'] = true;
            }

            if(settings['autoplay'] || settings['autoplay'] === 'true'){
                carousel_settings['autoplay'] = {
                    delay : settings['delay'],
                    disableOnInteraction : settings['pause_on_interaction']
                };
            } else {
                carousel_settings['autoplay'] = false;
            }
            // Creative Effect
            if(settings['creative-effect'] === 'effect1'){
                carousel_settings['creativeEffect'] = {
                    prev: {
                        shadow: true,
                        origin: "left center",
                        translate: ["-5%", 0, -200],
                        rotate: [0, 100, 0],
                    },
                    next: {
                        origin: "right center",
                        translate: ["5%", 0, -200],
                        rotate: [0, -100, 0],
                    },
                };
            }
            if(settings['slide_mode'] === 'material'){
                carousel_settings['modules'] = [EffectMaterial]
            }

            if(settings['creative-effect'] === 'effect2'){
                carousel_settings['creativeEffect'] = {
                    prev: {
                        shadow: true,
                        translate: [0, 0, -400],
                    },
                    next: {
                        translate: ["100%", 0, 0],
                    },
                };
            }

            if(settings['creative-effect'] === 'effect3'){
                carousel_settings['creativeEffect'] = {
                    prev: {
                        opacity: 0,
                    },
                    next: {
                        opacity: 0,
                    },
                };
            }

            // change_slides();
        
            // Start Swiper Thumbnail
            if ($this.find('.pxl-swiper-images').length > 0) {
                const $thumbEl = $this.find('.pxl-swiper-images');
                const thumb_settings = $thumbEl.data().settings || {};
            
                const thumb_carousel_settings = {
                    effect: "creative",
                    direction: thumb_settings['slide_direction'] || "horizontal",
                    wrapperClass: 'pxl-swiper-wrapper',
                    slideClass: 'pxl-swiper-slide',
                    spaceBetween: 0,
                    speed: 600,
                    slidesPerView: 1,
                    centeredSlides: true,
                    loop: !!thumb_settings['loop'],  
                    watchSlidesProgress: false,
                    slideToClickedSlide: false,
                    initialSlide: 2,
                    preventClicks: false,
                    parallax: true,
                    creativeEffect: {
                        perspective: true,
                        limitProgress: 6,
                        prev: {
                            translate: ["-95%", "5%", 0],
                            scale: 0.8,
                            rotate: [0, 0, -18],
                            opacity: 0.5,
                            origin: "bottom"
                        },
                        next: {
                            translate: ["95%", "5%", 0],
                            scale: 0.8,
                            rotate: [0, 0, 18],
                            opacity: 0.3,
                            origin: "bottom"
                        }
                    },
                    pagination: {
                        enabled: false,
                    },
                    breakpoints: {
                        1367: { slidesPerView: 3 },
                        992: { slidesPerView: 3 },
                        768: { slidesPerView: 1.5 },
                        576: { slidesPerView: 1 },
                    },
                };
            
                const slide_thumbs = new Swiper($thumbEl[0], thumb_carousel_settings);
            
                // Liên kết vào slider chính nếu cần
                carousel_settings['thumbs'] = { swiper: slide_thumbs };
            }  

            if($this.find('.pxl-swiper-thumbs').length > 0) {
                
                var thumb_settings = $this.find('.pxl-swiper-thumbs').data().settings;

                var thumb_carousel_settings = {
                    effect: thumb_settings['slide_mode'],
                    direction: thumb_settings['slide_direction'],
                    wrapperClass : 'pxl-swiper-wrapper',
                    slideClass: 'pxl-swiper-slide',
                    spaceBetween: 0,
                    slidesPerView: thumb_settings['slides_to_show'],
                    centeredSlides: false,
                    loop: thumb_settings['loop'],  
                    watchSlidesProgress: true,
                    slideToClickedSlide: true,
                };  

                var slide_thumbs = new Swiper($this.find('.pxl-swiper-thumbs')[0], thumb_carousel_settings);
                carousel_settings['thumbs'] = { swiper: slide_thumbs };
            }
            // End Swiper Thumbnail

            function animateSlideText($container, activeIndex) {
                var $hero = $container.find('.pxl-slider--hero');
                if($hero.length && typeof gsap !== 'undefined'){
                    var $currentSlide = $hero.find('[data-key]').eq(activeIndex);
                    var tl = gsap.timeline();
                    // Hiệu ứng cho tiêu đề
                    var $titles = $currentSlide.find('.slide-title');
                    if($titles.length){
                        tl.fromTo($titles, 
                            { autoAlpha: 0, y: "100%" },
                            { autoAlpha: 1, y: 0, duration: 0.5, ease: "power1.out", stagger: 0.03 }
                        );
                    }
                    // Hiệu ứng cho link
                    var $link = $currentSlide.find('.link-one');
                    if($link.length){
                        tl.fromTo($link, 
                            { autoAlpha: 0, y: "100%" },
                            { autoAlpha: 1, y: 0, duration: 0.3, ease: "power1.out" },
                            "-=0.2"
                        );
                    }
                }
            }

            var swiper = new Swiper($this.find(".pxl-swiper-container")[0], carousel_settings);
            slideChangeByTestimonialUser($this, swiper)
            if(settings['autoplay'] === 'true' && settings['pause_on_hover'] === 'true'){
                $( $this.find('.pxl-swiper-container') ).on({
                    mouseenter: function mouseenter() {
                        this.swiper.autoplay.stop();
                    },
                    mouseleave: function mouseleave() {
                        this.swiper.autoplay.start();
                    }
                });
            }

            function setBoxHeight() {
                var windowWidth = $(window).width();
            
                $('.swiper-vertical').each(function() {
                    var totalHeight = 0;
            
                    $(this).find('.pxl-swiper-slide.swiper-slide-visible').each(function() {
                        var slideHeight = 0;
            
                        if (windowWidth <= 1199) {
                            $(this).find('.slide-title').each(function() {
                                var innerHeight_ver = parseInt($(this).outerHeight()) || 0;
                                slideHeight += innerHeight_ver;
                            });
                        } else {
                            $(this).find('.slide-title h2').each(function() {
                                var imgHeight_ver = parseInt($(this).attr('height')) || 0;
                                slideHeight += imgHeight_ver;
                            });
                        }
            
                        var paddingTop = parseInt($(this).css('padding-top')) || 0;
                        var paddingBottom = parseInt($(this).css('padding-bottom')) || 0;
                        var paddingTop_in = parseInt($(this).find('.slide-title').css('padding-top')) || 0;
                        var paddingBottom_in = parseInt($(this).find('.slide-title').css('padding-bottom')) || 0;
                        slideHeight += paddingTop + paddingBottom + paddingTop_in + paddingBottom_in + 2;
            
                        totalHeight += slideHeight;
                    });
            
                    $(this).height(totalHeight + 'px');
                });
            }

            // Navigation Carousel
            $('.pxl-navigation-carousel').parents('.elementor-section').addClass('pxl--hide-arrow');
            setTimeout(function() {
                $('.pxl-navigation-carousel .pxl-navigation-arrow-prev').on('click', function () {
                    $(this).parents('.elementor-section').find('.pxl-swiper-arrow.pxl-swiper-arrow-prev').trigger('click');
                });
                $('.pxl-navigation-carousel .pxl-navigation-arrow-next').on('click', function () {
                    $(this).parents('.elementor-section').find('.pxl-swiper-arrow.pxl-swiper-arrow-next').trigger('click');
                });
            }, 300);

        });  

        $scope.find('.pxl-swiper-slider1').each(function(index, element) {
            var $this = $(this);

            var settings = $this.find(".pxl-swiper-container").data().settings;

            var carousel_settings = {
                direction: settings['slide_direction'],
                effect: settings['slide_mode'],
                wrapperClass : 'pxl-swiper-wrapper',
                slideClass: 'pxl-swiper-slide',
                slidesPerView: settings['slides_to_show'],
                slidesPerGroup: settings['slides_to_scroll'],
                slidesPerColumn: settings['slide_percolumn'],
                spaceBetween: 0,
                observer: true,
                mousewheel: {
                    forceToAxis: true,
                    sensitivity: 3,
                    releaseOnEdges: true,
                },
                parallax: true,
                observeParents: true,
                navigation: {
                    nextEl: $this.find('.pxl-swiper-arrow-next')[0],
                    prevEl: $this.find('.pxl-swiper-arrow-prev')[0],
                },
                pagination : {
                    type: settings['pagination_type'],
                    el: $this.find('.pxl-swiper-dots')[0],
                    clickable : true,
                    modifierClass: 'pxl-swiper-pagination-',
                    bulletClass : 'pxl-swiper-pagination-bullet',
                    renderCustom: function (swiper, element, current, total) {
                        return current + ' of ' + total;
                    },
                    renderBullet: function (index, className) {
                        return '<span class="' + className + '"><span></span></span>';
                    }
                },
                speed: settings['speed'],
                watchSlidesProgress: true,
                watchSlidesVisibility: true,
                breakpoints: {
                    0 : {
                        slidesPerView: settings['slides_to_show_xs'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    },
                    576 : {
                        slidesPerView: settings['slides_to_show_sm'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    },
                    768 : {
                        slidesPerView: settings['slides_to_show_md'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    },
                    992 : {
                        slidesPerView: settings['slides_to_show_lg'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    },
                    1200 : {
                        slidesPerView: settings['slides_to_show'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    },
                    1400 : {
                        slidesPerView: settings['slides_to_show_xxl'],
                        slidesPerGroup: settings['slides_to_scroll'],
                    }
                },
                on: {
                    init: function (swiper){ 
                        var active_index = this.activeIndex;
                        var number_first = active_index < 10 ? '0' + (active_index + 1) : active_index + 1;
                        var number_total = this.slides.length < 10 ? '0' + this.slides.length : this.slides.length;
                        $('.pxl-swiper-fraction-first').html(number_first);
                        $('.pxl-swiper-fraction-last').html(number_total);
                        setBoxHeight();

                        var $hero = $this.find('.pxl-slider--hero');
                        if ($hero.length) {
                            $hero.find('[data-key]').each(function(idx) {
                                var $thisItem = $(this);
                                var isActive = idx === active_index;

                                $thisItem.css('z-index', isActive ? '100' : '');

                                $thisItem.toggleClass('active', isActive);

                                if (typeof gsap !== 'undefined') {
                                    gsap.set($thisItem.find('.slide-title, .link-one'), { autoAlpha: 0, y: "100%" });
                                }
                            });
                        }


                        animateSlideText($this, active_index);
                        
                        slideChangeByTestimonialUser($this, swiper);
                    },
    
                    slideChangeTransitionStart: function (swiper){
                        var activeIndex = this.activeIndex;
                        $(this.slides).each(function(index){
                            if(index == activeIndex)
                                $(this).find('.wow').removeClass('pxl-invisible').addClass('animated');
                            else
                                $(this).find('.wow').removeClass('animated').addClass('pxl-invisible');
                        });
                        
                        var $hero = $this.find('.pxl-slider--hero');
                        if($hero.length){
                            $hero.find('[data-key]').each(function(idx){
                                var isActive = idx === activeIndex;
                                $(this).css('z-index', isActive ? '100' : '');
                                $(this).toggleClass('active', isActive);
                            });
                        }
                    },
    
                    slideChange: function (swiper) { 
                        var activeIndex = this.activeIndex; 
                        $(this.slides).each(function(index){
                            if(index == activeIndex)
                                $(this).find('.wow').removeClass('pxl-invisible').addClass('animated');
                            else
                                $(this).find('.wow').removeClass('animated').addClass('pxl-invisible');
                        });
                        
                        var number_first = activeIndex < 10 ? '0' + (activeIndex + 1) : activeIndex + 1;
                        $('.pxl-swiper-fraction-first').html(number_first);
                        //swiper images
                        if($this.hasClass('pxl-slider-carousel2')){
                            const imageCarousel = $this.find('.pxl-swiper-images').get(0).swiper;
                            imageCarousel.slideTo(activeIndex);
                            if (activeIndex === (this.slides.length - 1)) {
                                $('.circle-link')
                                    .addClass('active')
                                    .removeClass('transparent-on-dark');
                            
                                $('.slider-scroll-contact')
                                    .stop()
                                    .animate({ bottom: '40px' }, 300);
                            } else {
                                $('.circle-link')
                                    .removeClass('active')
                                    .addClass('transparent-on-dark');
                            
                                $('.slider-scroll-contact')
                                    .stop()
                                    .animate({ bottom: '-180px' }, 300);
                            }
                        }

                        if($this.hasClass('pxl-testimonial-carousel1')){
                            var users = $this.find('.testimonial-content-user');
                            users.removeClass('active');
                            $(users[activeIndex]).addClass('active');
                        }
                        
                        // Cập nhật z-index cho slider hero
                        var $hero = $this.find('.pxl-slider--hero');
                        if($hero.length){
                            $hero.find('[data-key]').each(function(idx){
                                var isActive = idx === activeIndex;
                                $(this).css('z-index', isActive ? '100' : '');
                                $(this).toggleClass('active', isActive);
                            });
                        }
                        
                        // Chạy hiệu ứng cho text slide mới
                        animateSlideText($this, activeIndex);
                    },
    
                    sliderMove: function (swiper) { 
                        var activeIndex = this.activeIndex; 
                        $(this.slides).each(function(index){
                            if(index == activeIndex)
                                $(this).find('.wow').removeClass('pxl-invisible').addClass('animated');
                            else
                                $(this).find('.wow').removeClass('animated').addClass('pxl-invisible');
                        });
                        // Cập nhật z-index trong quá trình kéo slide nếu cần
                        var $hero = $this.find('.pxl-slider--hero');
                        if($hero.length){
                            $hero.find('[data-key]').each(function(idx){
                                var isActive = idx === activeIndex;
                                $(this).css('z-index', isActive ? '100' : '');
                                $(this).toggleClass('active', isActive);
                            });
                        }
                    },
                }
            };

            if(settings['center_slide'] || settings['center_slide'] == 'true')
                carousel_settings['centeredSlides'] = true;

            if(settings['loop'] || settings['loop'] === 'true'){
                carousel_settings['loop'] = true;
            }

            if($this.find('.pxl-slider-carousel2').length > 0){
                carousel_settings['mousewheel'] = true;
            }

            if(settings['autoplay'] || settings['autoplay'] === 'true'){
                carousel_settings['autoplay'] = {
                    delay : settings['delay'],
                    disableOnInteraction : settings['pause_on_interaction']
                };
            } else {
                carousel_settings['autoplay'] = false;
            }
            // Creative Effect
            if(settings['creative-effect'] === 'effect1'){
                carousel_settings['creativeEffect'] = {
                    prev: {
                        shadow: true,
                        origin: "left center",
                        translate: ["-5%", 0, -200],
                        rotate: [0, 100, 0],
                    },
                    next: {
                        origin: "right center",
                        translate: ["5%", 0, -200],
                        rotate: [0, -100, 0],
                    },
                };
            }
            if(settings['slide_mode'] === 'material'){
                carousel_settings['modules'] = [EffectMaterial]
            }

            if(settings['creative-effect'] === 'effect2'){
                carousel_settings['creativeEffect'] = {
                    prev: {
                        shadow: true,
                        translate: [0, 0, -400],
                    },
                    next: {
                        translate: ["100%", 0, 0],
                    },
                };
            }

            if(settings['creative-effect'] === 'effect3'){
                carousel_settings['creativeEffect'] = {
                    prev: {
                        opacity: 0,
                    },
                    next: {
                        opacity: 0,
                    },
                };
            }

            // change_slides();
        
            // Start Swiper Thumbnail
            if ($this.find('.pxl-swiper-images').length > 0) {
                const $thumbEl = $this.find('.pxl-swiper-images');
                const thumb_settings = $thumbEl.data().settings || {};
            
                const thumb_carousel_settings = {
                    effect: "creative",
                    direction: thumb_settings['slide_direction'] || "horizontal",
                    wrapperClass: 'pxl-swiper-wrapper',
                    slideClass: 'pxl-swiper-slide',
                    spaceBetween: 0,
                    speed: 600,
                    slidesPerView: 1,
                    centeredSlides: true,
                    loop: !!thumb_settings['loop'],  
                    watchSlidesProgress: false,
                    slideToClickedSlide: false,
                    initialSlide: 2,
                    preventClicks: false,
                    parallax: true,
                    creativeEffect: {
                        perspective: true,
                        limitProgress: 6,
                        prev: {
                            translate: ["-95%", "5%", 0],
                            scale: 0.8,
                            rotate: [0, 0, -18],
                            opacity: 0.5,
                            origin: "bottom"
                        },
                        next: {
                            translate: ["95%", "5%", 0],
                            scale: 0.8,
                            rotate: [0, 0, 18],
                            opacity: 0.3,
                            origin: "bottom"
                        }
                    },
                    pagination: {
                        enabled: false,
                    },
                    breakpoints: {
                        1367: { slidesPerView: 3 },
                        992: { slidesPerView: 3 },
                        768: { slidesPerView: 1.5 },
                        576: { slidesPerView: 1 },
                    },
                };
            
                const slide_thumbs = new Swiper($thumbEl[0], thumb_carousel_settings);
            
                // Liên kết vào slider chính nếu cần
                carousel_settings['thumbs'] = { swiper: slide_thumbs };
            }  

            if($this.find('.pxl-swiper-thumbs').length > 0) {
                
                var thumb_settings = $this.find('.pxl-swiper-thumbs').data().settings;

                var thumb_carousel_settings = {
                    effect: thumb_settings['slide_mode'],
                    direction: thumb_settings['slide_direction'],
                    wrapperClass : 'pxl-swiper-wrapper',
                    slideClass: 'pxl-swiper-slide',
                    spaceBetween: 0,
                    slidesPerView: thumb_settings['slides_to_show'],
                    centeredSlides: false,
                    loop: thumb_settings['loop'],  
                    watchSlidesProgress: true,
                    slideToClickedSlide: true,
                };  

                var slide_thumbs = new Swiper($this.find('.pxl-swiper-thumbs')[0], thumb_carousel_settings);
                carousel_settings['thumbs'] = { swiper: slide_thumbs };
            }
            // End Swiper Thumbnail

            function animateSlideText($container, activeIndex) {
                var $hero = $container.find('.pxl-slider--hero');
                if($hero.length && typeof gsap !== 'undefined'){
                    var $currentSlide = $hero.find('[data-key]').eq(activeIndex);
                    var tl = gsap.timeline();
                    // Hiệu ứng cho tiêu đề
                    var $titles = $currentSlide.find('.slide-title');
                    if($titles.length){
                        tl.fromTo($titles, 
                            { autoAlpha: 0, y: "100%" },
                            { autoAlpha: 1, y: 0, duration: 0.5, ease: "power1.out", stagger: 0.03 }
                        );
                    }
                    // Hiệu ứng cho link
                    var $link = $currentSlide.find('.link-one');
                    if($link.length){
                        tl.fromTo($link, 
                            { autoAlpha: 0, y: "100%" },
                            { autoAlpha: 1, y: 0, duration: 0.3, ease: "power1.out" },
                            "-=0.2"
                        );
                    }
                }
            }

            var swiper = new Swiper($this.find(".pxl-swiper-container")[0], carousel_settings);
            slideChangeByTestimonialUser($this, swiper)
            if(settings['autoplay'] === 'true' && settings['pause_on_hover'] === 'true'){
                $( $this.find('.pxl-swiper-container') ).on({
                    mouseenter: function mouseenter() {
                        this.swiper.autoplay.stop();
                    },
                    mouseleave: function mouseleave() {
                        this.swiper.autoplay.start();
                    }
                });
            }

            function setBoxHeight() {
                var windowWidth = $(window).width();
            
                $('.swiper-vertical').each(function() {
                    var totalHeight = 0;
            
                    $(this).find('.pxl-swiper-slide.swiper-slide-visible').each(function() {
                        var slideHeight = 0;
            
                        if (windowWidth <= 1199) {
                            $(this).find('.slide-title').each(function() {
                                var innerHeight_ver = parseInt($(this).outerHeight()) || 0;
                                slideHeight += innerHeight_ver;
                            });
                        } else {
                            $(this).find('.slide-title h2').each(function() {
                                var imgHeight_ver = parseInt($(this).attr('height')) || 0;
                                slideHeight += imgHeight_ver;
                            });
                        }
            
                        var paddingTop = parseInt($(this).css('padding-top')) || 0;
                        var paddingBottom = parseInt($(this).css('padding-bottom')) || 0;
                        var paddingTop_in = parseInt($(this).find('.slide-title').css('padding-top')) || 0;
                        var paddingBottom_in = parseInt($(this).find('.slide-title').css('padding-bottom')) || 0;
                        slideHeight += paddingTop + paddingBottom + paddingTop_in + paddingBottom_in + 2;
            
                        totalHeight += slideHeight;
                    });
            
                    $(this).height(totalHeight + 'px');
                });
            }

            // Navigation Carousel
            $('.pxl-navigation-carousel').parents('.elementor-section').addClass('pxl--hide-arrow');
            setTimeout(function() {
                $('.pxl-navigation-carousel .pxl-navigation-arrow-prev').on('click', function () {
                    $(this).parents('.elementor-section').find('.pxl-swiper-arrow.pxl-swiper-arrow-prev').trigger('click');
                });
                $('.pxl-navigation-carousel .pxl-navigation-arrow-next').on('click', function () {
                    $(this).parents('.elementor-section').find('.pxl-swiper-arrow.pxl-swiper-arrow-next').trigger('click');
                });
            }, 300);

        }); 
    };
} )( jQuery );