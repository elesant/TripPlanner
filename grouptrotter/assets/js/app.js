var app = angular.module('app', ['firebase']);

$(document).ready(function () {
  var offsetFn = function() {
    return $('#affix-sidebar').position().top;
  };
  $('#affix-sidebar').affix({
    offset: {top: offsetFn}
  });

  $('.navbar-fixed-top').affix();

});