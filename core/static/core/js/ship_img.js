function ImgError(source){
        source.src = no_img_ship;
        source.onerror = "";
        var msg = 'Nice one? kinda... Would you like to add proper ship picture? Just visit <a href="{{ ship.url }}">Wikipedia page</a> and add some images!';
        document.getElementById('ship_img').innerHTML = msg;
        return true;
    }