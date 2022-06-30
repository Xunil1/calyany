// console.log(json)
let pricing = {
	"calyan": 30,
	"extra-cup": 12
} 
let cart = {

}

const addFunction = id => {
	if (cart[id] >= 1) {
		cart[id]++
	}
	else {
		cart[id] = 1
	}
	$('#cart__mini').addClass('cart_active');
    renderCart()
}

const minusFunction = id => {
	if (cart[id] === 1) {
		cart[id] = 1
	}
	else {
		cart[id] -= 1
	}
    renderCart()
}

const plusFunction = id => {
	cart[id]++
    renderCart()
}

const deleteFunction = id => {
	delete cart[id]
    renderCart()
}

const renderCart = () => {
    let price = 0
	let counter = 0

    if (Object.keys(cart).length > 0){
    	if ($('#cart__mini').hasClass("cart_active")){
        	$('#cart__mini').show()
    	}
    }
    else{
        $('#cart__mini').hide()
        $('#cart').hide()
        $('.body').removeClass('overflow_hidden');
    }
    console.log(cart)
    $('.cart_fullprice').empty()
    $('#cart__products').empty()
    $('#cart__products__inputs').empty()
    $('.final__price').empty()
	$('.cart__mini__counter').empty()
	let html_products = ''
	let html_products_inputs = ''
	let html_cart_mini_counter = ''

	Object.keys(cart).map(function(cart_el) {
		if (cart_el === "calyan"){
			html_products += '<div class="cart_el" id="cart_el"><div class="cart_el_title">Кальян</div>'
            html_products += '<div class="cart_el_count"><div class="cart_el_button minus" data-id="'+ cart_el +'">–</div><div class="cart_el_count_number">' + cart[cart_el] + '</div><div class="cart_el_button plus" data-id="'+ cart_el +'">+</div></div><div class="cart_el_price">' + cart[cart_el] * pricing[cart_el] + ' GEL</div>'
			price += cart[cart_el] * pricing[cart_el]
		}
		else if (cart_el === "extra-cup"){
			html_products += '<div class="cart_el" id="cart_el"><div class="cart_el_title">Дополнительная забивка</div>'
            html_products += '<div class="cart_el_count"><div class="cart_el_button minus" data-id="'+ cart_el +'">–</div><div class="cart_el_count_number">' + cart[cart_el] + '</div><div class="cart_el_button plus" data-id="'+ cart_el +'">+</div></div><div class="cart_el_price">' + cart[cart_el] * pricing[cart_el] + ' GEL</div>'
			price += cart[cart_el] * pricing[cart_el]
		}
		else if (cart_el === "choise"){
			html_products += '<div class="cart_el" id="cart_el"><div class="cart_el_title">Выберите что-нибудь сами</div>'
            html_products += '<div class="cart_el_count"><div class="cart_el_button minus" data-id="'+ cart_el +'">–</div><div class="cart_el_count_number">' + cart[cart_el] + '</div><div class="cart_el_button plus" data-id="'+ cart_el +'">+</div></div><div class="cart_el_price">' + 0 + ' GEL</div>'
		}
		else{
		    html_products += '<div class="cart_el" id="cart_el"><div class="cart_el_title">'+ json[cart_el] + '</div>'
            html_products += '<div class="cart_el_count"><div class="cart_el_button minus" data-id="'+ cart_el +'">–</div><div class="cart_el_count_number">' + cart[cart_el] + '</div><div class="cart_el_button plus" data-id="'+ cart_el +'">+</div></div><div class="cart_el_price">' + 0 + ' GEL</div>'
		}
		html_products += '<div class="cart_el_button delete" data-id="'+ cart_el +'">×</div></div>'
		html_products_inputs += '<input type="hidden" name="order_' + cart_el + '" id="order_' + cart_el + '" value="' + cart[cart_el] + '">'
	    	
	});
	if (isNaN(cart['extra-cup']) === true) {
		counter = cart['calyan']
	}
	else if (isNaN(cart['calyan']) === true) {
		counter = cart['extra-cup']
	}
	else {
		counter = cart['calyan'] + cart['extra-cup']
	}

	html_cart_mini_counter += '<div>' + counter + '</div>'
	$('#cart__products').append(html_products);
	$('#cart__products__inputs').append(html_products_inputs);
	$('.cart__mini__counter').append(html_cart_mini_counter);

	if ($('#cart__mini').hasClass("cart_active") && counter > 0) {
		$('.cart__mini__counter').show()
	}
	else { 
		$('.cart__mini__counter').hide()
	}

	let html_price = '<div>Сумма: ' + price + ' GEL</div>'
	$('.final__price').append(html_price);
	$('.cart_fullprice').append(html_price);

    if (price < 30){
        $('.submit__button').attr('disabled', true);
		$('.cart__order').addClass('display_none')
    }
    else{
        $('.submit__button').removeAttr('disabled');
		$('.cart__order').removeClass('display_none')
    }

}

renderCart()