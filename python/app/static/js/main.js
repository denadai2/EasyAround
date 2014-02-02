

$(document).ready(function() {
	$( "input[type=date]" ).datepicker();

	 $( ".ui-slider" ).slider({
		value:3,
		min: 1,
		max: 5,
		step: 1,
		slide: function( event, ui ) {
			$( "#"+$(this).attr("id").replace('-slider', '') ).val( ui.value );
		}
	});
	$( "#amount" ).val( "$" + $( "#slider" ).slider( "value" ) );

	function log( message ) {
		$( "<div>" ).text( message ).prependTo( "#log" );
		$( "#log" ).scrollTop( 0 );
	}

	$( "#clientName" ).autocomplete({
		source: "getClients",
		minLength: 2,
		select: function( event, ui ) {
		log( ui.item ?
		"Selected: " + ui.item.value + " aka " + ui.item.id :
		"Nothing selected, input was " + this.value );
		}
	});


	$('#excludeLocations, #includeLocations').textext({
            plugins : 'autocomplete tags ajax',
            ajax : {
                url : '/getLocations',
                dataType : 'json',
                cacheResults : false
            }
        });



	$("#submit").click(function(){
		$("form").submit();
	});
});
