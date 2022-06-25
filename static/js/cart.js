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

const renderCart = () => {
    if (Object.keys(cart).length > 0){
        $('#cart__mini').show()
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
			html_products += '<div id="cart_el"> Кальян Количество: ' + cart[cart_el] + '</div>'
			price += cart[cart_el] * pricing[cart_el]
		}
		else if (cart_el === "extra-cup"){
			html_products += '<div id="cart_el"> Доп.забивка Количество: ' + cart[cart_el] + '</div>'
			price += cart[cart_el] * pricing[cart_el]
		}
		else{
			html_products += '<div id="cart_el">'+ json[cart_el] + ' Количество: ' + cart[cart_el] + '</div>'
		}
		html_products_inputs += '<input type="hidden" name="order_' + cart_el + '" id="order_' + cart_el + '" value="' + cart[cart_el] + '">'
	    
	});
	$('#cart__products').append(html_products);
	$('#cart__products__inputs').append(html_products_inputs);


	let html_price = 'Сумма: ' + price + ' GEL'
	$('.final__price').append(html_price);
	$('.cart_fullprice').append(html_price);
}

renderCart()