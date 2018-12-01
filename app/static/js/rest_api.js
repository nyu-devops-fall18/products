$(function() {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_description").val(res.description);
        $("#product_category").val(res.category);
        $("#product_price").val(res.price);
        $("#product_condition").val(res.condition);
        $("#product_inventory").val(res.inventory);
        $("#product_review").val(res.review);
        $("#product_rating").val(res.rating);

    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_description").val("");
        $("#product_category").val("");
        $("#product_price").val("");
        $("#product_condition").val("");
        $("#product_inventory").val("");
        $("#product_review").val("");
        $("#product_rating").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }


     //****************************************
     //Rate a Product
     //****************************************

    $("#rating-btn").click(function () {

        var product_id = $("#product_id").val();
        var newrating = $("#product_rating").val();
        console.log(product_id)
        console.log(newrating)
        query = ""
        if(product_id){
            query += "id=" + product_id
            if(newrating){
                query += "&stars=" + newrating
            }
        }
        console.log(query)

        var ajax = $.ajax({
                type: "PUT",
                url: "/products/rating?" + query,
                contentType:"application/json",
                data: ''
            })

        ajax.done(function(res){
         // update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#product_name").val();
        var description = $("#product_description").val();
        var category = $("#product_category").val();
        var price = $("#product_price").val();
        var condition = $("#product_condition").val();
        var inventory = $("#product_inventory").val();
        var review = $("#product_review").val();
        var rating = $("#product_rating").val();

        var data = {
            "name": name,
            "description": description,
            "category": category,
            "price": price,
            "condition": condition,
            "inventory": inventory,
            "review": review,
            "rating": rating
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {

        var product_id = $("#product_id").val();

        var name = $("#product_name").val();
        var description = $("#product_description").val();
        var category = $("#product_category").val();
        var price = $("#product_price").val();
        var condition = $("#product_condition").val();
        var inventory = $("#product_inventory").val();
        var review = $("#product_review").val();
        var rating = $("#product_rating").val();

        var data = {
            "name": name,
            "description": description,
            "category": category,
            "price": price,
            "condition": condition,
            "inventory": inventory,
            "review": review,
            "rating": rating
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/products/" + product_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {

        var product_id = $("#product_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/products/" + "1",
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        var product_id = $("#product_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/products/" + "2",
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
//            flash_message("Product with ID [" + product_id + "] has been Deleted!")
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#product_name").val();
        var description = $("#product_description").val();
        var category = $("#product_category").val();
        var price = $("#product_price").val();
        var condition = $("#product_condition").val();
        var inventory = $("#product_inventory").val();
        var review = $("#product_review").val();
        var rating = $("#product_rating").val();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (description) {
            queryString += 'description=' + description
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (price) {
            queryString += 'price=' + price
        }
        if (condition) {
            queryString += 'condition=' + condition
        }
        if (inventory) {
            queryString += 'inventory=' + inventory
        }
        if (review) {
            if (queryString.length > 0) {
                queryString += '&review=' + review
            } else {
                queryString += 'review=' + review
            }
        }
        if (rating) {
            queryString += 'rating=' + rating
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/products?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Description</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:40%">Price</th>'
            header += '<th style="width:40%">Condition</th>'
            header += '<th style="width:40%">Inventory</th>'
            header += '<th style="width:40%">Review</th>'
            header += '<th style="width:40%">Rating</th>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                product = res[i];
                var row = "<tr><td>"+product.id+"</td><td>"+product.name+"</td><td>"+"</td><td>"+product.description+"</td><td>"+"</td><td>"+product.category+"</td><td>"+product.price+"</td><td>"+product.condition+"</td></td>"+"</td><td>"+product.inventory+
                "</td><td>"+"</td><td>"+product.review+"</td><td>"+"</td><td>"+product.rating+"</td><tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})


