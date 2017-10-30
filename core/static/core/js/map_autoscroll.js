// autoscroll to search ship map and ship detail view map
window.onload = function(){
 $('html, body').animate({
          scrollTop: $("#map").offset().top
        }, 1000, "easeInOutExpo");
};