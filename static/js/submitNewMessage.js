var prettyNames = {
  '1': 'almost certainly not',
  '2': 'somewhat likely to be',
  '3': 'fairly likely to be',
  '4': 'most likely',
  '5': 'almost certainly'
};

$(function() {
  $('.submitNewMessage').click(function() {

    $.ajax({
      url: '/submitMessage',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        $('.result').text('This message is ' + prettyNames[response] + ' about an NFL team.');
      },
      error: function(error) {
        console.log('the error is:',error);
      }
    });
  });
});
