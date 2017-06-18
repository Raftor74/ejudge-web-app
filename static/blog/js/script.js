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

	$(".reg_to_contest").click(function(){
		var contest_id = $(this).attr('data-id');
		var csrfmiddlewaretoken = $("input[name$='csrfmiddlewaretoken']").val();
		$.post("/contests/",
			{ 'contest_id':contest_id,
			  'csrfmiddlewaretoken':csrfmiddlewaretoken,
			},function(data){
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
				location.reload();
			});
		}
	});

	$(".delete_user").click(function(){
		if (confirm("Удалить пользователя?")){
			var user_id = $(this).attr('data-id');
			var csrfmiddlewaretoken = $("input[name$='csrfmiddlewaretoken']").val();
			$.post("/ejudgeusers/",
				{ 'user_id':user_id,
				  'delete_user':'delete',
				  'csrfmiddlewaretoken':csrfmiddlewaretoken,
				},function(data){
					location.reload();
				});
		}
	});

	//Validate Form Ejudge Registration
	$("#ejudge-registration-form").submit(function(){
		data = $(this).serializeArray();
		form_fields = convSerialazeToArray(data);
		error = false;
		error_log = [];
		if (form_fields['reg_login'].length < 3 || form_fields['reg_login'].length > 30){
			$("input[name='reg_login']").parent().removeClass("has-error").addClass("has-error");
			error_log.push("Логин должен быть от 5 до 30 символов")
			error = true;
		}
		
		if (form_fields['reg_password'].length < 5 || form_fields['reg_password'].length > 30){
			$("input[name='reg_password']").parent().removeClass("has-error").addClass("has-error")
			error_log.push("Пароль должен быть от 5 до 30 символов")
			error = true;
		}

		if (!form_fields['reg_email']){
			$("input[name='reg_email']").parent().removeClass("has-error").addClass("has-error")
			error_log.push("Email не должен быть пустым")
			error = true;
		}

		if (form_fields['reg_password'] != form_fields['reg_password_2']){
			$("input[name='reg_password_2']").parent().removeClass("has-error").addClass("has-error")
			$("input[name='reg_password']").parent().removeClass("has-error").addClass("has-error")
			error_log.push("Пароли не совпадают")
			error = true;
		}

		if (error){
			$('#myModal').find(".modal-body").html(printErrors(error_log));
			$('#myModal').modal('toggle');
			return false;
		}

	});

	//Validate Form Ejudge Login
	$("#ejudge-login-form").submit(function(){
		data = $(this).serializeArray();
		form_fields = convSerialazeToArray(data);
		error_log = [];
		error = false;
		if (!form_fields['login']){
			$("input[name='login']").parent().removeClass("has-error").addClass("has-error");
			error_log.push("Логин не должен быть пустым")
			error = true;
		}
		
		if (!form_fields['password']){
			$("input[name='password']").parent().removeClass("has-error").addClass("has-error")
			error_log.push("Пароль не должен быть пустым")
			error = true;
		}

		if (error){
			$('#myModal').find(".modal-body").html(printErrors(error_log));
			$('#myModal').modal('toggle');
			return false;
		}

	});

	//return map from serialaze form
	function convSerialazeToArray(serialaze){
		form_fields = {}
		$.each(serialaze,function( index, value ){
			form_fields[value['name']] = value['value'];
		});
		return form_fields;
	}

	function printErrors(error_array){
		text = "";
		for (var i = 0; i < error_array.length; i++){
			text += "</br><p>" + error_array[i] + "</p></br>"
		}
		return text;
	}
});