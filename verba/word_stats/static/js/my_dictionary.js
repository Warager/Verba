$(function (){
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