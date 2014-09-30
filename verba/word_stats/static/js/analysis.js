function ajaxError() {
  alert('Ooops! Something get wrong!')
}
$(document).on('click', '.addWord', function () {
  var row = $(this).closest('tr');
  var newRowWord = row.find('td:nth-child(2)');
  var newRow = $('.users-word-table tr:last').clone().show();
  var newRowNum = newRow.find('td:nth-child(1)');
  var numOfWords = $('.num-of-words');

  $.ajax({
    url: "process/add_word",
    method: "POST",
    data: {
      word: $(this).closest('tr').find('.wordInTable').text()
    },
    success: function (res) {
      if (res.reply == "OK") {
        newRow.find('td:nth-child(2)').html(newRowWord.text());
        newRow.find('td:nth-child(1)').html(parseInt(newRowNum.text()) + 1);
        newRow.appendTo('.users-word-table');
        numOfWords.html(parseInt(numOfWords.text()) + 1);
        row.remove();
        $('.countNewWords').each(function (index, td) {
          $(td).text(index)
        });
      }
    },
    error: ajaxError
  });
});

