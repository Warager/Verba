$(function () {
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }

      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });
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
        if (res.success) {
          newRow.find('td:nth-child(2)').html(newRowWord.text());
          newRow.find('td:nth-child(1)').html(parseInt(newRowNum.text()) + 1);
          newRow.appendTo('.users-word-table');
          numOfWords.html(parseInt(numOfWords.text()) + 1);
          row.remove();
          $('.countNewWords').each(function (index, td) {
            $(td).text(index)
          });
        }
        else {
          $('#signInOrSignUp').modal("show")
        }
      },
      error: ajaxError
    });
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
        if (res.success) {
          $('.num-of-words').html(parseInt(numOfWords.text()) - 1);
          $('.countWords').each(function (index, td) {
            $(td).text(index)
          });
        }
        else if (res.error == "does_not_exist") {
          alert("Word Does Not Exist!")
        }
      },
      error: ajaxError
    });
    row.remove();
  });
  $(document).on('click', '.my-dict-show', function () {
    $('.users-word-table').show();
    $('.my-dict-show').hide();
    $('.my-dict-hide').show();
  });
  $(document).on('click', '.my-dict-hide', function () {
    $('.users-word-table').hide();
    $('.my-dict-show').show();
    $('.my-dict-hide').hide();
  });
});

function ajaxError() {
  alert('Ooops! Something get wrong!')
}

function processWords() {
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
      }
    },
    error: ajaxError
  });
};