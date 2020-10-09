// Project Management Article
$("#buttonPM").click(function () {
  $("#dataDev").hide(20);
  $("#dataPM").toggle(400);
});

// Development Article
$("#buttonDev").click(function () {
  $("#dataPM").hide(20);
  $("#dataDev").toggle(400);
});