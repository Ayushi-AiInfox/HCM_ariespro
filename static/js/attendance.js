
    $("#absent1{{forloop.counter}}").click(function(){
        // $(".days" + val1).css("background", "#EE4B2B");
        // $(".days" + val1).css("color", "#fff");
        $("#days_bg").val("#EE4B2B");
        $("#days_color").val("#fff");
        $("#values").val("{{i.user}},1");
        console.log($("#values").val("{{i.user}},1,absent"));
    });
    // console.log("{{month_list}}")
    // console.log("{{month}}")
    if('{{month}}' == 1){
        document.getElementById('month').value = "January";
    }
    if('{{month}}' == 2){
        document.getElementById('month').value = "February";
        if('{{leapyear}}' == 0){
            $(".days29{{forloop.counter}}").hide();
            $(".days30{{forloop.counter}}").hide();
            $(".days31{{forloop.counter}}").hide();
        }else if('{{leapyear}}' == 1){  
            $(".days30{{forloop.counter}}").hide();
            $(".days31{{forloop.counter}}").hide();                                              
        }
    }
    if('{{month}}' == 3){
        document.getElementById('month').value = "March";
    }
    if('{{month}}' == 4){
        document.getElementById('month').value = "April";
        $(".days31{{forloop.counter}}").hide();
    }
    if('{{month}}' == 5){
        document.getElementById('month').value = "May";
    }
    if('{{month}}' == 6){
        document.getElementById('month').value = "June";
        $(".days31{{forloop.counter}}").hide();
    }
    if('{{month_list}}' == 7){
        document.getElementById('month').value = "July";
    }
    if('{{month_list}}' == 8){
        document.getElementById('month').value = "August";
    }
    if('{{month_list}}' == 9){

        document.getElementById('month').value = "September";
        $(".days31{{forloop.counter}}").hide();
    }
    if('{{month_list}}' == 10){
        document.getElementById('month').value = "October";
    }
    if('{{month_list}}' == 11){
        document.getElementById('month').value = "November";
        $(".days31{{forloop.counter}}").hide();
    }
    if('{{month_list}}' == 12){
        document.getElementById('month').value = "December";
    }