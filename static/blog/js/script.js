$(function(){


    // Регистрация пользователя на соревнование
    $(".reg-to-contest").click(function(){
        var url = "/contests/";
		var contest_id = $(this).attr('data-id');
		var csrfmiddlewaretoken = $("input[name$='csrfmiddlewaretoken']").val();
		var data = {
		    'registration': true,
		    'contest_id': contest_id,
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
        };

		$.post(url, data, function(callback){
		    if (callback.success) {
		        if (callback.success == "ok"){
		            console.log("Contest added");
		            location.reload();
                } else {
		            console.error("Contest register error: " + callback.error)
                }

            } else {
		        console.error("Contest register error: null response");
            }
        });

	    return false;
	});

    // Кнопки для управления системой Ejudge
	$(".ejudge_control_btn").click(function(){
		var url = "/profile/";
		var action = $(this).attr('data-id');
		var csrfmiddlewaretoken = $("input[name$='csrfmiddlewaretoken']").val();
		var data = {
			'action': action,
	  		'csrfmiddlewaretoken': csrfmiddlewaretoken,
		};

		$.post(url, data, function(callback){
		    if (callback.text) {
		        var text = callback.text;
		        var $info_block = $("#ejudge_control_info");
				$info_block.text(text).show(200);
				setTimeout(function(){
					$info_block.text("").hide(400);
				}, 4000);
            }
		});
	});


	/*
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