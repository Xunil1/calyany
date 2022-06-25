if (getCookie("disclaimer") === "show"){
	$('.body').removeClass('overflow_hidden');
	$('.disclaimer').hide()
}
else{
	$('.body').addClass('overflow_hidden');
	$('.disclaimer').show()
}