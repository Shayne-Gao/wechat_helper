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
// ro 计算器相关
            $("input#ro_begin").change(function(){
                var begin = $(this).val();
                var timestamp = Date.parse(new Date());
                document.getElementById("ro_start_time").innerHTML=timestamp/1000
                console.log(timestamp)
            });
            $("input#ro_end").change(function(){
                var end_z = $(this).val();
                var start_z = $("input#ro_begin").val()
                var start_1 =  $("input#ro_begin_1").val()
                var start_2 =  $("input#ro_begin_2").val()
                var start_3 =  $("input#ro_begin_3").val()

                var end_1 =  $("input#ro_end_1").val()
                var end_2 =  $("input#ro_end_2").val()
                var end_3 =  $("input#ro_end_3").val()

                var price_1 = $("input#ro_price_1").val()
                var price_2 = $("input#ro_price_2").val()
                var price_3 = $("input#ro_price_3").val()

                var startTimeStamp = document.getElementById("ro_start_time").innerHTML
                var endTimeStamp  = Date.parse(new Date()) / 1000;
                document.getElementById("ro_end_time").innerHTML=endTimeStamp
                var timePass = endTimeStamp - startTimeStamp
                var perSec =  ( (end_z - start_z) + (end_3-start_3)*price_3 +(end_2-start_2)*price_2 + (end_1-start_1)*price_1 ) / timePass
                document.getElementById("ro_per_min").innerHTML = Math.round(perSec * 60)
                document.getElementById("ro_per_100min").innerHTML = Math.round(perSec * 60 * 60)
                document.getElementById("ro_per_300min").innerHTML = Math.round(perSec * 60 * 300)
                document.getElementById("ro_per_500min").innerHTML = Math.round(perSec * 60 * 400)
                console.log(start+'|'+end+'|'+startTimeStamp+ '= '+ perSec)
            });
        }

    }
   
   
    $(document).ready(function () {
        mainApp.reviews_fun();
        mainApp.custom_fun();

    });
}(jQuery));


