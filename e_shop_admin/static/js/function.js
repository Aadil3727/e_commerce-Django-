$(document).on("click",".add-to-wishlist",function(){
    let product = $(this).attr("data-prooduct-item")
    let this_val = $(this)
  
    console.log("My pro id",product);
  
    $.ajax({
        url:"add-to-wishlist/",
        data:{
            "id": product
        },
        dataType:"json",
        beforeSend: function(){
            console.log("Added to wishlist");
           
        },
        success:function(response){
            this_val.html("✓")
            if(response.bool == true) {
                console.log("added");
            }
        }
    })
  });