var problems = [];
var load_problems_url = "/contests/getproblemslist/";

// Преобразует
function parseDurationTime(timestring) {
    var time = timestring.split(":");
    var hourses = parseInt(time[0]);
    var minutes = parseInt(time[1]);
    var seconds = parseInt(time[2]);
    return hourses * 60 + minutes;
}

// Подготавливает данные формы к отправке
function prepareContestForm(formData) {
    var toPost = {};
    var tasks = [];
    $.each(formData, function (i, elem) {
        switch (elem.name){
            case 'task_id':
                tasks.push({id:elem.value});
                break;
            case 'duration':
                var minutes = parseDurationTime(elem.value);
                toPost[elem.name] = minutes;
                break;
            default:
                toPost[elem.name] = elem.value;
                break;
        }
    });
    if (tasks.length) {
        toPost["tasks"] = JSON.stringify(tasks);
    } else {
        toPost["tasks"] = [];
    }

    return toPost;
}

// Деактивирует / Активирует проблему из списка при выборе
function setProblemActive(id, active) {
    $.each(problems, function (i, elem) {
       if (parseInt(elem.id) == parseInt(id))
       {
           elem.active = active;
       }
    });
}

// Добавляет задачу в список
function addTaskInList(value) {
    if (value.item) {
        var container = $('#contest-problems-list');
        var task_id = value.item.id;
        setProblemActive(task_id, false);
        var task_name = value.item.label;
        var template = '<li class="list-group-item">'
        + '<input type="hidden" name="task_id" value="'+task_id+'">'
        + '<span>'+task_name+'</span>'
        + '<button type="button" class="close task-delete" data-id="'+task_id+'" aria-label="Close">'
        + '<span aria-hidden="true">&times;</span>'
        + '</button>'
        + '</li>';
        container.append(template);
    }
}

// Получает список всех задач
function uploadProblems() {
    var csrfmiddlewaretoken = $("input[name$='csrfmiddlewaretoken']").val();
    $.post(load_problems_url,{
        "csrfmiddlewaretoken": csrfmiddlewaretoken
    },function(callback) {
       if (callback) {
           try {
               problems = JSON.parse(callback);
               console.log("Problems upload: SUCCESS");
           } catch(e){
               console.error("Problems upload: FAIL");
           }
       } else {
           console.error("Problems upload: FAIL");
       }
    });
}

$(document).ready(function () {
    uploadProblems();

    // Устанавливает поле даты для даты проведения соревнования
    $('#contest-sched-time').datetimepicker({
        lang:"ru",
        minTime: new Date,
        format:'Y/m/d H:i:00',
        step: 5,
        minDate: new Date,
        onSelectDate: function(ct, $i) {
          this.setOptions({
            minTime: ct.getTime() > new Date ? false : 0
          });
        }
    });

    // Устанавливает поле для выбора длительности соревнования
    $('#contest-duration').datetimepicker({
        datepicker:false,
        format: 'H:i:00',
        step: 5,
    });

    // Автоподстановка задач
    $('#contest-tasks-input').autocomplete({
        source: function (request, response) {
            var needle = request.term;
            var pattern = new RegExp(needle, "i");
            var items = $.map(problems, function (elements) {
                var fio = elements.value;
                var active = elements.active;
                if (pattern.test(fio) && active) {
                    return elements;
                }
            });
            response(items);
        },
        minLength: 1,
        delay: 300, // Задержка запроса (мсек), на случай, если мы не хотим слать миллион запросов, пока пользователь печатает.
        select: function (data, value) {
            $(this).val("");
            addTaskInList(value);
            return false;
        },
    });

    // Удаляет задачу из списка
    $(document).on("click", ".task-delete", function (event) {
        event.preventDefault();
        var task_id = $(this).data('id');
        setProblemActive(task_id, true);
        $(this).parent().remove();
    });

    // Действие при отправке формы
    $('#js-contest-add-from').submit(function(event){
        event.preventDefault();
        var $form = $(this);
        var url = $form.attr('action');
        var formData = $form.serializeArray();
        var postData = prepareContestForm(formData);

        $.post(url, postData, function (callback) {
            if(callback.status == "ok")
            {
                document.location.href = '/contests/list/';
            }
            else
            {
                alert("Ошибка создания контеста");
            }
        });
        return false;
    });

    // Действие при отправке формы
    $('#js-contest-edit-from').submit(function(event){
        event.preventDefault();
        var $form = $(this);
        var url = $form.attr('action');
        var formData = $form.serializeArray();
        var postData = prepareContestForm(formData);
        $.post(url, postData, function (callback) {
            if(callback.status == "ok")
            {
                document.location.href = '/contests/list/';
            }
            else
            {
                alert("Ошибка обновления контеста");
            }
        });
        return false;
    });

});