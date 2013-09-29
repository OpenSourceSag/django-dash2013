//Configure ajax and CSRF

// See https://docs.djangoproject.com/en/1.5/ref/contrib/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//UX Functions

function saveStory(storyField){
    storyId = $(storyField).data('id');
    storyData = {
        title: $(storyField).val(),
        estimated_time: 0
    };
    if (storyId){
        $.ajax({
            type: 'POST',
            url: 'story/'+storyId+'/',
            data: storyData
        }).fail(function(){
            errorMessage('The story could not be saved');
        }); 
    }else{
        $.ajax({
            type: 'POST',
            url: 'story/add/',
            data: storyData
        }).done(function(data){
            $(storyField).data('id', data.story_pk);
        }).fail(function(){
            $(storyField).parent().remove();
            errorMessage('The story could not be saved');
        }); 
    }
}

function saveTask(taskField){
    taskId = $(taskField).data('id');
    taskData = {
        title: $(taskField).val(),
        estimated_time: 0,
        story: 1
    };    
    if (taskId){
        $.ajax({
            type: 'POST',
            url: 'task/'+taskId+'/',
            data: taskData
        }).fail(function(){
            errorMessage('The task could not be saved');
        }); 
    }else{
        $.ajax({
            type: 'POST',
            url: 'task/add/',
            data: taskData
        }).done(function(data){
            $(taskField).data('id', data.task_pk);
        }).fail(function(){
            $(taskField).parent().remove();
            errorMessage('The task could not be added');
        }); 
    }
}

function addSprint(projectId){

}

function sprintAddTask(sprintArea){

}

function sprintDelTask(taskId){

}

function saveProject(){
    projectData = {
        name: $('#project_title').val(),
        description: $('#project_description').val() 
    };
    $.ajax({
        url: 'update/',
        type: 'POST',
        data: projectData
    }).fail(function(){
        errorMessage('The project could not be saved');
    }); 
}

function addNewStoryField(){
    // debugger;
    storyUl = $('#stories ul')
    newField = $('<li><input class="whiteboard_field text_font"></input></li>');
    newField.appendTo(storyUl);
    return newField;
}

function addNewTaskField(){
    taskUl = $('#tasks ul')
    newField = $('<li><span class="glyphicon glyphicon-chevron-right"></span><input class="whiteboard_field text_font"></input></li>');
    newField.appendTo(taskUl);
    return newField;
}

function addNewSprint(){

}

function syncStories(data){

}

function syncTasks(data){

}

function syncSprints(data){

}

function syncProject(){

}

//Events functions
function onHeaderFieldKeydown(e){
    if(e.which == 13 && e.target.value != '' && e.shiftKey == false){
        event.preventDefault();
        storyField = addNewStoryField();
        storyField.find('input').focus();
    }
}

function onHeaderFieldChange(e){
    saveProject();
}

function onStoryFieldKeydown(e){
    if(e.which == 13 && e.target.value != ''){
        event.preventDefault();
        storyField = addNewStoryField();
        storyField.find('input').focus();
    }
}

function onStoryFieldChange(e){
    saveStory(e.target);
}

function onTaskFieldKeydown(e){
    if(e.which == 13 && e.target.value != ''){
        event.preventDefault();
        taskField = addNewTaskField();
        taskField.find('input').focus();
    }
}

function onTaskFieldChange(e){
    saveTask(e.target);
}


$(function() {
    $('header .whiteboard_field').change(onHeaderFieldChange);
    $('header .whiteboard_field').keydown(onHeaderFieldKeydown);

    $('#stories').on('change','input',onStoryFieldChange);
    $('#stories').on('keydown','input',onStoryFieldKeydown);

    $('#tasks').on('change','input',onTaskFieldChange);
    $('#tasks').on('keydown','input',onTaskFieldKeydown);
    
    $("#tasks li").draggable({
        appendTo: "body",
        helper: "clone"
    });
    $(".sprint_tasks").droppable({
        activeClass: "ui-state-default",
        hoverClass: "ui-state-hover",
        accept: ":not(.ui-sortable-helper)",
        drop: function( event, ui ) {
            $(this).find(".placeholder").remove();
            var text = ui.draggable.find('input').val();
            var id = ui.draggable.find('input').data('id');
            var sprintId = $(this).data('id')
            if (id != undefined && $( this ).find("li[data-id='"+id+"']").length == 0){
                var sprintTaskTag = $( "<li></li>" ).text( text ).data('id', id).appendTo( this );
                $.ajax({
                    method: 'POST',
                    url: 'sprint-task/add/',
                    data: {
                        task: id,
                        sprint: sprintId
                    }
                }).fail(function(){
                    sprintTaskTag.remove();
                    errorMessage('Unable to add the task to the specified sprint');
                });
            }else{
                //Display Message
                errorMessage('You cannot add task that is already in the sprint');
            }
        }
    });
});

