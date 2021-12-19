$(document).ready(function () {
	//側邊欄下拉
	$(".menu>.drop--menu>a").click(function(e){
		e.preventDefault();
		$(this).parent().toggleClass("active")
		$(this).parent().siblings().find('ul').slideUp();
		$(this).parent().find("ul").slideToggle();
	});
    

    //字體放大縮小
	$('.font-s').click(function (e) { 
		$('.news-content .article p').css('font-size','14px');
	  });
	
	  $('.font-m').click(function (e) { 
		$('.news-content .article p').css('font-size','18px');
	  });
	
	  $('.font-b').click(function (e) { 
		$('.news-content .article p').css('font-size','20px');
	  });	
	});
	
	$(function () {
		$(".drop--menu>li>a").click(function (e) {
			e.preventDefault();
			$(this).toggleClass("active");
			$(this).parent().find('.menu--drop').slideToggle();
			$(this).parent().siblings().find('.menu--drop').slideUp();
	});
	
});

 