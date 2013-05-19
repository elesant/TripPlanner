$(document).ready(function(){
  var plan_ref = new Firebase('https://grouptrotter.firebaseio.com/plans/{{ plan.id }}');

  plan_ref.on('value', function(snapshot) {
    if(snapshot.val() === null) {
      alert('Plan does not exist!');
    } else {
      var events = snapshot.val().events;
      $('#event-list').html('');
      events.forEach(function(element, index, array) {
        $('#event-list').append(element + '<br />');
      });
    }
  });
});