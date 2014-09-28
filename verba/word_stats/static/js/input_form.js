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