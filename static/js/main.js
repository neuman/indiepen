/*global requirejs: false*/
requirejs.config({
  paths: {
    jquery: "../bower_components/jquery/jquery",
    requirejs: "../bower_components/requirejs/require",
    "jquery.bootstrap": "../bower_components/bootstrap/dist/js/bootstrap",
    dropzone: "../bower_components/dropzone/downloads/dropzone.min",
    imagesloaded: "../bower_components/imagesloaded/imagesloaded",
    masonry: "../bower_components/masonry/masonry",
    eventEmitter: "../bower_components/eventEmitter",
    eventie: "../bower_components/eventie",
    "get-size": "../bower_components/get-size",
    "jquery-bridget": "../bower_components/jquery-bridget/jquery.bridget",
    item: "../bower_components/outlayer/item",
    outlayer: "../bower_components/outlayer",
    "matches-selector": "../bower_components/matches-selector",
    "doc-ready": "../bower_components/doc-ready",
    "get-style-property": "../bower_components/get-style-property",
    "jquery.commonscripts": "../js/common-scripts",
    "jquery.nicescroll": "../bower_components/jquery.nicescroll/jquery.nicescroll",
    "stripe": "https://js.stripe.com/v2/?1",
    "jquery.jquery-ui": "../bower_components/jquery-ui/ui/minified/jquery-ui.min",
    "videojs": "../bower_components/videojs/dist/video-js/video",
    "jquery.superslides":"../bower_components/superslides/dist/jquery.superslides.js",
  },
  shim: {
    "jquery.bootstrap": {
      deps: ["jquery"]
    },
    "jquery.commonscripts": {
      deps: ["jquery"]
    },
    "jquery.nicescroll": {
      deps: ["jquery"]
    },
    "stripe": {
      exports: 'Stripe'
    },
    "jquery.jquery-ui": {
      deps: ["jquery"]
    },
  }

});
console.log('requiring stuff');

requirejs(["jquery","dropzone","imagesloaded","masonry","jquery.bootstrap","jquery.commonscripts","jquery.nicescroll","stripe", "jquery.jquery-ui", "videojs"], function($, Dropzone, imagesLoaded, Masonry, bootstrap, commonscripts, nicescroll, Stripe, ui, videojs) {
  console.log($);
  console.log(Stripe);

      //owl carousel
$(window).load(function() {
    $("#lazyload").fadeOut();
});

      $(document).ready(function() {

        //for testing ajax response
        //$.get(window.location.pathname, function(data) {
         //console.log("DATA ARRIVED");
         //console.log(data);
        //});

          /*$("#owl-demo").owlCarousel({
              navigation : true,
              slideSpeed : 300,
              paginationSpeed : 400,
              singleItem : true

            });
*/
jQuery.fn.doesExist = function(){
  return jQuery(this).length > 0;
};



    //SMOOTH SCROLL 
    $('a[href^="#"]').bind('click.smoothscroll', function(e) {
        e.preventDefault();
        $('html,body').animate({
            scrollTop: $(this.hash).offset().top
        }, 1200);
    });

    //SUPER SLIDES
    $('#home-slide').superslides({
        animation: 'fade', // You can choose either fade or slide
    });

    //ANIMAZE
    $('.animaze').bind('inview', function(event, visible) {
        if (visible) {
            $(this).stop().animate({
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
    $('.animaze').stop().animate({
        opacity: 0
    });

    //SERVICES
    $("#$-service").sudoSlider({
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
    $(".rotatez").textrotator({
        animation: "fade",
        separator: ",",
        speed: 1700
    });

    //PORTFOLIO
    $('.portfolioContainer').mixitup({
        filterSelector: '.portfolioFilter a',
        targetSelector: '.portfolio-item',
        effects: ['fade', 'scale']
    });
    
    //QUOTE SLIDE
    $("#quote-slider").sudoSlider({
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
    $('.popup').magnificPopup({
        type: 'image'
    });

    //PARALLAX
    $('.parallaxize').parallax("50%", 0.3);

    // CONTACT SLIDER
    $("#contact-slider").sudoSlider({
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


if($('.dropzone').doesExist()){
  new Dropzone(".dropzone", { 
    paramName: "original_file"
  });
};

      //bootstrapify images included in markdown
      $('img:not([class])').addClass('img-thumbnail');
      //custom select box

      //stripe stuff
      Stripe.setPublishableKey('pk_test_gQYGUBwsm6rzvoSxBpSKbDC2');
      jQuery(function($) {
        $('#payment-form').submit(function(event) {
          var $form = $(this);

          // Disable the submit button to prevent repeated clicks
          $form.find('button').prop('disabled', true);

          Stripe.card.createToken($form, stripeResponseHandler);

          // Prevent the form from submitting with the default action
          return false;
        });
      });

      var stripeResponseHandler = function(status, response) {
        var $form = $('#payment-form');

        if (response.error) {
          // Show the errors on the form
          $form.find('.payment-errors').text(response.error.message);
          $form.find('button').prop('disabled', false);
        } else {
          // token contains id, last4, and card type
          var token = response.id;
          // Insert the token into the form so it gets submitted to the server
          console.log("token: "+token)
          $form.append($('<input type="hidden" name="stripeToken" />').val(token));
          // and submit
          $form.get(0).submit();
        }
      };

      //$(function(){
      //    $('select.styled').customSelect();
      //});



$(function() {
  $( "#sortable" ).sortable({
    handle: '.handle',
    cursor: 'move',
    update: function(event, ui) {
     console.log("updated");
     var orderstring_ids = [];
    $(".media-representation").each(function( index ) {
      console.log( index + ": " + $( this ).data("pk") );
      orderstring_ids.push($(this).data("pk"));
    });
    var orderstring = "["+orderstring_ids.join(",")+"]"
    console.log(orderstring);
    $.post( window.location, { orderstring: orderstring, csrfmiddlewaretoken: $('#csrftoken').data('csrftoken')})
    .done(function( data ) {
      //window.location.href = window.location;
    });
   }

 });
  $("#sortable").disableSelection();
});

$('#sortable img').mousedown(function(event) {
  console.log("preventDefault");
  event.preventDefault();
});


$( "#submit_reorder" ).click(function() {

});

});


});
