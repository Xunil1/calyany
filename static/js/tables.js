

$( document ).ready(function() {
    interval_update_time = '60' //время в секундах
    getUpdate(interval_update_time)
});

document.onclick = event => {
    console.log(event.target.classList)
    if (event.target.classList.contains('show-admin')) {
        $("#admin-table").show();
        $('.show-admin').addClass('active');
        $(".order__cards").hide();
        $('.show-order').removeClass('active');
        $("#product-table").hide();
        $('.show-product').removeClass('active');
    }
    if (event.target.classList.contains('show-order')) {
        $("#admin-table").hide();
        $('.show-admin').removeClass('active');
        $(".order__cards").show();
        $('.show-order').addClass('active');
        $("#product-table").hide();
        $('.show-product').removeClass('active');
    }
    if (event.target.classList.contains('show-product')) {
        $("#admin-table").hide();
        $('.show-admin').removeClass('active');
        $(".order__cards").hide();
        $('.show-order').removeClass('active');
        $("#product-table").show();
        $('.show-product').addClass('active');
    }
    if (event.target.classList.contains('show_add_product')) {
        $('.adding__product').removeClass('display_none');
        $('.body').addClass('overflow_hidden');
    }
    if (event.target.classList.contains('edit_table')) {
        $('.editing').removeClass('display_none');
        $('.body').addClass('overflow_hidden');
        edit_from_table(event.target.dataset.id);
    }
    if (event.target.classList.contains('edit_table_order')) {
        $('.editing_order').removeClass('display_none');
        $('.body').addClass('overflow_hidden');
        edit_from_table(event.target.dataset.id);
    }
    if (event.target.classList.contains('edit_table_admin')) {
        $('.editing_admin').removeClass('display_none');
        $('.body').addClass('overflow_hidden');
        edit_from_table(event.target.dataset.id);
    }
    if (event.target.classList.contains('show_add_admin')) {
        $('.adding_admin').removeClass('display_none');
        $('.body').addClass('overflow_hidden');
    }
    
    if (event.target.classList.contains('exit_editing') || event.target.classList.contains('editing')) {
        $('.editing').addClass('display_none');
        $('.adding__product').addClass('display_none');
        $('.editing_admin').addClass('display_none');
        $('.editing_order').addClass('display_none');
        $('.adding_admin').addClass('display_none');
        $('.body').removeClass('overflow_hidden');
    }
    if (event.target.classList.contains('delete_table')) {
        delete_from_table(event.target.dataset.id);
    }
    if (event.target.id == "edit_product_form_submit" || event.target.id == "edit_order_form_submit" || event.target.id == "edit_admin_form_submit") {
        send_edited_data(event.target.dataset.id);
    }

    if (event.target.classList.contains('show__aside') && !($('.aside').hasClass('aside__position__absolute'))) {
        $('.aside').removeClass('aside__display__none');
        $('.aside').addClass('aside__position__absolute');
        $('.body').addClass('overflow_hidden');
    }
    else if (event.target.classList.contains('show__aside') && $('.aside').hasClass('aside__position__absolute')) {
        $('.aside').addClass('aside__display__none');
        $('.aside').removeClass('aside__position__absolute');
        $('.body').removeClass('overflow_hidden');
    }

    // if (event.target.classList.contains('show__aside') && $('.aside').hasClass('aside__position__absolute')) {
    //     $('.aside').addClass('aside__display__none');
    //     $('.aside').removeClass('aside__position__absolute');
    // }
    // if (event.target.classList.contains('show__aside') && $('.aside').hasClass('aside__display__none')) {
    //     $('.aside').removeClass('aside__display__none');
    //     $('.aside').addClass('aside__position__absolute');
    // }
    
    
}
$(".button_logout").click(function(){
    log_out('/add_product', $("#add_product_form"), $('.adding'))
});

$("#add_product_form_submit").click(function(){
    send_adding_data('/add_product', $("#add_product_form"), $('.adding'))
});

$("#add_admin_form_submit").click(function(){
	send_adding_data('/add_admin', $("#add_admin_form"), $('.adding_admin'))
});


function send_adding_data(path, form, modal){
    $.ajax({
		url: path,
		method: 'post',
		dataType: 'html',
		data: form.serialize(),
		success: function(data_add){
		    console.log(data_add)
		    if (data_add === "unauthorized_user"){
                alert("Для дальнейших действий вам нужно авторизоваться!")
            }
            else{
                if (data_add === "added"){
                    alert("Запись успешно добавлена!")
                    modal.addClass('display_none');
                    $('.body').removeClass('overflow_hidden');
                    renderTables(window.location.pathname + window.location.search)
                }
                else{
                    alert("Произошла ошибка, пожалуйста попробуйте позже!")
                }
            }
		}
	});
}


function log_out(){
    $.ajax('/logout', {
            success: function(data){
                location.reload();
            }
        })
}


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
                        renderTables(window.location.pathname + window.location.search)
                    }
                }
            }
        })
}

function send_edited_data(id){
    path = ''
    console.log(id)
    if (id.slice(0,2) === "ad"){
        path = "/edit_admin/" + id.slice(3)
        form = $("#edit_admin_form")
        modal = $(".editing_admin")
    }
    else{
        if (id.slice(0,2) === "or"){
            path = "/edit_order/" + id.slice(3)
            form = $("#edit_order_form")
            modal = $(".editing_order")
        }
        else{
            path = "/edit_product/" + id.slice(3)
            form = $("#edit_product_form")
            modal = $(".editing")
        }
    }
    $.ajax({
		url: path,
		method: 'post',
		dataType: 'html',
		data: form.serialize(),
		success: function(data_add){
		    if (data_add === "unauthorized_user"){
                alert("Для дальнейших действий вам нужно авторизоваться!")
            }
            else{
                if (data_add === "edited"){
                    alert("Запись успешно изменена!")
                    modal.addClass('display_none');
                    $('.body').removeClass('overflow_hidden');
                    renderTables(window.location.pathname + window.location.search)
                }
                else{
                    alert("Произошла ошибка, пожалуйста попробуйте позже!")
                }
            }
		}
	});
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
                console.log(id)
                if (data["status"] != "unauthorized_user"){
                    if (id.slice(0,2) === "ad"){
                        let formAdmin = $("#edit_admin_form")
                        formAdmin.find("#admin_name").val(data["name"])
                        formAdmin.find("#admin_surname").val(data["surname"])
                        formAdmin.find("#admin_username").val(data["username"])
                        formAdmin.find("#admin_email").val(data["email"])
                        formAdmin.find("#edit_admin_form_submit").attr("data-id", id)
                    }
                    else{
                        if (id.slice(0,2) === "or"){
                            let formOrder = $("#edit_order_form")
                            formOrder.find("#name").val(data["name"])
                            formOrder.find("#address").val(data["address"])
                            formOrder.find("#phone").val(data["phone"])
                            formOrder.find("#order_el").val(data["order_el"])
                            formOrder.find("#comment").val(data["comment"])
                            formOrder.find("#deposit").val(data["deposit"])
                            formOrder.find("#edit_order_form_submit").attr("data-id", id)
                        }
                        else{
                            let formProduct = $("#edit_product_form")
                            formProduct.find("#edit_product_name").val(data["name"])
                            formProduct.find("#edit_product_description").val(data["description"])
                            formProduct.find("#edit_product_count").val(data["count"])
                            formProduct.find("#edit_product_form_submit").attr("data-id", id)
                        }

                    }
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
                        renderTables(window.location.pathname + window.location.search)
                    }
                    getUpdate(interval)
                }
            }
        })}, parseInt(interval + "000")
    )
}

function renderTables(path){
    console.log(path)
    $.get(path).done(function(response){
        let document=$(response);
        let admin_table = document.find("#admin-table").find("table");
        let order_table = document.find(".order__cards");
        let product_table = document.find("#product-table").find("table");
        $( "#admin-table" ).html(admin_table);
        $( ".order__cards" ).html(order_table);
        $( "#product-table" ).html(product_table);
      });
}