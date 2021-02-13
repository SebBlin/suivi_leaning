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
