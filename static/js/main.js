/*global requirejs: false*/
requirejs.config({
  paths: {
    jquery: "../bower_components/jquery/jquery",
    requirejs: "../bower_components/requirejs/require",
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
    "get-style-property": "../bower_components/get-style-property"
  }
});
console.log('requiring stuff');

requirejs(["jquery","dropzone","imagesloaded","masonry"], function($, Dropzone, imagesLoaded, Masonry) {
    console.log($);

      //owl carousel

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

          });*/

         jQuery.fn.doesExist = function(){
                return jQuery(this).length > 0;
         };



        imagesLoaded(
          '.js-masonry', 
          function() {
            console.log('images loaded');
            var container = document.querySelector('.js-masonry');
            var msnry = new Masonry( container, {
              // options...
              itemSelector: '.item'
            });
          });

        if($('.dropzone').doesExist()){
          new Dropzone(".dropzone", { 
          url: "{{ upload_url }}",
          paramName: "original_file"
          });
        };
      //custom select box

      $(function(){
          $('select.styled').customSelect();
      });

  });


});
