function build_table(selector) {
    $.getJSON("data.json", function(data) {
        // console.log(data);
        var tr_tag = $('<tr/>');
        tr_tag.append($('<th/>').attr('scope', 'col').text('FIO'));
        for (i = 1; i<=7; i++){
            tr_tag.append($('<th/>').attr('scope', 'col').addClass('text-center').text('Лаб. ' + i.toString()));
        }
        $(selector).append($('<thead/>').append($(tr_tag)));
        
        var tbody = $('<tbody/>');
        for (const [key, value] of Object.entries(data)) {
            var tr_tag = $('<tr/>');
            tr_tag.append($('<th/>').attr('scope', 'row').text(key));
            for (i = 1; i<=7; i++){
                if (value.indexOf(i) > -1){
                    tr_tag.append($('<th/>').addClass('text-center').attr('scope', 'col').text('+'));
                } else {
                    tr_tag.append($('<th/>').attr('scope', 'col').text(""));
                }
            }
            $(tbody).append(tr_tag);
            console.log(key);
        }
        $(selector).append(tbody);

    })
    
}

