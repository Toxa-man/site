function build_table(selector) {
    $.getJSON("data.json", function(data) {
        var lab_count = 3;
        var tr_tag = $('<tr/>');
        tr_tag.append($('<th/>').attr({scope: 'col', style: 'width: 20%'}).text('ФИО'));
        for (i = 1; i < lab_count; i++){
            tr_tag.append($('<th/>').attr('scope', 'col').addClass('text-center').text('Лаб. ' + i.toString() ));
        }
        tr_tag.append($('<th/>').attr('scope', 'col').addClass('text-center').text('Курсовая'));
        $(selector).append($('<thead/>').append($(tr_tag)));
        
        var tbody = $('<tbody/>');
        for (const [key, value] of Object.entries(data)) {
            var tr_tag = $('<tr/>');
            var fio = key;
            if (value["fio"]){
                fio = value["fio"];
            }
            tr_tag.append($('<th/>').attr('scope', 'row').text(fio));
            for (i = 1; i <= lab_count; i++){
                var lab_result = "";
                if (value["labs"].indexOf(i) > -1){
                    lab_result = "+";
                }
                if (i == lab_count){
                    lab_result = value["course_mark"];
                } 
                tr_tag.append($('<th/>').addClass('text-center').attr('scope', 'col').text(lab_result));
            }
            $(tbody).append(tr_tag);
        }
        $(selector).append(tbody);

    })
    
}

