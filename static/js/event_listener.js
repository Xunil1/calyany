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
    if (event.target.id == 'disclaimer__confirm' || event.target.id == 'disclaimer__confirm__text') {
		setCookie("disclaimer", "shown")
		$('.body').removeClass('overflow_hidden');
		$('.disclaimer').hide()
	}
    if (event.target.classList.contains('submit__button')) {
        send_order('/set_order_from_site', $("#cart__form"), $('#cart'))
    }
    
}



function send_order(path, form, modal){
    $.ajax({
		url: path,
		method: 'post',
		dataType: 'html',
		data: form.serialize(),
		success: function(data_add){
            if (data_add === "order_added"){
                $('.order__succesful').removeClass('display_none');
                modal.addClass('display_none');
                setTimeout( function(){
                    $('.order__succesful').addClass('display_none');
                    location.reload();
                }, 3000)
                $('.body').removeClass('overflow_hidden');
            }
            else{
                alert("Произошла ошибка, пожалуйста попробуйте позже!")
            }
        }
	});
}