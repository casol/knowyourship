  $(function() {
    $("#id_query").autocomplete({
      source: "/get_ship/",
      select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
      },
      minLength: 2,
    });
  });

  function AutoCompleteSelectHandler(event, ui)
  {
    var selectedObj = ui.item;
  }
