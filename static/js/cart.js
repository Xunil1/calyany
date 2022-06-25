console.log(json)
let pricing = {
	"calyan": 30,
	"extra-cup": 12
} 
let cart = {

}


//увеличение количества товара 
//уменьшение количества товара
//удаление товара 


document.onclick = event => {
    console.log(event.target.classList)
    if (event.target.classList.contains('add')) {
        addFunction(event.target.dataset.id);
    }
    if (event.target.classList.contains('cart_show')) {
        $("#cart").toggle(200);
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
}







const addFunction = id => {
	if (cart[id] >= 1) {
		cart[id]++
	}
	else {
		cart[id] = 1
	}
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
    if (Object.keys(cart).length > 0){
        $('#cart__mini').show()
    }
    else{
        $('#cart__mini').hide()
        $('#cart').hide()
    }
    console.log(cart)
    $('.cart_fullprice').empty()
    $('#cart__products').empty()
    $('#cart__products__inputs').empty()
    $('.final__price').empty()
	let html_products = ''
	let html_products_inputs = ''
	let price = 0
	
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
		else{
		    html_products += '<div class="cart_el" id="cart_el"><div class="cart_el_title">'+ json[cart_el] + '</div>'
            html_products += '<div class="cart_el_count"><div class="cart_el_button minus" data-id="'+ cart_el +'">–</div><div class="cart_el_count_number">' + cart[cart_el] + '</div><div class="cart_el_button plus" data-id="'+ cart_el +'">+</div></div><div class="cart_el_price">' + 0 + ' GEL</div>'
		}
		html_products += '<div class="cart_el_button delete" data-id="'+ cart_el +'">×</div></div>'
		html_products_inputs += '<input type="hidden" name="order_' + cart_el + '" id="order_' + cart_el + '" value="' + cart[cart_el] + '">'
	    
	});
	$('#cart__products').append(html_products);
	$('#cart__products__inputs').append(html_products_inputs);


	let html_price = '<div>Сумма: ' + price + ' GEL</div>'
	$('.final__price').append(html_price);
	$('.cart_fullprice').append(html_price);
}

renderCart()