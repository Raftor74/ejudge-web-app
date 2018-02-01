$(function(){
	
	/*$(".ejudge_control_btn").click(function(){
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

	$(".reg_to_contest").click(function(){
		var contest_id = $(this).attr('data-id');
		var csrfmiddlewaretoken = $("input[name$='csrfmiddlewaretoken']").val();
		$.post("/contests/",
			{ 'contest_id':contest_id,
			  'csrfmiddlewaretoken':csrfmiddlewaretoken,
			},function(data){
				console.log(data)
				location.reload();
			});
	});

	$(".delete_contest").click(function(){
		if (confirm("Удалить контест?")){
		var contest_id = $(this).attr('data-id');
		var csrfmiddlewaretoken = $("input[name$='csrfmiddlewaretoken']").val();
		$.post("/contests/",
			{ 'contest_id':contest_id,
			  'delete_contest':'delete',
			  'csrfmiddlewaretoken':csrfmiddlewaretoken,
			},function(data){
		        console.log(data)
				location.reload();
			});
		}
	});*/
});