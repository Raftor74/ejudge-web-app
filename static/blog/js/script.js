
// Подготавливает данные для добавления задачи
function prepareFormData(formData) {
    var toPost = {};
    var input_output = [];
    var last_input = "";
    var last_output = "";
    $.each(formData, function (i, elem) {
        if (elem.name == 'task_input[]')
        {
            last_input = elem.value;
        }
        if (elem.name == 'task_output[]')
        {
            if (last_input != "")
                last_output = elem.value;
            else
                last_output = "";
        }
        if (elem.name != 'task_input[]' && elem.name != 'task_output[]')
        {
            toPost[elem.name] = elem.value;
        }

        if (last_input != "" && last_output != "")
        {
           var data = {'input':last_input, 'output':last_output};
           input_output.push(data);
           last_input = "";
           last_output = "";
        }
    });
    toPost["input_output"] = JSON.stringify(input_output);
    return toPost;
}

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

	// Добавление строки при создании задач (Ввод-вывод)
    $(document).on('click','#task-add-input-output-col', function () {
        // Блок куда будем добавлять строку
        var $block = $('.input-output-block').last();
        var $elem = '<tr class="input-output-block"><td>' +
            '<textarea class="form-control vresize task-input" rows="2" name="task_input[]"></textarea>' +
            '</td>' +
            '<td>' +
            '<textarea class="form-control vresize task-output" rows="2" name="task_output[]"></textarea>' +
            '</td></tr>';
        $block.after($elem);
        return false;
    });

    $('#task-add-btn').click(function () {
        var url = '/problems/add/';
        var $form = $('#task-add-form');
        var formData = $form.serializeArray();
        var postData = prepareFormData(formData);
        $.post(url, postData, function (callback) {
            if(callback.status == "ok")
            {
                document.location.reload();
            }
            else
            {
                alert("Ошибка создания задачи");
            }
        });
        return false;
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