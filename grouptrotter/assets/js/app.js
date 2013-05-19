$(document).ready(function () {
  var offsetFn = function() {
    return $('#affix-sidebar').position().top;
  };
  $('#affix-sidebar').affix({
    offset: {top: offsetFn}
  });

  $('.navbar-fixed-top').affix();

  // index page
  $.get('/api/plan/list', function(data) {
    var plan_list = data['plans'];
    plan_list.forEach(function(element, index, array) {
      $('#container').append('<div class="item"><a href="/plan/' + element['id'] + '">' + element['title'] + '</a></div>');
    });
  });

  $(function(){
    $('#container').masonry({
      // options
      itemSelector : '.item',
      columnWidth : 240
    });
  });

  $('#create_list_plan').submit(function() {
    $.ajax({
      type: "POST",
      url: '/api/plan/add/',
      data: {
        title: $('#create_list_plan_text').val()
      },
      success: function (data) {
        window.location = '/plan/' + data.plan_id;
      }
    })
  });
});
