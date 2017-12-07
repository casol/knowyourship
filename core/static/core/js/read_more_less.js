$(document).ready(function() {
(function(){
    var showChar = 1600;
    var ellipsestext = "...";

    $('.truncate').each(function() {
        var content = $(this).html();
        if(content.length > showChar) {

            var c = content.substr(0, showChar);
            var h = content;
            var html = '<div class="truncate-text" style="display:block">' + c + '<span class="moreellipses">' + ellipsestext + '&nbsp;&nbsp;<a href="" class="moreless more"><i class="fa fa-plus-square" title="Show All"></i> Show All</a></span></span></div><div class="truncate-text" style="display:none">' + h + '<a href="" class="moreless less"><i class="fa fa-minus-square" title="Hide"></i> hide</a></span></div>';

            $(this).html(html);
        }

    });

    $(".moreless").click(function(){
        var thisEl = $(this);
        if(thisEl.hasClass("less")) {
            thisEl.closest('.truncate-text').prev('.truncate-text').toggle();
            thisEl.closest('.truncate-text').slideToggle();
            $('html, body').animate({
                    scrollTop: $("#portfolio").offset().top
                }, 1200);

        } else {
            thisEl.closest('.truncate-text').toggle();
            thisEl.closest('.truncate-text').next('.truncate-text').fadeToggle();
        }
        return false;
    });
    /* end iffe */
    }());

/* end ready */
});