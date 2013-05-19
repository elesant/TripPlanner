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
      $('#plan-list').append('<div class="well"><a href="/plan/' + element['id'] + '">' + element['title'] + '</a></div>');
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
