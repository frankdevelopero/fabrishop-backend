$(document).ready(function() {
  $("#sidebarCollapse").on("click", function() {
    $("#sidebar").addClass("active");
  });

  $("#sidebarCollapseX").on("click", function() {
    $("#sidebar").removeClass("active");
  });

  $("#sidebarCollapse").on("click", function() {
    if ($("#sidebar").hasClass("active")) {
      $(".overlay").addClass("visible");
      console.log("it's working!");
    }
  });

  $("#sidebarCollapseX").on("click", function() {
    $(".overlay").removeClass("visible");
  });
});

var navItems = document.querySelectorAll(".mobile-bottom-nav__item");
navItems.forEach(function(e, i) {
	e.addEventListener("click", function(e) {
		navItems.forEach(function(e2, i2) {
			e2.classList.remove("mobile-bottom-nav__item--active");
		})
		this.classList.add("mobile-bottom-nav__item--active");
	});
});

$(document).ready(function() {
  $("#navbar").click();
});