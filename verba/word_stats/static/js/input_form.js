$(function (){
  $(document).on('click', '.process', function () {
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