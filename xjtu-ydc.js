// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        http://202.117.17.144/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=17.144
// @grant        none
// ==/UserScript==

(function() {
    document.getElementById("reserve").style.display = "block";
    var u = window.location.href;
    $(document).click(function(e){
            var id=e.target.id;
            console.log(id);
            if(id=="reserve"){
            if(u.includes('setNoPrice')){
            document.getElementById("reserve").attachEvent=("onclick",applySeat());
            }
            if(u.includes('order')){
            document.getElementById("reserve").attachEvent=("onclick",yzmWindow());
            }



            }
    });
function applySeat() {
	var num = Number($('.tip-number .red').text())/Number($('#daynum').text());

	if (num > 0) {
		loadInfo("锁定"+typename+"", "正在为您锁定"+typename+".....请勿刷新页面！");
		var model = {};
		var seats = $('span[id^=s_]');
		var seatid = [];
		$.each(seats, function(i, item) {
			seatid.push($(item).attr('id').split('_')[1]);
		})
		var stock = {};
		var stockids = $('#stockid').val().split(',');
		for(var i = 0;i<stockids.length;i++){
			stock[stockids[i]] = num+'';
		}
		model.stock = stock;
		model.address = $('#serviceid').val();
		model.stockdetailids = seatid.join(',');
//		alert(JSON.stringify(model));
//		model.stockid = $('#stockid').val();
//		model.number=num;
//		AjaxPost('/order/book',param1,createSuccess);
		if($('#yuding-method').find(".selected").attr('date') == 'day'){
			var param = {};
			param.serviceid = $('#serviceid').val();
			param.num = seatid.length;
			param.date = $('#s_date').val();

			if($('#s_date').find('.rac').length>0){
				$.each($('#s_date .selected'), function(i, item) {
					param.date = $(item).text();
				});
			}
			if ($('#select_date').length>0) {
				param.date = $('#select_date').datebox('getValue');
			}
			var t = $("#extend").find('li');
			var extend = {};
			for (var i = 0; i < t.length; i++) {
				if($('#zbid_'+i).next('input').val()>0){
					extend[$('#zbid_'+i).val()] = $('#zbid_'+i).next('input').val();
				}
			}
			model.extend = extend;
			//AjaxGet('/order/booklimt',param,function(o){
			//	if(o.result == 1){
			//		$('#param').val(JSON.stringify(model));
			//		$('#form1').submit();
			//	}else{
			//		info(o.message);
			//	}
			//},'json');
			$('#param').val(JSON.stringify(model));
					$('#form1').submit();
		}else{
			$('#param').val(JSON.stringify(model));
			$('#form1').submit();
		}





	} else {
		info("请选择需要预订的"+typename+"信息！");
	}

}

function yzmWindow(){
	var html = '<div class="typecode" id="typecode">' +
		'<dl class="dl-input sprite code-filed">' +
		'<dd><input type="text" txt="验证码" placeholder="验证码" class="textinput" name="yzm" id="yzm"></dd>' +
		'</dl>' +
		'<span class="code-img"><img onclick="change();" src="'+ $('#contextPath').val() +'/login/yzm'+ $('#ctrlSuffix').val() +'?'+ Math.random() +'" alt="验证码" height="44" width="108" /></span>'+
		'</div>'
	showDialog(600, 300, 169, '填写验证码', true, html, 200);
	$('.dialog-foot').html("<button class=\"normal-button-mid button-info\" onclick=\"yzmyz();\">&nbsp;&nbsp;继续预订&nbsp;&nbsp;</button>");

}

})();
