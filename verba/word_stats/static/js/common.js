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
});

function ajaxError() {
  alert('Ooops! Something get wrong!')
}