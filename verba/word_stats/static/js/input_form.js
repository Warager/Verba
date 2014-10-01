$(function (){
    $(document).on('click', '.process', function () {
//    var row = $(this).closest('tr');
//    var newRowWord = row.find('td:nth-child(2)');
//    var newRow = $('.users-word-table tr:last').clone().show();
//    var newRowNum = newRow.find('td:nth-child(1)');
//    var numOfWords = $('.num-of-words');

    $.ajax({
      url: "process",
      method: "POST",
      data: {
        text: $('#textarea').val(),
        threeLetters: $('#threeLetters').is(':checked'),
        onlyBase: $('#onlyBase').is(':checked')
      },
      success: function (res) {
        if (res.success) {
          var analysis = $('.analysis');
          analysis.html(res.analysis);
          $('.general').hide();
          analysis.show();
//          newRow.find('td:nth-child(2)').html(newRowWord.text());
//          newRow.find('td:nth-child(1)').html(parseInt(newRowNum.text()) + 1);
//          newRow.appendTo('.users-word-table');
//          numOfWords.html(parseInt(numOfWords.text()) + 1);
//          row.remove();
//          $('.countNewWords').each(function (index, td) {
//            $(td).text(index)
//          });
        }
//        else if (res.error == 'error'){
//          $('#signInOrSignUp').modal("show");
//        }
      },
      error: ajaxError
    });
  });
  $('#extraBtn').click(function () {
    $('.extraFeature').show();
    $('#extraBtn').hide();
    $('#extraHide').show();
  });
  $('#extraHide').click(function () {
    $('.extraFeature').hide();
    $('#extraBtn').show();
    $('#extraHide').hide();
  });
  $("#3letters-popover").hover(
      function () {
        $(this).popover("show");
      },
      function () {
        $(this).popover("hide");
      }
  );
  $("#onlyBase-popover").hover(
      function () {
        $(this).popover("show");
      },
      function () {
        $(this).popover("hide");
      }
  );
});