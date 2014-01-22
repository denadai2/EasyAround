

$(document).ready(function() {
	$( "input[type=date]" ).datepicker();

	 $( ".ui-slider" ).slider({
		value:3,
		min: 1,
		max: 5,
		step: 1,
		slide: function( event, ui ) {
			$( "#"+$(this).attr("id")+"-slider" ).val( "$" + ui.value );
		}
	});
	$( "#amount" ).val( "$" + $( "#slider" ).slider( "value" ) );

	$( "#dinamicity-slider" ).slider({
		value:2,
		min: 1,
		max: 3,
		step: 1,
		slide: function( event, ui ) {
			$( "#dinamicity-slider" ).val( "$" + ui.value );
		}
	});
	$( "#dinamicity" ).val( "$" + $( "#slider" ).slider( "value" ) );
});
