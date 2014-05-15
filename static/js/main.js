/*global requirejs: false*/
requirejs.config({
    paths: {
        "jquery": "../bower_components/jquery/jquery",
        "requirejs": "../bower_components/requirejs/require",
        "jquery.bootstrap": "../bower_components/bootstrap/dist/js/bootstrap",
        "dropzone": "../bower_components/dropzone/downloads/dropzone.min",
        "imagesloaded": "../bower_components/imagesloaded/imagesloaded",
        "masonry": "../bower_components/masonry/masonry",
        "eventEmitter": "../bower_components/eventEmitter",
        "eventie": "../bower_components/eventie",
        "get-size": "../bower_components/get-size",
        "jquery-bridget": "../bower_components/jquery-bridget/jquery.bridget",
        "item": "../bower_components/outlayer/item",
        "outlayer": "../bower_components/outlayer",
        "matches-selector": "../bower_components/matches-selector",
        "doc-ready": "../bower_components/doc-ready",
        "get-style-property": "../bower_components/get-style-property",
        "jquery.nicescroll": "../bower_components/jquery.nicescroll/jquery.nicescroll",
        "stripe": "https://js.stripe.com/v2/?1",
        "jquery.jquery-ui": "../bower_components/jquery-ui/ui/minified/jquery-ui.min",
        "videojs": "../bower_components/videojs/dist/video-js/video",
        "jquery.superslides": "../bower_components/superslides/dist/jquery.superslides"
    },
    shim: {
        "stripe": {
            exports: 'Stripe'
        },
        "jquery.bootstrap": {
            deps: ["jquery"]
        },
        "jquery.nicescroll": {
            deps: ["jquery"]
        },
        "jquery.jquery-ui": {
            deps: ["jquery"]
        },
    }

});
console.log('requiring stuff');

requirejs(["jquery", "dropzone", "imagesloaded", "masonry", "jquery.bootstrap", "jquery.nicescroll", "stripe", "jquery.jquery-ui", "videojs"], function($, Dropzone, imagesLoaded, Masonry, bootstrap, commonscripts, nicescroll, Stripe, ui, videojs) {
    console.log($);
    console.log("Stripe:");
    console.log(Stripe);

    $(document).ready(function() {

        //for testing ajax response
        //$.get(window.location.pathname, function(data) {
        //console.log("DATA ARRIVED");
        //console.log(data);
        //});


        jQuery.fn.doesExist = function() {
            return jQuery(this).length > 0;
        };

        if ($('.dropzone').doesExist()) {
            new Dropzone(".dropzone", {
                paramName: "original_file"
            });
        };


        $(".tileate").each(function() {
            console.log("tileate");
            var msnry = new Masonry($(this)[0], {
                // options...
                itemSelector: '.item'
            });

        });


        //bootstrapify images included in markdown
        $('img:not([class])').addClass('img-thumbnail');
        //custom select box

        //$(function(){
        //    $('select.styled').customSelect();
        //});



        $("#sortable").sortable({
            cursor: 'move',
            update: function(event, ui) {
                console.log("updated");
                var orderstring_ids = [];
                $(".media-representation").each(function(index) {
                    console.log(index + ": " + $(this).data("pk"));
                    orderstring_ids.push($(this).data("pk"));
                });
                var orderstring = "[" + orderstring_ids.join(",") + "]"
                console.log(orderstring);
                $.post(window.location, {
                    orderstring: orderstring,
                    csrfmiddlewaretoken: $('#csrftoken').data('csrftoken')
                })
                    .done(function(data) {
                        //window.location.href = window.location;
                    });
            }

        });
        $("#sortable").disableSelection();

        $('#sortable img').mousedown(function(event) {
            console.log("preventDefault");
            event.preventDefault();
        });


        $("#submit_reorder").click(function() {

        });

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
                console.log("token: " + token)
                $form.append($('<input type="hidden" name="stripeToken" />').val(token));
                // and submit
                $form.get(0).submit();
            }
        };

    });


});