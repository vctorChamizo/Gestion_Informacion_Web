// JavaScript Document
$(function() {
	// ordenar los menus de bootstrap
	var viewportWidth = $(window).width();
    if (viewportWidth <= 767) {
            $("#contenidomenu").removeClass("nav-justified").addClass("navbar-nav");
    }   
   //  fin ordenar menus boot
   
   // comportamiento buscar en movil, click en lupa
   $('#btsearch').click(function(e){
		$('#formbuscador').removeClass('posicion_buscar');	
		$('#formbuscador').addClass('posicion_input_buscar');
		$('#boption').show();
		if (viewportWidth <= 550) {
			$('#boption').addClass('boption_block');
		}
		if (!$('#search').is(':visible')){
		  e.preventDefault();
		}
		$('#search').show();
		$('#search').focus();
		$('#cerrar_buscador').show();
		$('#btsearch').hide();
		$('#collapse-personal').hide();
  });
  
  $('#cerrar_buscador').click(function(e){
	$('#formbuscador').removeClass('posicion_input_buscar');
	$('#formbuscador').addClass('posicion_buscar');	   
	$('#btsearch').show();
	$('#boption').hide();
	 if (viewportWidth <= 767) {
		 $('#collapse-personal').show();
		 $('#search').hide();
	 }
	$('#cerrar_buscador').hide();	
	e.preventDefault();
  });
   $('#carouselUcm').carousel({
	  interval: 10000,
	  pausa: 'hover',
   });
   
});