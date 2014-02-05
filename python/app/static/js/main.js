

var excludeList = Array();

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

	$( "#clientName" ).autocomplete({
		source: "getClients",
		minLength: 2,
		select: function (event, ui) {
			event.preventDefault();
	        $("#clientName").val(ui.item.label); // display the selected text
	        $("#existingClient").val(ui.item.value); // save selected id to hidden input
			$("#clientDetails").hide();
	    }
	});

	$( "#clientName" ).keyup(function(){
		$("#existingClient").val(0);
		$("#clientDetails").show();
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


	$( "#modifyItinerary" ).click(function(event){
		$("td > a").addClass("active");
		$("#showNewItinerary").show();
		$(this).hide();
		$("#confirmItinerary").hide();
		event.preventDefault();
	});

	$( "td > a" ).click(function(event){
		if($(this).hasClass("active")){
			$(this).parent().css('opacity', '0.3');
			$(this).removeClass('active');
			excludeList.push($(this).attr("id").replace("location", ""));
		}
		event.preventDefault();
	});

	$( "#showNewItinerary" ).click(function(event){
		$(this).attr("href", $(this).attr("href")+"?excludeList="+excludeList.join(","));
	});

	$( "#confirmItinerary" ).click(function(event){
		alert("Thank you, your trip has been confirmed");
	});
	
});
