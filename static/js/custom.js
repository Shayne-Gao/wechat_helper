function item_click(value) {
        var form1 = $("#form1");
        var item = $("#item").val();
        if (value == 1) {          
            form1.action = "./wf/price";
             $("#form1").attr("action",form1.action);
            form1.submit();
        }
        if (value == 2) {
            form1.action = "./wf/build";
            $("#form1").attr("action", form1.action);
            form1.submit();
        }
 }


(function ($) {
    "use strict";
    var mainApp = {
       
        reviews_fun:function()
        {
            ($)(function () {
                $('#carousel-example').carousel({
                    interval: 3000 //TIME IN MILLI SECONDS
                });
            });

        },
     
        custom_fun:function()
        {


            /*====================================
             WRITE YOUR   SCRIPTS  BELOW
            ======================================*/
            $("#header").load("/static/html/header.html");
        }

    }
   
   
    $(document).ready(function () {
        mainApp.reviews_fun();
        mainApp.custom_fun();

    });
}(jQuery));


