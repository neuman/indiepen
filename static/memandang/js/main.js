var dp = jQuery;
dp.noConflict();
dp(document).ready(function() {

    //SMOOTH SCROLL 
    dp('a[href^="#"]').bind('click.smoothscroll', function(e) {
        e.preventDefault();
        dp('html,body').animate({
            scrollTop: dp(this.hash).offset().top
        }, 1200);
    });

    //SUPER SLIDES
    dp('#home-slide').superslides({
        animation: 'fade', // You can choose either fade or slide
        play: 6000
    });

    //ANIMAZE
    dp('.animaze').bind('inview', function(event, visible) {
        if (visible) {
            dp(this).stop().animate({
                opacity: 1,
                top: '0px'
            }, 500);
        }
        /* REMOVE THIS if you want to repeat the animation after the element not in view
              else {
                $(this).stop().animate({ opacity: 0 });
                $(this).removeAttr('style');
              }*/
    });
    dp('.animaze').stop().animate({
        opacity: 0
    });

    //SERVICES
    dp("#dp-service").sudoSlider({
        customLink: 'a.servicesLink',
        responsive: true,
        speed: 350,
        prevNext: false,
        useCSS: true,
        effect: "fadeOutIn",
        continuous: true,
        updateBefore: true
    });

    //TEXT ROTATOR
    dp(".rotatez").textrotator({
        animation: "fade",
        separator: ",",
        speed: 1700
    });

    //PORTFOLIO
    dp('.portfolioContainer').mixitup({
        filterSelector: '.portfolioFilter a',
        targetSelector: '.portfolio-item',
        effects: ['fade', 'scale']
    });
    
    //QUOTE SLIDE
    dp("#quote-slider").sudoSlider({
        customLink: 'a.quoteLink',
        speed: 425,
        prevNext: true,
        responsive: true,
        prevHtml: '<a href="#" class="quote-left-indicator"><i class="icon-arrow-left"></i></a>',
        nextHtml: '<a href="#" class="quote-right-indicator"><i class="icon-arrow-right"></i></a>',
        useCSS: true,
        continuous: true,
        effect: "fadeOutIn",
        updateBefore: true
    });

    //MAGNIFIC POPUP
    dp('.popup').magnificPopup({
        type: 'image'
    });

    //PARALLAX
    dp('.parallaxize').parallax("50%", 0.3);

    // CONTACT SLIDER
    dp("#contact-slider").sudoSlider({
        customLink: 'a.contactLink',
        speed: 750,
        responsive: true,
        prevNext: false,
        useCSS: false,
        continuous: false,
        updateBefore: true,
        effect: "fadeOutIn"
    });

    //Map
    dp('#map').gmap3({
            map: {
                options: {
                    maxZoom: 15
                }
            },
            marker: {
                address: "Haltern am See, Weseler Str. 151", // PUT YOUR ADDRESS HERE
                options: {
                    icon: new google.maps.MarkerImage(
                        "http://cdn.webiconset.com/map-icons/images/pin6.png",
                        new google.maps.Size(42, 69, "px", "px")
                    )
                }
            }
        },
        "autofit");
});
dp(window).load(function() {
    dp("#lazyload").fadeOut();
});
