

$( document ).ready(function() {
    interval_update_time = '5' //время в секундах
    getUpdate(interval_update_time)
});

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
        $('.adding').removeClass('display_none');
        $('.body').addClass('overflow_hidden');
    }
    if (event.target.classList.contains('edit_table')) {
        $('.editing').removeClass('display_none');
        $('.body').addClass('overflow_hidden');
    }
    if (event.target.classList.contains('edit_table_order')) {
        $('.editing_order').removeClass('display_none');
        $('.body').addClass('overflow_hidden');
    }
    if (event.target.classList.contains('exit_editing') || event.target.classList.contains('editing')) {
        $('.editing').addClass('display_none');
        $('.adding').addClass('display_none');
        $('.editing_order').addClass('display_none');
        $('.body').removeClass('overflow_hidden');
    }
    if (event.target.classList.contains('edit_table')) {
        $('.editing').removeClass('display_none');
        $('.body').addClass('overflow_hidden');
    }
    if (event.target.classList.contains('delete_table')) {
        delete_from_table(event.target.dataset.id);
    }
    if (event.target.classList.contains('edit_table')) {
        edit_from_table(event.target.dataset.id);
    }
}


$("#add_product_form_submit").click(function(){
	$.ajax({
		url: '/add_product',
		method: 'post',
		dataType: 'html',
		data: $("#add_product_form").serialize(),
		success: function(data_add){
		    console.log(data_add)
		    if (data_add === "unauthorized_user"){
                alert("Для дальнейших действий вам нужно авторизоваться!")
            }
            else{
                if (data_add === "added"){
                    alert("Запись успешно добавлена!")
                    $('.adding').addClass('display_none');
                    $('.body').removeClass('overflow_hidden');
                }
                else{
                    alert("Произошла ошибка, пожалуйста попробуйте позже!")
                }
            }
		}
	});
});

function delete_from_table(id){
    path = ''
    if (id.slice(0,2) === "ad"){
        path = "deleteAdmin"
    }
    else{
        if (id.slice(0,2) === "or"){
            path = "deleteOrder"
        }
        else{
            path = "deleteProduct"
        }

    }
    $.ajax('/admin/' + path + '/' + id.slice(3), {
            success: function(data){
                if (data["status"] != "unauthorized_user"){
                    if (data["status"] === "deleted"){
                        renderTables()
                    }
                }
            }
        })
}

function edit_from_table(id){
    path = ''
    if (id.slice(0,2) === "ad"){
        path = "getAdmin"
    }
    else{
        if (id.slice(0,2) === "or"){
            path = "getOrder"
        }
        else{
            path = "getProduct"
        }

    }
    $.ajax('/admin/' + path + '/' + id.slice(3), {
            success: function(data){
                if (data["status"] != "unauthorized_user"){
                    console.log(data)
                }
            }
        })
}




function getUpdate(interval){
    setTimeout(function(){
        $.ajax('/admin/getUpdate/' + interval + "000", {
            success: function(data){
                if (data["status"] != "unauthorized_user"){
                    if (data["status"] === "updated"){
                        renderTables()
                    }
                    getUpdate(interval)
                }
            }
        })}, parseInt(interval + "000")
    )
}

function renderTables(){
    $.get("/admin").done(function(response){
        let document=$(response);
        let admin_table = document.find("#admin-table").find("table");
        let order_table = document.find("#order-table").find("table");
        let product_table = document.find("#product-table").find("table");
        $( "#admin-table" ).html(admin_table);
        $( "#order-table" ).html(order_table);
        $( "#product-table" ).html(product_table);
      });
}