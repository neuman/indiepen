;(function(){
	function setEqualHeight(columns) {
	    var tallestcolumn = 0;

	    columns.each(function() {
	        currentHeight = $(this).height();
	        if(currentHeight > tallestcolumn) {
	            tallestcolumn  = currentHeight;
	            }
	        }
	    );

		columns.height(tallestcolumn);
	}

	var delay = (function(){
		var timer = 0;
		
		return function(callback, ms){
			clearTimeout (timer);
			timer = setTimeout(callback, ms);
		};
	})();

	var app = {
		init: function(){
			// Smooth scroll
			$('a[href^="#"]').bind('click.smoothscroll',function (e) {
				e.preventDefault();

		        /*var target = this.hash,
		        $target = $(target);*/

		        $('html,body').animate({scrollTop:$(this.hash).offset().top}, 1200);
		        /*$('html, body').stop().animate({
					'scrollTop': $(target).offset().top-0
		        }, 900, 'swing', function () {
					window.location.hash = target;
				});*/
			});

			// Scrollable menu on small devices
			$(window).bind("load resize", function(){
				if($(window).height() < 400){
					$(".menu").css("overflow-y","scroll");
				}
				else {
					$(".menu").css("overflow-y","hidden");
				}
			});

			// Preload the fullscreen images
			$('.fullscreen-image:not(:first)').each(function(){
				var img = $('<img />'),
					bgSrc = $(this).css('backgroundImage').match(/[^\(]+\.(gif|jpg|jpeg|png)/g);

				if(bgSrc && bgSrc.length){
					img.attr('src', bgSrc[0]);
				}
			});

			/*$(document).on('animating.slides', function(a){
				// Fittxt
				setTimeout(function(){
					$('.fittext').fitText(0.5, { minFontSize: '40px', maxFontSize: '100px' });
					$('.hugetext').fitText(0.5, { minFontSize: '100px', maxFontSize: '180px' });
					$('.fitticker').fitText(2, { minFontSize: '16px', maxFontSize: '50px' });
				}, 100)
			});

		      $('.fittext').fitText(0.5, { minFontSize: '40px', maxFontSize: '100px' });
		      $('.hugetext').fitText(0.5, { minFontSize: '100px', maxFontSize: '180px' });
		      $('.fitticker').fitText(2, { minFontSize: '16px', maxFontSize: '50px' });*/

			// Superslides fullscreen slider
			$('#slides').superslides({
				animation: 'fade', // Choose between slide or fade
				play:4000
			});

			$('.animaze').bind('inview', function(event, visible) {
		      if (visible) {
		        $(this).stop().animate({ opacity: 1,top:'0px'},500);
		      } 
		      /* REMOVE THIS if you want to repeat the animation after the element not in view
		      else {
		        $(this).stop().animate({ opacity: 0 });
		        $(this).removeAttr('style');
		      }*/
		    });
		    $('.animaze').stop().animate({opacity:0});

			// Sudoslider services slider
			$("#services-slider").sudoSlider({
				customLink:'a.servicesLink',
				speed: 400,
				responsive: true,
				prevNext: true,
				prevHtml: '<a href="#" class="services-arrow-prev"><i class="icon-angle-left"></i></a>', 
				nextHtml: '<a href="#" class="services-arrow-next"><i class="icon-angle-right"></i></a>', 
				useCSS: true,
				continuous: true,
				updateBefore: true
			});

			// Sudoslider quote slider
			$("#quote-slider").sudoSlider({
				customLink:'a.quoteLink',
				speed: 400,
				responsive: true,
				prevNext: true, // Set this to false if you only want to show one quote
				prevHtml: '<a href="#" class="quote-arrow-prev"><i class="icon-angle-left"></i></a>', 
				nextHtml: '<a href="#" class="quote-arrow-next"><i class="icon-angle-right"></i></a>', 
				useCSS: true,
				continuous: true,
				updateBefore: true
			});

			// Sudoslider contact slider
			$("#contact-slider").sudoSlider({
				customLink:'a.contactLink',
				speed: 750,
				responsive: true,
				prevNext: false,
				useCSS: false, // Better performance for this slider
				continuous: false,
				updateBefore: true,
				effect: "fadeOutIn"
			});

			// Sudoslider portfolio slider
			$("#portfolio-slider").sudoSlider({
				customLink:'a.portfolioLink',
				speed: 400,
				numeric: true,
				responsive: true,
				prevNext: true,
				prevHtml: '<a href="#" class="portfolio-arrow-prev"><i class="icon-angle-left"></i></a>', 
				nextHtml: '<a href="#" class="portfolio-arrow-next"><i class="icon-angle-right"></i></a>', 
				useCSS: true,
				continuous: true,
				updateBefore: true
			});

	        var $container = $('.portfolioContainer');
	        $container.isotope({
	            filter: '*',
	            animationOptions: {
	                duration: 250,
	                easing: 'linear',
	                queue: false
	            }
	        });
	     	// ISOTOPE
	        $('.portfolioFilter a').click(function(){
	          var $container = $('.portfolioContainer');
	            $('.portfolioFilter .current').removeClass('current');
	            $(this).addClass('current');
	            var selector = $(this).attr('data-filter');
	            $container.isotope({
	                filter: selector,
	                animationOptions: {
	                    duration: 250,
	                    easing: 'linear',
	                    queue: false
	                }
	             });
	             return false;
	        }); 


			// Mixitup
			/*$('#portfolio-grid').mixitup({
				onMixStart: function(a){
					$('#filter-container').addClass('filtered');
				}
			});*/

			// Magnific popup for images
			 $('.popup').magnificPopup({type:'image'});
			/*
			$('.popup').magnificPopup({ 
			type: 'image',
			fixedContentPos: false,
			mainClass: 'mfp-with-zoom',
				zoom: {
					enabled: true,
					duration: 300,
					easing: 'ease-in-out', 
					opener: function(openerElement) {
						return openerElement.is('img') ? openerElement : openerElement.find('img');
					}
				}
			});

			// Magnific popup for videos
			$('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
				disableOn: 700,
				type: 'iframe',
				mainClass: 'mfp-fade',
				removalDelay: 160,
				preloader: false,
				fixedContentPos: false
			});
			*/
			//Map
		    $('#map').gmap3({
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

			// Contact Form
			$('#contact').submit(function(e) {
				e.preventDefault();

				$.ajax({
					url: 'inc/contact.php',
					data: 'name='+ escape($('#contactName').val()) +'&email=' + escape($('#contactEmail').val()) + '&phone=' + escape($('#contactPhone').val()) + '&message='+escape($('#contactMessage').val()),
					dataType: 'json',
					success: function(resp) {
						$('#contactName, #contactEmail, #contactMessage').removeClass('error');

						if(resp.success == 1){
							$('#modalContent').text(resp.message);
							$('#modal, #modalOverlay').fadeIn(500);

							$('#contactName, #contactEmail, #contactMessage, #contactPhone').val('');
						}
						else {
							if(resp.errorCode == 1){
								$('#contactName').addClass('error').focus();
							}
							else if(resp.errorCode == 2){
								$('#contactEmail').addClass('error').focus();
							}
							else if(resp.errorCode == 3){
								$('#contactMessage').addClass('error').focus();
							}	
						}					
					}
				});
			
				return false;
			});

			$('#modal').on('click touchstart', function(e){
				e.stopPropagation();
			});

			$('#modalClose, #modalOverlay').on('click touchstart', function(){
				$('#modal, #modalOverlay').fadeOut(500);
			});
		},
		domReady: function(){},
		windowLoad: function(){
			$('#loader').fadeOut(1600, "linear");
			
			$('a.popup').each(function(){
                var t = $(this),
                    img = $('<img />');
                 
                    img.attr('src', t.attr('href'));
            });
		}
	};

	app.init();
	$(function(){
		app.domReady();

		$(window).load(app.windowLoad);
	});

	$(window).resize(function() {
	    delay(function(){
	        $('.same-height').css('height','auto'); //solve for all you browser stretchers out there!
	        setEqualHeight($('.same-height'));
	    }, 500);
	});

})(jQuery)