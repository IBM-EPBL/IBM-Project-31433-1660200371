$(function () {
  $(".sidenav").sidenav();
  $("select").formSelect();
  $(".tabs").tabs();
  $("textarea#share_story").characterCounter();

  // SEACH IN THE TABLE
  $("#search").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#filter_info tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });

  // PHONE NUMBER FORMATTER

  $("#password").on("focusout", function (e) {
    if ($(this).val() != $("#confirmPassword").val()) {
      $("#confirmPassword").removeClass("valid").addClass("invalid");
    } else {
      $("#confirmPassword").removeClass("invalid").addClass("valid");
    }
  });

  $("#confirmPassword").on("keyup", function (e) {
    if ($("#password").val() != $(this).val()) {
      $(this).removeClass("valid").addClass("invalid");
    } else {
      $(this).removeClass("invalid").addClass("valid");
    }
  });
});
