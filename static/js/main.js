/*global requirejs: false*/

requirejs.config({
  baseUrl: '../static/'
  // OR
  // paths: {
  //   eventie: '../bower_components/eventie',
  //   'doc-ready': '../bower_components/doc-ready',
  //   eventEmitter: '../bower_components/eventEmitter',
  //   'get-style-property': '../bower_components/get-style-property',
  //   'get-size': '../bower_components/get-size',
  //   'matches-selector': '../bower_components/matches-selector',
  //   outlayer: '../bower_components/outlayer'
  // }
});

requirejs( [ '../static/masonry/masonry' ], function( Masonry ) {

  new Masonry( document.querySelector('#basic') );

});
