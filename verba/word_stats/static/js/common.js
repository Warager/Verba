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
  function ajaxError() {
    alert('Ooops! Something get wrong!')
  }

  $(".form-signin").submit(function () {
    $.ajax({
      url: "/accounts/login",
      data: {
        login: $('#myEmail').val(),
        password: $('#myPassword').val()
      },
      method: "POST",
      success: function (res) {
        if ((res) == "OK") {
          document.location.reload()
        }
        else {
          $(".invalidInput").show()
        }
      },
      error: ajaxError()
    });
    return false;
  });
  $(".form-signup").submit(function () {
    $.ajax({
      url: "accounts/signup",
      method: "POST",
      data: {
        login: $('#myNewEmail').val(),
        name: $('#myName').val(),
        password: $('#myNewPassword').val(),
        confirm: $('#myNewPasswordConfirm').val()
      },
      success: function (res) {
        if ((res) == "OK") {
          $('#signUp').hide();
          $('#ThankYou').modal("show").on('hide.bs.modal', function () {
            document.location.reload();
          });
        }
        else if ((res) == "Wrong") {
          $(".invalidPassword").show()
        }
        else if ((res) == "EmptyUser") {
          $(".emptyUserName").show()
        }
        else if ((res) == "EmptyPassword") {
          $(".emptyPassword").show()
        }
        else {
          $(".invalidUserName").show()
        }
      },
      error: ajaxError()
    });
    return false
  });
  $('.form-signup').click(function () {
    $(".invalidInput").hide();
    $(".invalidPassword").hide();
    $(".invalidUserName").hide();
    $(".emptyUserName").hide();
    $(".emptyPassword").hide();
  });
  $('.form-signin').click(function () {
    $(".invalidInput").hide();
    $(".invalidPassword").hide();
    $(".invalidUserName").hide();
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
        if (res == "OK") {
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
      error: ajaxError()
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


