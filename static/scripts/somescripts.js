function createOption(ddl, text, value) {
    var opt = document.createElement('option');
    opt.value = value;
    opt.text = value + ' - ' + text;
    ddl.options.add(opt);
}

function configureListItems(selUE, selItems) {
    selItems.options.length = 0;
    $.post("/ls/get-items-for-ue",{ue: selUE.value},
        function(data, status){
            $.each(JSON.parse(data), function(i,v){createOption(selItems,v.item_name, v.item_id)});
      });
}
	
$(document).ready(function() {
    $('#example').DataTable( {
      scrollY:        '50vh',
      scrollX: true,
      scrollCollapse: true,
      paging:         false,
      ordering: false,
      columnDefs: [ {
        targets: 1,
        render: $.fn.dataTable.render.ellipsis(15)
    } ]
    } );
} );

var columns = [];

function getDT() {
    $.ajax({
      url: "/api/cols",
      success: function (data) {
        data = JSON.parse(data);
        columnNames = Object.keys(data);
        for (var i in data) {
          columns.push({data: data[i], 
                    title: capitalizeFirstLetter(data[i])});
        }
	    $('#list_items').DataTable( {
		    processing: true,
		    serverSide: false,
            scrollY:        '50vh',
            scrollX: true,
            scrollCollapse: true,
            paging:         false,
            ordering: false,
            columnDefs: [ {
                targets: 1,
                render: $.fn.dataTable.render.ellipsis(15)
            } ],
              
		    ajax: "/api/lls",
		    columns: columns
	    } );
      }
    });
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

$(document).ready(function() {
   getDT();
} );
