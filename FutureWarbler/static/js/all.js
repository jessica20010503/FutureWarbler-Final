$(document).ready(function () {
    var t = $("#quantity");
	$("#add").click(function(){
		t.val(parseInt(t.val())+1);
		$("#min").removeAttr("disabled");                 //當按加1時，解除$("#min")不可讀狀態
		setTotal();
	})
	$("#min").click(function(){
               if (parseInt(t.val())>1) {                     //判斷數量值大於1時才可以減少
                t.val(parseInt(t.val())-1)
                }else{
                $("#min").attr("disabled","disabled")        //當$("#min")為1時，$("#min")不可讀狀態
               }
		setTotal();
	})
	function setTotal(){
		$("#total").html((parseInt(t.val())*3.95).toFixed(2));
	}
	setTotal();

    //停損停利
    var t = $("#stopquantity");
	$("#stopadd").click(function(){
		t.val(parseInt(t.val())+1);
		$("#stopmin").removeAttr("disabled");                 //當按加1時，解除$("#min")不可讀狀態
		setTotal();
	})
	$("#stopmin").click(function(){
               if (parseInt(t.val())>15000) {                     //判斷數量值大於1時才可以減少
                t.val(parseInt(t.val())-1)
                }else{
                $("#stopmin").attr("disabled","disabled")        //當$("#min")為1時，$("#min")不可讀狀態
               }
		setTotal();
	})
	function setTotal(){
		$("#total").html((parseInt(t.val())*3.95).toFixed(2));
	}
	setTotal();
});