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
//初始化时间空间

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
            $("select#change_cate_select").change(function(){
                var cateName = $(this).val();
                var rid = $(this).attr("rid");
                var url = '../change_type?type_name='+cateName+'&rid='+rid
                $.ajax({
        url:url,
        dateType: "json",
        success:function(ret){
                   console.log(ret.res);
                }});
            });
        }

    }
   
   
    $(document).ready(function () {
        mainApp.reviews_fun();
        mainApp.custom_fun();

    });
}(jQuery));


