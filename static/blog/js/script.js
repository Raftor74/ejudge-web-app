$(function(){
	
	$(".ejudge_control_btn").click(function(){
		var action = $(this).attr('data-id');
		var csrfmiddlewaretoken = $("input[name$='csrfmiddlewaretoken']").val();
		$.post("/ejudgeaction/",
			{ 'action':action,
			  'csrfmiddlewaretoken':csrfmiddlewaretoken,
			},function(data){
				var info_block = $("#ejudge_control_info");
				info_block.text(data).show(200);
				setTimeout(function(){
					info_block.text("").hide(400);
				}, 4000);
			});
	});

});