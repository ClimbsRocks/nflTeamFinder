$(function() {
  $('.submitNewMessage').click(function() {

    $.ajax({
      url: '/submitMessage',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        console.log(response);
      },
      error: function(error) {
        console.log('the error is:',error);
      }
    });
  });
});
