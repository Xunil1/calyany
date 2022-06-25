document.onclick = event => {
    console.log(event.target.classList)
    if (event.target.classList.contains('show-admin')) {
        $("#admin-table").show();
        $("#order-table").hide();
        $("#product-table").hide();
    }
    if (event.target.classList.contains('show-order')) {
        $("#admin-table").hide();
        $("#order-table").show();
        $("#product-table").hide();
    }
    if (event.target.classList.contains('show-product')) {
        $("#admin-table").hide();
        $("#order-table").hide();
        $("#product-table").show();
    }
}