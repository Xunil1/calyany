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
}

renderCart()