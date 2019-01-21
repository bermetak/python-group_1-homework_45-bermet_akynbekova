function deleteFood(event) {
    event.preventDefault()

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    var csrftoken = getCookie('csrftoken');


    let orderFoodPk = $(this).data('pk');
    let url = $(this).attr('href');
    $('#food_form').off('submit');
    $.ajax({
        url: url,
        method: 'DELETE',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: {
            pk: orderFoodPk,
            csrfmiddlewaretoken: csrftoken
        },
        success: function (response, status) {
            console.log(response);
            console.log(status);
            let orderFoodPk = response.pk;
            let foodElement = $('#order_food_' + orderFoodPk);
            foodElement.remove()
        },
        error: function (response, status) {
            console.log(response);
            console.log(status)
        }
    });
    $('#food_edit').modal('hide');
};


function editFood(event) {
    event.preventDefault();
    $("#food_edit .modal-title").text('Изменить блюдо');
    $("#food_submit").text('Изменить');
    let foodForm = $('#food_form');
    foodForm.off('submit');
    foodForm.attr('action', $(this).attr('href'));
    let foodPk = $(this).data('pk');
    let foodName = $('#order_food_name_' + foodPk);
    let foodAmount = $('#order_food_amount_' + foodPk);

    $('#id_food').val(foodName.data('food_pk'));
    $('#id_amount').val(foodAmount.text());


    $('#food_submit').on('click', function (e) {
        e.preventDefault();

        let url = $('#food_form').attr('action');
        let data = {
            food: $('#id_food').val(),
            amount: $('#id_amount').val(),
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        };
        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            success: function (response, status) {
                console.log(response);
                console.log(status);
                let pk = response.pk;
                let food_name_span = $('#order_food_name_' + pk);
                food_name_span.text(response.food_name);
                food_name_span.data('food_pk', response.food_pk);
                $('#order_food_amount_' + pk).text(response.amount);
                $('#food_edit').modal('hide');
            },
            error: function (response, status) {
                console.log(response);
                console.log(status)
            }
        });

    });
    $('#food_edit').modal('show');
};


function orderFoodAdd(event) {
    event.preventDefault();
    $("#food_edit .modal-title").text('Добавить блюдо');
    $("#food_submit").text('Добавить');
    let foodForm = $('#food_form');
    foodForm.attr('action', $(this).attr('href'));
    $('#id_food').val('');
    $('#id_amount').val('');
    foodForm.off('submit');
    $('#food_submit').on('click', function (e) {
        $.ajax($('#food_form').attr('action'), {
            type: 'POST',
            data: {
                food: $('#id_food').val(),
                amount: $('#id_amount').val(),
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response, status) {
                console.log(response);
                console.log(status);

                let newFoodLi = $('<li></li>');

                let foodNameSpan = $('<span></span>')
                    .attr('id', 'order_food_name_' + response.pk)
                    .data('food_pk', response.pk)
                    .text(response.food_name);
                let foodAmountSpan = $('<span></span>')
                    .attr('id', 'order_food_amount_' + response.pk)
                    .text(response.amount);
                let editLink = $('<a></a>')
                    .addClass('edit_link')
                    .attr('href', response.edit_url)
                    .data('pk', response.pk)
                    .text('Изменить');

                let deleteLink = $('<a></a>')
                    .addClass('delete_link')
                    .attr('href', response.delete_url)
                    .text('Удалить');

                newFoodLi
                    .attr('id', 'order_food_' + response.pk)
                    .append(foodNameSpan)
                    .append(document.createTextNode(': '))
                    .append(foodAmountSpan)
                    .append(document.createTextNode(' шт. ('))
                    .append(editLink)
                    .append(document.createTextNode(' / '))
                    .append(deleteLink)
                    .append(document.createTextNode(')'));

                $('#order_food_list').append(newFoodLi);

                $('#food_edit').modal('hide');

            },
            error: function (response, status) {
                console.log(response);
                console.log(status)
            }
        })

    });
    $('#food_edit').modal('show');
}


window.addEventListener('load', function () {
    $("#order_food_add_link").click(orderFoodAdd);
    $('.edit_link').click(editFood);
    $('.delete_link').click(deleteFood)
});