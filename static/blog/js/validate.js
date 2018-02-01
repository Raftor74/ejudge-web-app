$(document).ready(function () {

    //Валидация для формы регистрации
	$("#registration-form").submit(function(){
		var data = $(this).serializeArray();
		var form_fields = convSerialazeToArray(data);
        var error = false;
		var login_length = form_fields['login'].length;
		var password_length = form_fields['password'].length;

		if (!(login_length < 30 && login_length > 5)) {
		    $("input[name='login']").parent().removeClass('has-error').addClass('has-error');
		    error = true;
        }

		if (!(password_length < 30 && password_length > 5)) {
		    $("input[name='password']").parent().removeClass('has-error').addClass('has-error');
		    error = true;
        }

        if (form_fields['password_again'] !== form_fields['password']) {
		    $("#password_again_error").html("Пароли не совпадают");
            $("input[name='password_again']").parent().removeClass('has-error').addClass('has-error');
		    error = true;
        }

        if (error)
            return false;

	});

	//Преобразует данные с формы в ассоциативный массив (объект)
	function convSerialazeToArray(serialaze){
		var form_fields = {}
		$.each(serialaze, function( index, value ){
			form_fields[value['name']] = value['value'];
		});
		return form_fields;
	}

});