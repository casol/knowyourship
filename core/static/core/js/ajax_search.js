$(function(){

// using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('#id_query').on('keyup', function () {
       $.ajax({
           type: 'POST',                 #request method
           url: '/music/search/',        #request url
           data: {
               'search_text' : $('#id_query').val(),
               'csrfmiddlewaretoken': getCookie('csrftoken')
           },
           success: function(response){
               $('#search_results').html(response)
           }
       })
    });

});