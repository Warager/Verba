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
      if (res.reply == "OK") {
        $('.navhead').html(res.navhead)
      }
      else {
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
      if (res.reply == "OK") {
        $('#signUp').hide();
        $('#ThankYou').modal("show").on('hide.bs.modal', function () {
          document.location.reload();
        });
      }
      else if (res.reply == "Wrong") {
        $(".invalidPassword").show()
      }
      else if (res.reply == "EmptyUser") {
        $(".emptyUserName").show()
      }
      else if (res.reply == "EmptyPassword") {
        $(".emptyPassword").show()
      }
      else {
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
