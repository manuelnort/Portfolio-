;(function ($) {

    "use strict";
    
    var pxl_scroll_top;
    var pxl_window_height;
    var pxl_window_width;
    var pxl_scroll_status = '';
    var pxl_last_scroll_top = 0;
    var pxl_post_slip = false;
    
    
    $(window).on('load', function () {
        $(".pxl-loader").addClass("is-loaded");
        $('.pxl-swiper-slider, .pxl-header-mobile-elementor').css('opacity', '1');
        $('.pxl-gallery-scroll').parents('body').addClass('body-overflow').addClass('body-visible-sm');
        pxl_window_width = $(window).width();
        pxl_window_height = $(window).height();
        evne_header_sticky();
        evne_header_mobile();
        evne_scroll_to_top();
        evne_footer_fixed();
        evne_shop_quantity();
        evne_submenu_responsive();
        evne_panel_anchor_toggle();
        evne_post_grid();
        evne_header_left_scroll();
        evne_col_offset();
        animatePinPortfolio();
        
    });

    $(window).on('scroll', function () {
        pxl_scroll_top = $(window).scrollTop();
        pxl_window_height = $(window).height();
        pxl_window_width = $(window).width();
        if (pxl_scroll_top < pxl_last_scroll_top) {
            pxl_scroll_status = 'up';
        } else {
            pxl_scroll_status = 'down';
        }
        pxl_last_scroll_top = pxl_scroll_top;
        evne_header_sticky();
        evne_scroll_to_top();
        evne_footer_fixed();
        evne_ptitle_scroll_opacity();
        evne_header_left_scroll();
        if (pxl_scroll_top < 100) {
            $('.elementor > .pin-spacer').removeClass('scroll-top-active');
        }
        
    });

    $(window).on('resize', function () {
        pxl_window_height = $(window).height();
        pxl_window_width = $(window).width();
        evne_submenu_responsive();
        evne_header_mobile();
        evne_post_grid();
        evne_col_offset();
        animatePinPortfolio();
    });

    $(document).ready(function () {
        evne_el_parallax();
        evne_backtotop_progess_bar();
        evne_type_file_upload();
        evne_zoom_point();
        evne_smother_scroll();
        hoverImageParallax();
        cursorFollow()
        initializeLinkCircle();
        observePanelPopupActive();
        initCustomScrollbar();
        // Custom Dots Slider Revolution
        setTimeout(function() {
            $('.tp-bullets.theme-style2').append('<span class="pxl-revslider-arrow-prev"></span><span class="pxl-revslider-arrow-next"></span>');
            $('.tp-bullets.theme-style2').parent().find('.tparrows').addClass('pxl-revslider-arrow-hide');

            $('.revslider-initialised').each(function () {
                $(this).find('.pxl-revslider-arrow-prev').on('click', function () {
                    $(this).parents('.revslider-initialised').find('.tp-leftarrow').trigger('click');
                });
                $(this).find('.pxl-revslider-arrow-next').on('click', function () {
                    $(this).parents('.revslider-initialised').find('.tp-rightarrow').trigger('click');
                });
            });

        }, 500);

        // Deactive Link
        $('.deactive-click a').on("click", function (e) {
            e.preventDefault();
        });

        /* Start Menu Mobile */
        $('.pxl-header-menu li.menu-item-has-children').append('<span class="pxl-menu-toggle"></span>');
        $('.pxl-menu-toggle').on('click', function () {
            if( $(this).hasClass('active')){
                $(this).closest('ul').find('.pxl-menu-toggle.active').toggleClass('active');
                $(this).closest('ul').find('.sub-menu.active').toggleClass('active').slideToggle();    
            }else{
                $(this).closest('ul').find('.pxl-menu-toggle.active').toggleClass('active');
                $(this).closest('ul').find('.sub-menu.active').toggleClass('active').slideToggle();
                $(this).toggleClass('active');
                $(this).parent().find('> .sub-menu').toggleClass('active');
                $(this).parent().find('> .sub-menu').slideToggle();
            }      
        });
    
        $("#pxl-nav-mobile, .pxl-anchor-mobile-menu").on('click', function () {
            $(this).toggleClass('active');
            $('body').toggleClass('body-overflow');
            $('.pxl-header-menu').toggleClass('active');
        });

        $(".pxl-menu-close, .pxl-header-menu-backdrop, #pxl-header-mobile .pxl-menu-primary a.is-one-page").on('click', function () {
            $(this).parents('.pxl-header-main').find('.pxl-header-menu').removeClass('active');
            $('#pxl-nav-mobile').removeClass('active');
            $('body').toggleClass('body-overflow');
        });
        /* End Menu Mobile */

        /* Menu Vertical */
        $('.pxl-nav-vertical li.menu-item-has-children > a').append('<span class="pxl-arrow-toggle"><i class="flaticon-right-arrow"></i></span>');
        $('.pxl-nav-vertical li.menu-item-has-children > a').on('click', function () {
            if( $(this).hasClass('active')){
                $(this).next().toggleClass('active').slideToggle(); 
            }else{
                $(this).closest('ul').find('.sub-menu.active').toggleClass('active').slideToggle();
                $(this).closest('ul').find('a.active').toggleClass('active');
                $(this).find('.pxl-menu-toggle.active').toggleClass('active');
                $(this).toggleClass('active');
                $(this).next().toggleClass('active').slideToggle();
            }   
        });

        /* Menu Hidden Sidebar Popup */
        $('.pxl-menu-hidden-sidebar li.menu-item-has-children > a').append('<span class="pxl-arrow-toggle"><i class="flaticon-right-arrow"></i></span>');
        $('.pxl-menu-hidden-sidebar li.menu-item-has-children > a').on('click', function () {
            if( $(this).hasClass('active')){
                $(this).next().toggleClass('active').slideToggle(); 
            }else{
                $(this).closest('ul').find('.sub-menu.active').toggleClass('active').slideToggle();
                $(this).closest('ul').find('a.active').toggleClass('active');
                $(this).find('.pxl-menu-toggle.active').toggleClass('active');
                $(this).toggleClass('active');
                $(this).next().toggleClass('active').slideToggle();
            }   
        });

        $('.pxl-menu-hidden-sidebar .pxl-menu-button').on('click', function () {
            $(this).parents('.pxl-menu-hidden-sidebar').toggleClass('active');
            $(this).parents('.pxl-menu-hidden-sidebar').removeClass('boxOut');
            $(this).parents('body').toggleClass('body-overflow');
        });
        $('.pxl-menu-popup-overlay').on('click', function () {
            $(this).parent().removeClass('active');
            $(this).parent().addClass('boxOut');
            $(this).parents('body').removeClass('body-overflow');
        });
        $('.pxl-menu-popup-close, .pxl-menu-hidden-sidebar .pxl-menu-hidden a.is-one-page').on('click', function () {
            $(this).parents('.pxl-menu-hidden-sidebar').removeClass('active');
            $(this).parents('.pxl-menu-hidden-sidebar').addClass('boxOut');
            $(this).parents('body').removeClass('body-overflow');
        });


        /* Mega Menu Max Height */
        var m_h_mega = $('li.pxl-megamenu > .sub-menu > .pxl-mega-menu-elementor').outerHeight();
        var w_h_mega = $(window).height();
        var w_h_mega_css = w_h_mega - 120;
        if(m_h_mega > w_h_mega) {
            $('li.pxl-megamenu > .sub-menu > .pxl-mega-menu-elementor').css('max-height', w_h_mega_css + 'px');
            $('li.pxl-megamenu > .sub-menu > .pxl-mega-menu-elementor').css('overflow-x', 'scroll');
        }
        /* End Mega Menu Max Height */
        //text marquee
        $(document).ready(function () {
            function startMarquee() {
                const $marqueeContainer = $(".marquee-1");
                const $marqueeContent = $(".pxl-item--text");
        
                if (!$marqueeContainer.length || !$marqueeContent.length) return;
        
                let repeatCount = 10; 
                let originalHtml = $marqueeContent.html();
                for (let i = 0; i < repeatCount; i++) {
                    $marqueeContent.append(originalHtml);
                }
        
                const speed = 100;
                const contentWidth = $marqueeContent.outerWidth();
                
                gsap.set($marqueeContent, { x: 0 });
        
                gsap.to($marqueeContent, {
                    x: `-${contentWidth / 2}px`,
                    duration: (contentWidth / 2) / speed,
                    ease: "linear",
                    repeat: -1,
                    onRepeat: function () {
                        gsap.set($marqueeContent, { x: 0 }); 
                    }
                });
            }
        
            startMarquee();
        });
        //end animate horizontal scroll
        $(document).ready(function () {
            function startMarquee() {
                const $marqueeContainer = $(".marquee-2");
                const $marqueeContent = $(".pxl-item--text");
        
                if (!$marqueeContainer.length || !$marqueeContent.length) return;
        
                let repeatCount = 10;
                let originalHtml = $marqueeContent.html();
                for (let i = 0; i < repeatCount; i++) {
                    $marqueeContent.append(originalHtml);
                }
        
                const speed = 100;
                const contentWidth = $marqueeContent.outerWidth();
                
                gsap.set($marqueeContent, { x: 0 });
        
                gsap.to($marqueeContent, {
                    x: `-${contentWidth / 2}px`,
                    duration: (contentWidth / 2) / speed,
                    ease: "linear",
                    repeat: -1,
                    onRepeat: function () {
                        gsap.set($marqueeContent, { x: 0 });
                    }
                });
            }
        
            startMarquee();
        });
        //end marquee

        /* Scroll To Top */
        $('.pxl-scroll-top').on('click', function () {
            $('html, body').animate({scrollTop: 0}, 1200);
            $(this).parents('.pxl-wapper').find('.elementor > .pin-spacer').addClass('scroll-top-active');
            return false;
        });
        
        $('.pxl-scroll-top1').on('click', function () {
            $('html, body').animate({scrollTop: 0}, 1200);
            $(this).parents('.pxl-wapper').find('.elementor > .pin-spacer').addClass('scroll-top-active');
            return false;
        });

        /* Animate Time Delay */
        $('.pxl-grid-masonry').each(function () {
            var eltime = 80;
            var elt_inner = $(this).children().length;
            var _elt = elt_inner - 1;
            $(this).find('> .pxl-grid-item > .wow').each(function (index, obj) {
                $(this).css('animation-delay', eltime + 'ms');
                if (_elt === index) {
                    eltime = 80;
                    _elt = _elt + elt_inner;
                } else {
                    eltime = eltime + 80;
                }
            });
        });

        $('.btn-text-nina').each(function () {
            var eltime = 0.045;
            var elt_inner = $(this).children().length;
            var _elt = elt_inner - 1;
            $(this).find('> .pxl--btn-text > span').each(function (index, obj) {
                $(this).css('transition-delay', eltime + 's');
                eltime = eltime + 0.045;
            });
        });

        $('.btn-text-nanuk').each(function () {
            var eltime = 0.05;
            var elt_inner = $(this).children().length;
            var _elt = elt_inner - 1;
            $(this).find('> .pxl--btn-text > span').each(function (index, obj) {
                $(this).css('animation-delay', eltime + 's');
                eltime = eltime + 0.05;
            });
        });

        $('.btn-text-smoke').each(function () {
            var eltime = 0.05;
            var elt_inner = $(this).children().length;
            var _elt = elt_inner - 1;
            $(this).find('> .pxl--btn-text > span > span > span').each(function (index, obj) {
                $(this).css('--d', eltime + 's');
                eltime = eltime + 0.05;
            });
        });

        $('.btn-text-reverse .pxl-text--front, .btn-text-reverse .pxl-text--back').each(function () {
            var eltime = 0.05;
            var elt_inner = $(this).children().length;
            var _elt = elt_inner - 1;
            $(this).find('.pxl-text--inner > span').each(function (index, obj) {
                $(this).css('transition-delay', eltime + 's');
                eltime = eltime + 0.05;
            });
        });
        
        /* End Animate Time Delay */

        /* Stat Menu Popup */
        $('.pxl-menu-hidden-1 .pxl-menu-hidden > li').on('mouseenter', function () {
            $(this).removeClass('hoverd').siblings().addClass('hoverd');
        });

        $('.pxl-menu-hidden-1 .pxl-menu-hidden > li').on('mouseleave', function () {
            $(this).removeClass('hoverd').siblings().removeClass('hoverd');
        });

        /* Menu Hidden Sidebar Popup */
        const $menuItems = $('.pxl-menu-hidden-1 li.menu-item-has-children > a');
        $menuItems.append('<span class="pxl-arrow-toggle"><i class="fas fa-chevron-right"></i></span>');

        $menuItems.on('mouseenter', function () {
            const $this = $(this);
            const $subMenu = $this.next('.sub-menu');
            const $closestUl = $this.closest('ul');
            const $activeSubMenu = $closestUl.find('.sub-menu.active');
            const $activeLink = $closestUl.find('a.active');

            if ($this.hasClass('active')) {
                return;
            }

            $activeSubMenu.removeClass('active').slideUp(300);
            $activeLink.removeClass('active');

            $this.addClass('active');
            $subMenu.addClass('active').slideDown(300);
        });

        /*Start Menu popup */
        $('.pxl-menu-hidden-1 .pxl-menu-button').on('click', function () {
            const $menuSidebar = $(this).parents('.pxl-menu-hidden-1');
            $menuSidebar.toggleClass('active');

            if ($menuSidebar.hasClass('active')) {
                const timeline = gsap.timeline({ ease: "power4.inOut" });
                // timeline.to('.pxl-menu-hidden > li', {  duration: 0.25, opacity: 1, y: -25, ease: Power2.out});
                timeline.to('.pxl-menu-popup-wrap .pxl-item--image', {  duration: 0.25, opacity: 1, x: -25, rotate: '-15deg', ease: Power2.out});
                timeline.to('.pxl-menu-popup-wrap .pxl-item-content', {  duration: 0.25, opacity: 1, x: -25, ease: Power2.out});
                $('body').toggleClass('body-overflow');
            }
        });

        $('.pxl-menu-popup-close').on('click', function () {
            const $menuSidebar = $(this).parents('.pxl-menu-hidden-1');
            const timeline = gsap.timeline({ ease: "power2.inOut" });

            $menuSidebar.removeClass('active');
            $('body').removeClass('body-overflow');

            // timeline.to('.pxl-menu-hidden > li', {  duration: 0.25, opacity: 0, y: 25, ease: Power2.out});
            timeline.to('.pxl-menu-popup-wrap .pxl-item--image', {  duration: 0.25, opacity: 0, x: 25, rotate: '0deg', ease: Power2.out});
            timeline.to('.pxl-menu-popup-wrap .pxl-item-content', {  duration: 0.25, opacity: 0, x: 25, ease: Power2.out});
        });

        /*End Menu popup */

        $('.pxl-menu-popup-overlay').on('click', function () {
            const $parent = $(this).parent();
            $parent.removeClass('active').addClass('boxOut');
            $('body').removeClass('body-overflow');
        });

        $('.pxl-menu-hidden-sidebar .pxl-menu-hidden a.is-one-page').on('click', function () {
            const $menuSidebar = $(this).parents('.pxl-menu-hidden-sidebar');
            $menuSidebar.removeClass('active').addClass('boxOut');
            $('body').removeClass('body-overflow');
        });

        const $firstMenuItem = $('.pxl-menu-hidden-sidebar li.menu-item-has-children:first-child > a');
        $firstMenuItem.addClass('active');
        $firstMenuItem.next('.sub-menu').addClass('active').slideDown();

        /* Lightbox Popup */
        setTimeout(function() {
            $('.pxl-action-popup').magnificPopup({
                type: 'iframe',
                mainClass: 'mfp-fade',
                removalDelay: 160,
                preloader: false,
                fixedContentPos: false
            });
        }, 300);

        $('.pxl-gallery-lightbox').each(function () {
            $(this).magnificPopup({
                delegate: 'a.lightbox',
                type: 'image',
                gallery: {
                    enabled: true
                },
                mainClass: 'mfp-fade',
            });
        });

        /* Page Title Parallax */
        if($('#pxl-page-title-default').hasClass('pxl--parallax')) {
            $(this).stellar();
        }

        /* Cart Sidebar Popup */
        $(".pxl-cart-sidebar-button").on('click', function () {
            $('body').addClass('body-overflow');
            $('#pxl-cart-sidebar').addClass('active');
        });
        $("#pxl-cart-sidebar .pxl-popup--overlay, #pxl-cart-sidebar .pxl-item--close, #pxl-cart-sidebar .pxl-popup--close2").on('click', function () {
            $('body').removeClass('body-overflow');
            $('#pxl-cart-sidebar').removeClass('active');
        });

        /* Start Icon Bounce */
        var boxEls = $('.el-bounce, .pxl-image-effect1, .el-effect-zigzag');
        $.each(boxEls, function(boxIndex, boxEl) {
            loopToggleClass(boxEl, 'active');
        });

        function loopToggleClass(el, toggleClass) {
            el = $(el);
            let counter = 0;
            if (el.hasClass(toggleClass)) {
                waitFor(function () {
                    counter++;
                    return counter == 2;
                }, function () {
                    counter = 0;
                    el.removeClass(toggleClass);
                    loopToggleClass(el, toggleClass);
                }, 'Deactivate', 1000);
            } else {
                waitFor(function () {
                    counter++;
                    return counter == 3;
                }, function () {
                    counter = 0;
                    el.addClass(toggleClass);
                    loopToggleClass(el, toggleClass);
                }, 'Activate', 1000);
            }
        }

        function waitFor(condition, callback, message, time) {
            if (message == null || message == '' || typeof message == 'undefined') {
                message = 'Timeout';
            }
            if (time == null || time == '' || typeof time == 'undefined') {
                time = 100;
            }
            var cond = condition();
            if (cond) {
                callback();
            } else {
                setTimeout(function() {
                    waitFor(condition, callback, message, time);
                }, time);
            }
        }
        /* End Icon Bounce */

        /* Image Effect */
        if($('.pxl-image-tilt').length){
            $('.pxl-image-tilt').parents('.elementor-top-section').addClass('pxl-image-tilt-active');
            $('.pxl-image-tilt').each(function () {
                var pxl_maxtilt = $(this).data('maxtilt'),
                    pxl_speedtilt = $(this).data('speedtilt'),
                    pxl_perspectivetilt = $(this).data('perspectivetilt');
                VanillaTilt.init(this, {
                    max: pxl_maxtilt,
                    speed: pxl_speedtilt,
                    perspective: pxl_perspectivetilt
                });
            });
        }

        /* Select Theme Style */
        $('.wpcf7-select').each(function(){
            var $this = $(this), numberOfOptions = $(this).children('option').length;
          
            $this.addClass('pxl-select-hidden'); 
            $this.wrap('<div class="pxl-select"></div>');
            $this.after('<div class="pxl-select-higthlight"></div>');

            var $styledSelect = $this.next('div.pxl-select-higthlight');
            $styledSelect.text($this.children('option').eq(0).text());
          
            var $list = $('<ul />', {
                'class': 'pxl-select-options'
            }).insertAfter($styledSelect);
          
            for (var i = 0; i < numberOfOptions; i++) {
                $('<li />', {
                    text: $this.children('option').eq(i).text(),
                    rel: $this.children('option').eq(i).val()
                }).appendTo($list);
            }
          
            var $listItems = $list.children('li');
          
            $styledSelect.on('click', function (e) {
                e.stopPropagation();
                $('div.pxl-select-higthlight.active').not(this).each(function(){
                    $(this).removeClass('active').next('ul.pxl-select-options').addClass('pxl-select-lists-hide');
                });
                $(this).toggleClass('active');
            });
          
            $listItems.on('click', function (e) {
                e.stopPropagation();
                $styledSelect.text($(this).text()).removeClass('active');
                $this.val($(this).attr('rel'));
            });
          
            $(document).on('click', function () {
                $styledSelect.removeClass('active');
            });

        });

        /* Nice Select */
        $('.woocommerce-ordering .orderby, #pxl-sidebar-area select, .variations_form.cart .variations select, .pxl-open-table select, .pxl-nice-select').each(function () {
            $(this).niceSelect();
        });

        /* Typewriter */
        if($('.pxl-title--typewriter').length) {
            function typewriterOut(elements, callback)
            {
                if (elements.length){
                    elements.eq(0).addClass('is-active');
                    elements.eq(0).delay( 3000 );
                    elements.eq(0).removeClass('is-active');
                    typewriterOut(elements.slice(1), callback);
                }
                else {
                    callback();
                }
            }

            function typewriterIn(elements, callback)
            {
                if (elements.length){
                    elements.eq(0).addClass('is-active');
                    elements.eq(0).delay( 3000 ).slideDown(3000, function(){
                        elements.eq(0).removeClass('is-active');
                        typewriterIn(elements.slice(1), callback);
                    });
                }
                else {
                    callback();
                }
            }

            function typewriterInfinite(){
                typewriterOut($('.pxl-title--typewriter .pxl-item--text'), function(){ 
                    typewriterIn($('.pxl-title--typewriter .pxl-item--text'), function(){
                        typewriterInfinite();
                    });
                });
            }
            $(function(){
                typewriterInfinite();
            });
        }
        /* End Typewriter */

        /* Section Particles */      
        setTimeout(function() {
            $(".pxl-row-particles").each(function() {
                particlesJS($(this).attr('id'), {
                  "particles": {
                    "number": {
                        "value": $(this).data('number'),
                    },
                    "color": {
                        "value": $(this).data('color')
                    },
                    "shape": {
                        "type": "circle",
                    },
                    "size": {
                        "value": $(this).data('size'),
                        "random": $(this).data('size-random'),
                    },
                    "line_linked": {
                        "enable": false,
                    },
                    "move": {
                        "enable": true,
                        "speed": 2,
                        "direction": $(this).data('move-direction'),
                        "random": true,
                        "out_mode": "out",
                    }
                  },
                  "retina_detect": true
                });
            });
        }, 400);

        /* Get checked input - Mailchimpp */
        $('.mc4wp-form input:checkbox').change(function(){
            if($(this).is(":checked")) {
                $('.mc4wp-form').addClass("pxl-input-checked");
            } else {
                $('.mc4wp-form').removeClass("pxl-input-checked");
            }
        });

        /* Scroll to content */
        $('.pxl-link-to-section .btn').on('click', function(e) {
            var id_scroll = $(this).attr('href');
            var offsetScroll = $('.pxl-header-elementor-sticky').outerHeight();
            e.preventDefault();
            $("html, body").animate({ scrollTop: $(id_scroll).offset().top - offsetScroll }, 600);
        });
        
        // Hover Overlay Effect
        $('.pxl-overlay-shake').mousemove(function(event){ 
            var offset = $(this).offset();
            var W = $(this).outerWidth();
            var X = (event.pageX - offset.left);
            var Y = (event.pageY - offset.top);
            $(this).find('.pxl-overlay--color').css({
                'top' : + Y + 'px',
                'left' : + X + 'px'
            });
        });

        // Hover Portfolio Effect
        $(".pxl-portfolio-style1 .pxl-post--inner").hover(
            function () {
                $(this).addClass("active-hover");
                $(this).removeClass("none-hover");
            },
            function () {
                $(this).removeClass("active-hover");
                $(this).addClass("none-hover");
            }
        );

        /* Custom One Page by theme */
        if($('.pxl-link-scroll1').length) {
            $('.pxl-item--onepage').on('click', function (e) {
                var _this = $(this);
                var _link = $(this).attr('href');
                var _id_data = e.currentTarget.hash;
                var _offset;
                var _data_offset = $(this).attr('data-onepage-offset');
                if(_data_offset) {
                    _offset = _data_offset;
                } else {
                    _offset = 0;
                }
                if ($(_id_data).length === 1) {
                    var _target = $(_id_data);
                    $('.pxl-onepage-active').removeClass('pxl-onepage-active');
                    _this.addClass('pxl-onepage-active');
                    $('html, body').stop().animate({ scrollTop: _target.offset().top - _offset }, 1000);   
                    return false;
                } else {
                    window.location.href = _link;
                }
                return false;
            });
            $.each($('.pxl-item--onepage'), function (index, item) {
                var target = $(item).attr('href');
                var el =  $(target);
                var _data_offset = $(item).attr('data-onepage-offset');
                var waypoint = new Waypoint({
                    element: el[0],
                    handler: function(direction) {
                        if(direction === 'down'){
                            $('.pxl-onepage-active').removeClass('pxl-onepage-active');
                            $(item).addClass('pxl-onepage-active');
                        }
                        else if(direction === 'up'){
                            var prev = $(item).parent().prev().find('.pxl-item--onepage');
                            $(item).removeClass('pxl-onepage-active');
                            if(prev.length > 0)
                                prev.addClass('pxl-onepage-active');
                        }
                    },
                    offset: _data_offset,
                });
            });
        }

        /* Item Hover Active */
        $('.pxl-hover-item').each(function () {
            $(this).hover(function () {
                $(this).parent('.pxl-hover-wrap').find('.pxl-hover-item').removeClass('pxl-active');
                $(this).addClass('pxl-active');
            });
        });

        // Active Mega Menu Hover
        $('li.pxl-megamenu').hover(function(){
                $(this).parents('.elementor-section').addClass('section-mega-active');
            },function(){
                $(this).parents('.elementor-section').removeClass('section-mega-active');
        });

    });
    
    jQuery(document).ajaxComplete(function(event, xhr, settings){
        evne_shop_quantity();
    });

    jQuery( document ).on( 'updated_wc_div', function() {
        evne_shop_quantity();
    } );
     
    /* Header Sticky */
    function evne_header_sticky() {
        if($('#pxl-header-elementor').hasClass('is-sticky')) {
            if (pxl_scroll_top > 100) {
                $('.pxl-header-elementor-sticky.pxl-sticky-stb').addClass('pxl-header-fixed');
                $('#pxl-header-mobile').addClass('pxl-header-mobile-fixed');
            } else {
                $('.pxl-header-elementor-sticky.pxl-sticky-stb').removeClass('pxl-header-fixed');
                $('#pxl-header-mobile').removeClass('pxl-header-mobile-fixed');
            }

            if (pxl_scroll_status == 'up' && pxl_scroll_top > 100) {
                $('.pxl-header-elementor-sticky.pxl-sticky-stt').addClass('pxl-header-fixed');
            } else {
                $('.pxl-header-elementor-sticky.pxl-sticky-stt').removeClass('pxl-header-fixed');
            }
        }

        $('.pxl-header-elementor-sticky').parents('body').addClass('pxl-header-sticky');
    }

    /* Header Left Scroll */
    function evne_header_left_scroll() {
        if($('.px-header--left_sidebar').hasClass('px-header-sidebar-style2')) {
            var h_section_top = $('.h5-section-top').outerHeight() + 50;
            console.log(h_section_top);
            if (pxl_scroll_top > h_section_top) {
                $('.px-header--left_sidebar').addClass('px-header--left_shadow');
            } else {
                $('.px-header--left_sidebar').removeClass('px-header--left_shadow');
            }
        }
    }

    /* Header Mobile */
    function evne_header_mobile() {
        var h_header_mobile = $('#pxl-header-elementor').outerHeight();
        if(pxl_window_width < 1199) {
            $('#pxl-header-elementor').css('min-height', h_header_mobile + 'px');
        }
    }

    /* Scroll To Top */
    function evne_scroll_to_top() {
        if (pxl_scroll_top < pxl_window_height) {
            $('.pxl-scroll-top').addClass('pxl-off').removeClass('pxl-on');
        }
        if (pxl_scroll_top > pxl_window_height) {
            $('.pxl-scroll-top').addClass('pxl-on').removeClass('pxl-off');
        }
    }
    
    const initializeLinkCircle = () => {
        const svgs = $(".circle-inner > svg");
        if (!svgs.length) return;
        let rotateValue = 0;
    
        $(window).on({
            wheel(event) {
                rotateValue += event.originalEvent.deltaY > 0 ? 10 : -10;
                svgs.css("display", "block").animate({
                    deg: rotateValue
                }, {
                    step: function(now) {
                        $(this).css("transform", `rotate(${now}deg)`);
                    },
                    duration: 50
                });
            },
            load() {
                svgs.css("display", "block").animate({
                    deg: rotateValue
                }, {
                    step: function(now) {
                        $(this).css("transform", `rotate(${now}deg)`);
                    },
                    duration: 50
                });
            }
        });
    };
    //start scroll menu
    const initCustomScrollbar = () => {
        const scrollableElements = document.querySelectorAll('.pxl-nav-menu1');
    
        scrollableElements.forEach((scrollableElement) => {
            const scrollbarContainer = scrollableElement.querySelector('.scroll-modern');
            const scrollbarThumb = scrollbarContainer.querySelector('.scroll-thumb');
    
            const updateThumbPosition = () => {
                const thumbHeight = (scrollableElement.clientHeight / scrollableElement.scrollHeight) * 100;
                const thumbTop = (scrollableElement.scrollTop / scrollableElement.scrollHeight) * 100;
                scrollbarThumb.style.height = `${thumbHeight}%`;
                scrollbarThumb.style.top = `${thumbTop}%`;
            };
    
            updateThumbPosition();
    
            scrollableElement.addEventListener('scroll', updateThumbPosition);
    
            let isDragging = false;
            let startY;
            let initialScrollTop;
    
            scrollbarThumb.addEventListener('mousedown', (e) => {
                isDragging = true;
                startY = e.clientY;
                initialScrollTop = scrollableElement.scrollTop;
                document.body.style.userSelect = 'none'; 
            });
    
            document.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                const deltaY = e.clientY - startY; 
                const scrollRatio = scrollableElement.scrollHeight / scrollableElement.clientHeight;
                scrollableElement.scrollTop = initialScrollTop + deltaY * scrollRatio;
            });
    
            document.addEventListener('mouseup', () => {
                if (isDragging) {
                    isDragging = false;
                    document.body.style.userSelect = ''; 
                }
            });
    
            if (scrollbarThumb.clientHeight < 1) {
                scrollbarThumb.style.height = '33%';
            }
    
            window.addEventListener('resize', updateThumbPosition);
        });
    };
    //end scroll menu
    
    // pin work       
    const animatePinPortfolio = () => {
        if (typeof gsap === 'undefined') return;
        gsap.registerPlugin(ScrollTrigger);
        
        const worksPin = document.querySelector(".works-pin");
        if (!worksPin) return;
        
        const cards = gsap.utils.toArray(".works-pin .single-item");
        if (!cards.length) return;
        
        const lastCardST = ScrollTrigger.create({
          trigger: cards[cards.length - 1],
          start: "center center",
        });
        
        const setStart = (window.innerHeight - cards[0].offsetHeight) / 3;
        worksPin.style.cssText = `padding-top:${setStart / 2 + 5}px;`;
        
        cards.forEach((card, index) => {
          const isLastCard = index === cards.length - 1;
          
          const target = isLastCard
            ? { scale: 1, filter: "blur(0px)" }
            : { scale: 0.8, filter: "blur(10px)" };
          
          if (!isLastCard) {
            card.style.cssText += `margin-bottom:${setStart * 2}px;`;
          }
          
          if (!isLastCard) {
            gsap.timeline({
                scrollTrigger: {
                    trigger: card,
                    pin: true,
                    pinSpacing: false,
                    start: "top 30%",
                    end: "bottom top",
                    scrub: 1,
                }
            })
            .fromTo(
                card,
                { 
                y: 0, 
                filter: "blur(0px)",
                scale: 1, 
                transformOrigin: "center center" 
                },
                { 
                y: -setStart, 
                filter: target.filter,
                scale: target.scale,
                ease: "power2.out", 
                duration: 1 
                }
            );
          } else {
            gsap.timeline({
                scrollTrigger: {
                    trigger: card,
                    pin: true,
                    pinSpacing: false,
                    start: "top 30%",
                    end: "top 30%",
                    scrub: 1,
                }
            });
        }
          const h2 = card.querySelector(".works-title h2");
          if (h2) {
            gsap.set(h2, {
                webkitTextStrokeColor: "#fff",
                webkitTextFillColor: "transparent"
            });
            gsap.timeline({
                scrollTrigger: {
                    trigger: h2,
                    start: "-10% center",
                    end: "50% center",
                    scrub: 5,
                }
            })
            .fromTo(
                h2,
                { 
                    webkitTextStrokeColor: "#fff", 
                    webkitTextFillColor: "transparent" 
                },
                { 
                    webkitTextStrokeColor: "transparent", 
                    webkitTextFillColor: "#fff",
                    ease: "power2.out",
                    duration: 1 
                }
            );
            }
        });
    };                      
    //end pin works
    

    //start horizontal scroll
    gsap.registerPlugin(ScrollTrigger);

    document.addEventListener("DOMContentLoaded", () => {
        const elements = document.querySelectorAll(".animate-horizontal-scroll");
        if (!elements.length) return;

        const windowWidth = window.innerWidth;

        if (windowWidth > 1024) {
            elements.forEach((el) => {
                const wrapper = el.querySelector(".scrolling-wrapper");
                if (!wrapper) return;

                const checkPin = el.classList.contains("pin");
                const items = wrapper.querySelectorAll(".item");
                if (!items.length) return;

                const itemsWidth = wrapper.scrollWidth;
                const containerWidth = el.clientWidth;
                const moveDistance = containerWidth - itemsWidth < 0 ? containerWidth - itemsWidth : 0;

                if (el.offsetHeight && el.offsetWidth) {
                    gsap.to(wrapper, {
                        x: moveDistance,
                        ease: "none",
                        scrollTrigger: {
                            trigger: el,
                            pin: checkPin,
                            scrub: 1,
                            pinSpacing: true,
                            start: checkPin
                                ? `top +=${(window.innerHeight - el.offsetHeight) / 2}`
                                : "top 65%",
                            end: () => `+=${Math.abs(moveDistance)}`,
                        }
                    });
                }
            });

            setTimeout(() => ScrollTrigger.refresh(), 500);
        }
    });

    //end horizontal scroll

    function hoverImageParallax() {
        const els = $('.hover-image-parallax');
        if (!els.length) return;
        $(els).on({
          mousemove(e) {
          const rect = this.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          const moveX = (x - rect.width / 2) * 0.15;
          const moveY = (y - rect.height / 2) * 0.15;
          gsap.to($(this), {
            x: moveX,
            y: moveY,
            duration: 0.25,
            ease: "none",
          });
          },
          mouseleave() {
          gsap.to($(this), {
            x: 0,
            y: 0,
            duration: 0.25,
            ease: "none",
          });
          },
        });
      }


    /* Footer Fixed */
    function evne_footer_fixed() {
        setTimeout(function(){
            var h_footer = $('.pxl-footer-fixed #pxl-footer-elementor').outerHeight() - 1;
            $('.pxl-footer-fixed #pxl-main').css('margin-bottom', h_footer + 'px');
        }, 600);
    }

    /* WooComerce Quantity */
    function evne_shop_quantity() {
        "use strict";
        $('#pxl-wapper .quantity').append('<span class="quantity-icon quantity-down pxl-icon--caretdown"></span><span class="quantity-icon quantity-up pxl-icon--caretup"></span>');
        $('.quantity-up').on('click', function () {
            $(this).parents('.quantity').find('input[type="number"]').get(0).stepUp();
            $(this).parents('.woocommerce-cart-form').find('.actions .button').removeAttr('disabled');
        });
        $('.quantity-down').on('click', function () {
            $(this).parents('.quantity').find('input[type="number"]').get(0).stepDown();
            $(this).parents('.woocommerce-cart-form').find('.actions .button').removeAttr('disabled');
        });
        $('.quantity-icon').on('click', function () {
            var quantity_number = $(this).parents('.quantity').find('input[type="number"]').val();
            var add_to_cart_button = $(this).parents( ".product, .woocommerce-product-inner" ).find(".add_to_cart_button");
            add_to_cart_button.attr('data-quantity', quantity_number);
            add_to_cart_button.attr("href", "?add-to-cart=" + add_to_cart_button.attr("data-product_id") + "&quantity=" + quantity_number);
        });
        $('.woocommerce-cart-form .actions .button').removeAttr('disabled');
    }

    /* Menu Responsive Dropdown */
    function evne_submenu_responsive() {
        var $evne_menu = $('.pxl-header-elementor-main, .pxl-header-elementor-sticky');
        $evne_menu.find('.pxl-menu-primary li').each(function () {
            var $evne_submenu = $(this).find('> ul.sub-menu');
            if ($evne_submenu.length == 1) {
                if ( ($evne_submenu.offset().left + $evne_submenu.width() + 0 ) > $(window).width()) {
                    $evne_submenu.addClass('pxl-sub-reverse');
                }
            }
        });
    }

    function evne_panel_anchor_toggle(){
        'use strict';
        $(document).on('click','.pxl-anchor-button',function(e){
            e.preventDefault();
            e.stopPropagation();
            var target = $(this).attr('data-target');
            $(this).toggleClass('open');
            $(target).toggleClass('active');
            $('body').addClass('body-overflow');
            $('.pxl-popup--conent .wow').addClass('animated').removeClass('aniOut');
            $('.pxl-popup--conent .fadeInPopup').removeClass('aniOut');
            if($(target).find('.pxl-search-form').length > 0){
                setTimeout(function(){
                    $(target).find('.pxl-search-form .pxl-search-field').focus();
                },1000);
            }
        });

        $('.pxl-anchor-button').each(function () {
            var t_target = $(this).attr('data-target');
            var t_delay = $(this).attr('data-delay-hover');
            $(t_target).find('.pxl-popup--conent').css('transition-delay', t_delay + 'ms');
            $(t_target).find('.pxl-popup--overlay').css('transition-delay', t_delay + 'ms');
        });

        $(".pxl-hidden-panel-popup .pxl-popup--overlay, .pxl-hidden-panel-popup .pxl-close-popup").on('click', function () {
            $('body').removeClass('body-overflow');
            $('.pxl-hidden-panel-popup').removeClass('active');
            $('.pxl-popup--conent .wow').addClass('aniOut').removeClass('animated');
            $('.pxl-popup--conent .fadeInPopup').addClass('aniOut');
        });

        $(".pxl-button.pxl-atc-popup").on('click', function () {
            $('body').addClass('body-overflow');
            $(this).parents('.pxl-wapper').find('.pxl-page-popup').addClass('active');
        });
        $(".pxl-popup--close").on('click', function () {
            $('body').removeClass('body-overflow');
            $(this).parent().removeClass('active');
        });

        /* Custom Theme Style */
        $('blockquote:not(.pxl-blockquote)').append('<i class="pxl-blockquote-icon flaticon-quote-1 text-gradient"></i>');
    }

    /* Post Grid */
    function evne_post_grid() {
        setTimeout(function(){
            $('.pxl-item--inner').each(function () {
                var item_w = $(this).outerWidth();
                var item_h = $(this).outerHeight();
                $(this).find('.pxl-item--imgfilter').css('width', item_w + 'px');
                $(this).find('.pxl-item--imgfilter').css('height', item_h + 'px');
            });
        }, 300);
    }

    /* Page Title Scroll Opacity */
    function evne_ptitle_scroll_opacity() {
        var divs = $('#pxl-page-title-elementor.pxl-scroll-opacity .elementor-widget'),
            limit = $('#pxl-page-title-elementor.pxl-scroll-opacity').outerHeight();
        if (pxl_scroll_top <= limit) {
            divs.css({ 'opacity' : (1 - pxl_scroll_top/limit)});
        }
    }

    $(document).on("scroll", function () {
        var $accordion = $(".pxl-accordion1");
        if ($accordion.length === 0) return;
        
        var rect = $accordion[0].getBoundingClientRect();
        var windowHeight = $(window).height();
        
        if (rect.top <= windowHeight - 600 && rect.bottom >= 0) {
            $accordion.addClass("pxl-accordion-toggle");
        } else {
            $accordion.removeClass("pxl-accordion-toggle");
        }
    });

    $(document).on("scroll", function () {
        var $accordion = $(".pxl-scroll-fill1");
        if ($accordion.length === 0) return;
        
        var rect = $accordion[0].getBoundingClientRect();
        var windowHeight = $(window).height();
        
        if (rect.top <= windowHeight - 600 && rect.bottom >= 0) {
            $accordion.addClass("scroll-class");
        } else {
            $accordion.removeClass("scroll-class");
        }
    });
    
    /* Preloader Default */
    $.fn.extend({
        jQueryImagesLoaded: function () {
          var $imgs = this.find('img[src!=""]')

          if (!$imgs.length) {
            return $.Deferred()
              .resolve()
              .promise()
          }

          var dfds = []

          $imgs.each(function () {
            var dfd = $.Deferred()
            dfds.push(dfd)
            var img = new Image()
            img.onload = function () {
              dfd.resolve()
            }
            img.onerror = function () {
              dfd.resolve()
            }
            img.src = this.src
          })

          return $.when.apply($, dfds)
        }
    })

    /* Button Parallax */
    function evne_el_parallax() {
        $('.btn-text-parallax').on('mouseenter', function() {
            $(this).addClass('hovered');
        });
        $('.btn-text-parallax').on('mouseleave', function() {
            $(this).removeClass('hovered');
        });
        $('.btn-text-parallax').on('mousemove', function(e) {
            const bounds = this.getBoundingClientRect();
            const centerX = bounds.left + bounds.width / 2;
            const centerY = bounds.top + bounds.height;
            const deltaX = Math.floor((centerX - e.clientX)) * 0.172;
            const deltaY = Math.floor((centerY - e.clientY)) * 0.273;
            $(this).find('.pxl--btn-text').css({
                transform: 'translate3d('+ deltaX * 0.32 +'px, '+ deltaY * 0.32 +'px, 0px)'
            });
            $(this).css({
                transform: 'translate3d('+ deltaX * 0.25 +'px, '+ deltaY * 0.25 +'px, 0px)'
            });
        });

        $('.el-parallax-wrap').each(function () {
            $(this).on('mouseenter', function() {
                $(this).addClass('hovered');
            });

            $(this).on('mouseleave', function() { 
                $(this).removeClass('hovered');
            });

            $(this).on('mousemove', function(e) {
                const bounds = this.getBoundingClientRect();
                const centerX = bounds.left + bounds.width / 2;
                const centerY = bounds.top + bounds.height;
                const deltaX = Math.floor((centerX - e.clientX)) * 0.222;
                const deltaY = Math.floor((centerY - e.clientY)) * 0.333;
                $(this).find('.el-parallax-item').css({
                    transform: 'translate3d('+ deltaX * 0.32 +'px, '+ deltaY * 0.32 +'px, 0px)'
                });
            });
        });

        $('.pxl-hover-parallax').on('mousemove', function(e) {
            const bounds = this.getBoundingClientRect();
            const centerX = bounds.left + bounds.width / 2;
            const centerY = bounds.top + bounds.height;
            const deltaX = Math.floor((centerX - e.clientX)) * 0.222;
            const deltaY = Math.floor((centerY - e.clientY)) * 0.333;
            $(this).find('.pxl-item-parallax').css({
                transform: 'translate3d('+ deltaX * 0.32 +'px, '+ deltaY * 0.32 +'px, 0px)'
            });
        });
    }

    /* Back To Top Progress Bar */
    function evne_backtotop_progess_bar() {
        if($('.pxl-scroll-top').length > 0) {
            var progressPath = document.querySelector('.pxl-scroll-top path');
            var pathLength = progressPath.getTotalLength();
            progressPath.style.transition = progressPath.style.WebkitTransition = 'none';
            progressPath.style.strokeDasharray = pathLength + ' ' + pathLength;
            progressPath.style.strokeDashoffset = pathLength;
            progressPath.getBoundingClientRect();
            progressPath.style.transition = progressPath.style.WebkitTransition = 'stroke-dashoffset 10ms linear';      
            var updateProgress = function () {
                var scroll = $(window).scrollTop();
                var height = $(document).height() - $(window).height();
                var progress = pathLength - (scroll * pathLength / height);
                progressPath.style.strokeDashoffset = progress;
            }
            updateProgress();
            $(window).scroll(updateProgress);   
            var offset = 50;
            var duration = 550;
            $(window).on('scroll', function() {
                if ($(this).scrollTop() > offset) {
                    $('.pxl-scroll-top').addClass('active-progress');
                } else {
                    $('.pxl-scroll-top').removeClass('active-progress');
                }
            });
        }
    }

    /* Custom Type File Upload*/
    function evne_type_file_upload() {

        var multipleSupport = typeof $('<input/>')[0].multiple !== 'undefined',
        isIE = /msie/i.test( navigator.userAgent );

        $.fn.pxl_custom_type_file = function() {

            return this.each(function() {

            var $file = $(this).addClass('pxl-file-upload-hidden'),
            $wrap = $('<div class="pxl-file-upload-wrapper">'),
            $button = $('<button type="button" class="pxl-file-upload-button">Choose File</button>'),
            $input = $('<input type="text" class="pxl-file-upload-input" placeholder="No File Choose" />'),
            $label = $('<label class="pxl-file-upload-button" for="'+ $file[0].id +'">Choose File</label>');
            $file.css({
                position: 'absolute',
                opacity: '0',
                visibility: 'hidden'
            });

            $wrap.insertAfter( $file )
            .append( $file, $input, ( isIE ? $label : $button ) );

            $file.attr('tabIndex', -1);
            $button.attr('tabIndex', -1);

            $button.on('click', function () {
                $file.focus().click();
            });

            $file.change(function() {

            var files = [], fileArr, filename;

            if ( multipleSupport ) {
                fileArr = $file[0].files;
                for ( var i = 0, len = fileArr.length; i < len; i++ ) {
                files.push( fileArr[i].name );
                }
                filename = files.join(', ');
            } else {
                filename = $file.val().split('\\').pop();
            }

            $input.val( filename )
                .attr('title', filename)
                .focus();
            });

            $input.on({
                blur: function() { $file.trigger('blur'); },
                keydown: function( e ) {
                if ( e.which === 13 ) {
                    if ( !isIE ) { 
                        $file.trigger('click'); 
                    }
                } else if ( e.which === 8 || e.which === 46 ) {
                    $file.replaceWith( $file = $file.clone( true ) );
                    $file.trigger('change');
                    $input.val('');
                } else if ( e.which === 9 ){
                    return;
                } else {
                        return false;
                    }
                }
            });

            });

        };
        $('.wpcf7-file[type=file]').pxl_custom_type_file();
    }

    // Zoom Point
    function evne_zoom_point() {
        $(".pxl-zoom-point").each(function () {

            let scaleOffset = $(this).data('offset');
            let scaleAmount = $(this).data('scale-mount');

            function scrollZoom() {
                const images = document.querySelectorAll("[data-scroll-zoom]");
                let scrollPosY = 0;
                scaleAmount = scaleAmount / 100;

                const observerConfig = {
                    rootMargin: "0% 0% 0% 0%",
                    threshold: 0
                };

                images.forEach(image => {
                    let isVisible = false;
                    const observer = new IntersectionObserver((elements, self) => {
                        elements.forEach(element => {
                            isVisible = element.isIntersecting;
                        });
                    }, observerConfig);

                    observer.observe(image);

                    image.style.transform = `scale(${1 + scaleAmount * percentageSeen(image)})`;

                    window.addEventListener("scroll", () => {
                    if (isVisible) {
                        scrollPosY = window.pageYOffset;
                        image.style.transform = `scale(${1 +
                        scaleAmount * percentageSeen(image)})`;
                    }
                    });
                });

                function percentageSeen(element) {
                    const parent = element.parentNode;
                    const viewportHeight = window.innerHeight;
                    const scrollY = window.scrollY;
                    const elPosY = parent.getBoundingClientRect().top + scrollY + scaleOffset;
                    const borderHeight = parseFloat(getComputedStyle(parent).getPropertyValue('border-bottom-width')) + parseFloat(getComputedStyle(element).getPropertyValue('border-top-width'));
                    const elHeight = parent.offsetHeight + borderHeight;

                    if (elPosY > scrollY + viewportHeight) {
                        return 0;
                    } else if (elPosY + elHeight < scrollY) {
                        return 100;
                    } else {
                        const distance = scrollY + viewportHeight - elPosY;
                        let percentage = distance / ((viewportHeight + elHeight) / 100);
                        percentage = Math.round(percentage);

                        return percentage;
                    }
                }
            }

            scrollZoom();

        });
    }
    //menu 
    const shape1 = 'M469.539032,263.986786H-0.000001L0,263.557617c66.11113,0.429169,351.088104,0.429169,469.539032,0.208344V263.986786z';
    const shape2 = 'M469.539032,263.986786H-0.000001L0,229.890961c310.649475,58.156982,255.61113-98.5,469.539032-65.062302V263.986786z';
    const shape3 = 'M469.539032,263.986786H-0.000001L0,0c226.11113,0,182.887283-0.414484,469.539032,0V263.986786z';

    function animateWave(isOpening = true) {
        const $wave = $('.wave');
        const $wavePath = $wave.find('path');
    
        if ($wave.length === 0 || $wavePath.length === 0) return;
    
        gsap.set($wave[0], { display: 'flex' });
    
        const waveTimeline = gsap.timeline({
            onComplete: () => {
                if (!isOpening) {
                    gsap.set($wave[0], { display: 'none' });
                }
            }
        });
    
        if (isOpening) {
            gsap.set($wavePath[0], { attr: { d: shape1 }, fill: '#181818' });
            waveTimeline
                .to($wavePath[0], { attr: { d: shape2 }, duration: 0.3, ease: "none" })
                .to($wavePath[0], { attr: { d: shape3 }, duration: 0.3, ease: "none" });
        } else {
            gsap.set($wavePath[0], { attr: { d: shape3 }, fill: '#181818' });
            waveTimeline
                .to($wavePath[0], { attr: { d: shape2 }, duration: 0.3, ease: "none" })
                .to($wavePath[0], { attr: { d: shape1 }, duration: 0.3, ease: "none" });
        }
    }
    
    function observePanelPopupActive() {
        const target = document.querySelector('.pxl-hidden-panel-popup');
        const $footer = $('.footer-svg');
    
        if (!target || $footer.length === 0) return;
    
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.attributeName === 'class') {
                    const isActive = $(target).hasClass('active');
    
                    if (isActive) {
                        $footer.addClass('active');
                        animateWave(true); 
                    } else {
                        animateWave(false); 
                        $footer.removeClass('active');
                    }
                }
            });
        });
    
        observer.observe(target, { attributes: true });
    }
    const target = document.querySelector('.pxl-hidden-panel-popup');
    if (!target) return;

    const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.attributeName === 'class') {
                if ($(target).hasClass('active')) {
                    $('.footer-svg').addClass('active');
                } else {
                    $('.footer-svg').removeClass('active');
                }
            }
        });
    });

    observer.observe(target, { attributes: true });

    // function isValidURL(url) {
    //     try {
    //         new URL(url);
    //         return true;
    //     } catch (_) {
    //         return false;
    //     }
    // }
    
    // function setLinks() {
    //     document.querySelectorAll('a:not(.pxl-gallery-grid1 a):not(.pxl-image-custom a):not(.pxl-video-player1 a):not(.pxl-button3 a)').forEach((link) => {
    //         link.addEventListener('click', (e) => {
    //             e.preventDefault();
    //             const url = link.href;
    
    //             if (url.includes('mailto:')) {
    //                 window.location.href = url;
    //                 return;
    //             }
    
    //             if (!isValidURL(url)) {
    //                 console.error("Invalid URL:", url);
    //                 return;
    //             }
    
    //             animateWave(true);
    
    //             setTimeout(() => {
    //                 window.location.href = url;
    //             }, 2000);
    //         });
    //     });
    // }
    // const isValidURL = (url) => {

    //     // Check if the URL is empty, contains only spaces, starts with 'javascript:', or contains spaces
    //     if (!url || url.trim() === '' || url.startsWith('javascript:') || url.includes(' ') || url.includes('#')) {
    //         return false;
    //     }
    
    //     // Regular expression to check if the URL starts with 'http://', 'https://', '/', or 'file://'
    //     const urlPattern = /^(https?:\/\/|\/|file:\/\/)/;
    //     // Test the URL against the pattern and return the result
    //     return urlPattern.test(url);
    // };

    // // Khởi chạy các chức năng khi DOM đã sẵn sàng
    // document.addEventListener('DOMContentLoaded', () => {
    //     observePanelPopupActive();
    //     setLinks();
    // });

    //emd menu

    // Zoom Point
    function evne_smother_scroll() {
        if( $( 'body').hasClass( 'body-smooth-scroll')){

            gsap.registerPlugin( ScrollTrigger, ScrollSmoother);

            ScrollSmoother.create({
              smooth: 1, 
              effects: true, 
              smoothTouch: 0.1, 
            });
        }   
    }
    function evne_col_offset() {
        var w_pxl_row_lg = ($("#pxl-main").width() - 1290) / 2;
        if (pxl_window_width > 1200) {
            $(".pxl-col-offset-right .pxl-column-inner").css(
                "padding-right",
                w_pxl_row_lg + "px"
            );
            $(".pxl-col-offset-left .pxl-column-inner").css(
                "padding-left",
                w_pxl_row_lg + "px"
            );
        }
    }

    function cursorFollow() {
    let elements = $('.pxl-portfolio-grid-layout3, .pxl-portfolio-grid-layout4, .pxl-image-custom2, .pxl-image-custom3');
    if (!elements.length) return;
    
    gsap.set('.pxl-portfolio-grid-layout3 .pxl-cursor-icon, .pxl-portfolio-grid-layout4 .pxl-cursor-icon , .pxl-image-custom2 .pxl-cursor-icon, .pxl-image-custom3 .pxl-cursor-icon', { opacity: 0, scale: 0 });

    elements.on('mousemove', function(e) {
        let offset = $(this).offset();
        let x = e.pageX - offset.left;
        let y = e.pageY - offset.top;
        const cursor = $(this).find('.pxl-cursor-icon')[0];
        gsap.to($(cursor)[0], {
            x: x,
            y: y,
            duration: 0.5,
            ease: "none",
            scale: 1,
            opacity: 1
        });
    });

    elements.on('mouseleave', function() {
        const cursor = $(this).find('.pxl-cursor-icon')[0];
        gsap.to($(cursor)[0], {
            duration: 0.5,
            ease: "none",
            scale: 0,
            opacity: 0
        });
    });
}

})(jQuery);

const shape1 = 'M469.539032,263.986786H-0.000001L0,263.557617c66.11113,0.429169,351.088104,0.429169,469.539032,0.208344V263.986786z';
const shape2 = 'M469.539032,263.986786H-0.000001L0,229.890961c310.649475,58.156982,255.61113-98.5,469.539032-65.062302V263.986786z';
const shape3 = 'M469.539032,263.986786H-0.000001L0,0c226.11113,0,182.887283-0.414484,469.539032,0V263.986786z';
let finishLoading = false;

const initializePreloader = () => {
    if (typeof gsap === 'undefined') return;

    const preloader = document.querySelector(".loader-2");
    if (!preloader) return;

    document.documentElement.style.overflow = "hidden";

    const wave = document.querySelector(".wave");

    gsap.set("#target1, #target2, #target3", {
        rotation: 40,
        svgOrigin: "83 63",
        opacity: 0
    });

    preloader.offsetHeight; 

    const tl = gsap.timeline({
        repeat: -1,
        repeatDelay: 0.1,
        defaults: { ease: "linear" }
    });

    tl.to("#target3", { attr: { y2: 25, y1: 85 }, opacity: 1 }, 0)
        .to("#target2", { attr: { y2: 42, y1: 102 }, opacity: 1 }, "+=0.1")
        .to("#target1", { attr: { y2: 58, y1: 119 }, opacity: 1 }, "+=0.1")
        .to("#target3", { attr: { y2: 85, y1: 85 }, opacity: 1, delay: 0.02 }, "+=0.1")
        .to("#target2", { attr: { y2: 102, y1: 102 }, opacity: 1 }, "+=0.1")
        .to("#target1", {
        attr: { y2: 119, y1: 119 }, opacity: 1,
        onComplete: () => {
            if (!finishLoading) return;

            tl.pause();
            preloader.style = "opacity:0;transition: opacity 1s ease;";

            setTimeout(() => {
                preloader.remove();
                document.documentElement.style.removeProperty("overflow");
            }, 1000);

            const gsap_tl = gsap.timeline({ paused: true, reversed: true });

            if (shape1 && shape2 && shape3) {
                gsap.set(wave, { display: 'flex' });
                const wavePath = wave.querySelector("path");
                if (wavePath) {
                    gsap.set(wavePath, { attr: { d: shape3 }, fill: '#181818' });

                    gsap_tl.to(wave, { display: 'flex', ease: 'none' })
                        .to(wavePath, { attr: { d: shape2 }, fill: '#181818', duration: 0.3, ease: "none", delay: 0.03 })
                        .to(wavePath, { attr: { d: shape1 }, fill: '#181818', duration: 0.02, ease: "none" })
                        .to(wave, { display: 'none', ease: 'none' });

                    gsap_tl.play();
                }
            }

            tl.kill();
        },
        });
};

// Khởi chạy ngay khi DOM sẵn sàng
document.addEventListener("DOMContentLoaded", initializePreloader);
