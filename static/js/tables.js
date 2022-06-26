document.onclick = event => {
    console.log(event.target.classList)
    if (event.target.classList.contains('show-admin')) {
        $("#admin-table").show();
        $('.show-admin').addClass('active');
        $("#order-table").hide();
        $('.show-order').removeClass('active');
        $("#product-table").hide();
        $('.show-product').removeClass('active');
    }
    if (event.target.classList.contains('show-order')) {
        $("#admin-table").hide();
        $('.show-admin').removeClass('active');
        $("#order-table").show();
        $('.show-order').addClass('active');
        $("#product-table").hide();
        $('.show-product').removeClass('active');
    }
    if (event.target.classList.contains('show-product')) {
        $("#admin-table").hide();
        $('.show-admin').removeClass('active');
        $("#order-table").hide();
        $('.show-order').removeClass('active');
        $("#product-table").show();
        $('.show-product').addClass('active');
    }
    if (event.target.classList.contains('show_add_product')) {
        $('.editing').removeClass('display_none');
        $('.body').addClass('overflow_hidden');
    }
    if (event.target.classList.contains('exit_editing')) {
        $('.editing').addClass('display_none');
        $('.body').removeClass('overflow_hidden');
    }

}