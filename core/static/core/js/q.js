$(document).ready(function(){
 $( "#ships" ).autocomplete({
                        source: "/core/get_ship",
                        selectFirst: true,
                        minLength: 2
    });
});