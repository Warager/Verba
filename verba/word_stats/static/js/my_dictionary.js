function ajaxError() {
  alert('Ooops! Something get wrong!')
}
$('.my-dict-show').click(function () {
  $('.users-word-table').show();
  $('.my-dict-show').hide();
  $('.my-dict-hide').show();
});
$('.my-dict-hide').click(function () {
  $('.users-word-table').hide();
  $('.my-dict-show').show();
  $('.my-dict-hide').hide();
});
$(document).on('click', '.remWord', function () {
  var row = $(this).closest('tr');
  var numOfWords = $('.num-of-words');
  $.ajax({
    url: "process/rem_word",
    method: "POST",
    data: {
      wordToRem: row.find('.wordInTable').text()
    },
    success: function (res) {
      if (res == "OK") {
        $('.num-of-words').html(parseInt(numOfWords.text()) - 1);
        $('.countWords').each(function (index, td) {
          $(td).text(index)
        });
      }
      else if (res == "DoesNotExist") {
        alert("Word Does Not Exist!")
      }
    },
    error: ajaxError()
  });
  row.remove();
});