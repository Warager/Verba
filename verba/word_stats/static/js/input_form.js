$(function (){
  $(document).on('click', '.process', function(){
    processWords();
    $(document).on('login', processWords)
  });
  $(document).on('click', '.go_back', function(){
    $('.analysis').hide();
    $('.general').show();
    $(document).off('login', processWords)
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