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
    console.log(cart)
    $data.find('input[type=checkbox]').each(function() {
       //находим инпуты для удаления и удаляем вместе с родительским li
       $("#city_list #" + $(this).attr('id')).parent().remove()
     })
    $('#cart__products').parentNode.removeChild($('#cart__products'));
	var html = '';
	Object.keys(cart).map(function(cart_el) {    
	    html += '<div id="cart_el">'+ cart_el + '</div>';
	});
	$('#cart__products').append(html);
}

renderCart()