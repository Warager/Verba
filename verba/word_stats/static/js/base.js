$(function () {
  $(".form-signin").submit(function () {
    $.ajax({
      url: "/accounts/login",
      data: {
        login: $('#myEmail').val(),
        password: $('#myPassword').val()
      },
      method: "POST",
      success: function (res) {
        if (res.success) {
          $('.headline').html(res.headline);
          $('#signIn').modal("hide")
        }
        else if (res.error == 'error'){
          $(".invalidInput").show()
        }
      },
      error: ajaxError
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
        if (res.success) {
          $('#signUp').hide();
          $('#ThankYou').modal("show").on('hide.bs.modal', function () {
            document.location.reload();
          });
        }
        else if (res.error == "wrong") {
          $(".invalidPassword").show()
        }
        else if (res.error == "empty_user") {
          $(".emptyUserName").show()
        }
        else if (res.error == "empty_password") {
          $(".emptyPassword").show()
        }
        else  if (res.error == "error"){
          $(".invalidUserName").show()
        }
      },
      error: ajaxError
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
});