if (getCookie("disclaimer") === "shown"){
	$('.body').removeClass('overflow_hidden');
	$('.disclaimer').hide()
}
else{
	$('.body').addClass('overflow_hidden');
	$('.disclaimer').show();
}