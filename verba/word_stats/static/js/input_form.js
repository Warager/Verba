$(function (){
  $(document).on('click', '.process', function(){
    processWords();
    $(document).on('login', processWords)
  });
  $(document).on('click', '.go_back', function(){
    $('.analysis').hide();
    $('.general').show();
    $(document).off('login', processWords)
  });
  $(document).on('click', '#extraBtn', function(){
    $('.extraFeature').show(function(){
      if ($('#threeLetters').is(':checked')){
        $('#threeLetters').closest('label').addClass('active');
      }
      if ($('#onlyBase').is(':checked')){
        $('#onlyBase').closest('label').addClass('active');
      }
    });
    $('#extraBtn').hide();
    $('#extraHide').show();
  });
  $(document).on('click', '#extraHide', function(){
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