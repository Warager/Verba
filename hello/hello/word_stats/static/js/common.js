$(function(){
    $.ajaxSetup({
         beforeSend: function(xhr, settings) {
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
    $(".form-signin").submit(function(){
        $.ajax({
            url:"/accounts/login",
            data:{
                login:$('#myEmail').val(),
                password:$('#myPassword').val()
            },
            method: "POST",
            success: function(res){
                if((res) == "OK") {
                    document.location.reload()
                }
                else{
                    $(".invalidInput").show()
                }
            },
            error: function(){
                alert("Ooops! Something get wrong!")
            }
        });
        return false;
    });
    $(".form-signup").submit(function(){
        $.ajax({
            url: "accounts/signup",
            method: "POST",
            data: {
                login:$('#myNewEmail').val(),
                password:$('#myNewPassword').val(),
                confirm:$('#myNewPasswordConfirm').val()
            },
            success: function(res){
                if((res) == "OK") {
                    $('#signUp').hide();
                    $('#ThankYou').modal("show").on('hide.bs.modal', function(){
                        document.location.reload();
                    });
                }
                else if((res) == "Wrong") {
                    $(".invalidPassword").show()
                }
                else {
                    $(".invalidUserName").show()
                }
            },
            error: function(){
                alert("Ooops!")
            }
        });
        return false
    });
    $('.form-signup').click(function(){
      $(".invalidInput").hide();
      $(".invalidPassword").hide();
      $(".invalidUserName").hide();
    });
    $('.form-signin').click(function(){
      $(".invalidInput").hide();
      $(".invalidPassword").hide();
      $(".invalidUserName").hide();
    });
    $('#extraBtn').click(function(){
        $('.extraFeature').show();
        $('#extraBtn').hide();
        $('#extraHide').show();
    });
    $('#extraHide').click(function(){
        $('.extraFeature').hide();
        $('#extraBtn').show();
        $('#extraHide').hide();
    });
    $('.addWord').click(function(){
        var row = $(this).closest('tr');
        $.ajax({
            url:"process/add_word",
            method: "POST",
            data: {
                word: $(this).closest('tr').find('.wordInTable').text()
//                email:$('#myEmail').val()
            },
            success: function(res){
                if (res == "OK") {
                    row.remove()
                }
            },
            error: function(){
                alert('No OK response')
            }
        });
    });
});


