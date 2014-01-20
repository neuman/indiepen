/*global requirejs: false*/
requirejs.config({
  baseUrl: '../static/'
  // OR
  // paths: {
  //   jquery: '../bower_components/jquery',
  //   eventie: '../bower_components/eventie',
  //   'doc-ready': '../bower_components/doc-ready',
  //   eventEmitter: '../bower_components/eventEmitter',
  //   'get-style-property': '../bower_components/get-style-property',
  //   'get-size': '../bower_components/get-size',
  //   'matches-selector': '../bower_components/matches-selector',
  //   outlayer: '../bower_components/outlayer'
  // }
});
console.log('requiring stuff');

requirejs(['../static/jquery/jquery'], function( $) {
    console.log($);       // undefined


});
