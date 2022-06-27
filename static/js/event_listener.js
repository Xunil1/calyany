document.onclick = event => {
    console.log(event.target.classList)
    if (event.target.classList.contains('add')) {
        addFunction(event.target.dataset.id);
    }
    if (event.target.classList.contains('cart_show')) {
        $("#cart").toggle(200);
        $("#cart__mini").toggle(200);
        $('#cart__mini').removeClass('cart_active');
		$('.body').addClass('overflow_hidden');
    }
    if (event.target.classList.contains('cart__exit') || event.target.classList.contains('cart')) {
        $("#cart").toggle(200);
        $("#cart__mini").toggle(15);
        $('#cart__mini').addClass('cart_active');
		$('.body').removeClass('overflow_hidden');
    }
    if (event.target.classList.contains('minus')) {
        minusFunction(event.target.dataset.id);
    }
    if (event.target.classList.contains('plus')) {
        plusFunction(event.target.dataset.id);
    }
    if (event.target.classList.contains('delete')) {
        deleteFunction(event.target.dataset.id);
    }
    if (event.target.id == 'disclaimer__confirm' || event.target.classList.contains('disclaimer__button_text')) {
		setCookie("disclaimer", "shown")
		$('.body').removeClass('overflow_hidden');
		$('.disclaimer').hide()
	}
}