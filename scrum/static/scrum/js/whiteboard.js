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
    storyId = $('.story_selected input').data('id');
    taskData = {
        title: $(taskField).val(),
        estimated_time: 0,
        story: storyId
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
    if($('.empty-story').length == 0){
        newField = $('<li class="empty-story"><input class="whiteboard_field text_font"></input></li>');
        newField.appendTo(storyUl);
        return newField;
    }else{
        return $('.empty-story');
    }
}

function addNewTaskField(){
    taskUl = $('#tasks ul')
    if($('.empty-task').length == 0){
        newField = $('<li class="empty-task visible_task"><span class="glyphicon glyphicon-chevron-right"></span><input class="whiteboard_field text_font"></input></li>');
        newField.appendTo(taskUl);
        return newField;
    }else{
        return $('.empty-task');
    }
}

function addNewSprint(){
    $.ajax('sprint/add/').done(function(data){
        $('<li><div>Sprint #'+data.number+'<div><ul data-id="'+data.id+'" class="sprint_tasks visible_sprint"><li>The sprint is empty. Put some gaz!</li></ul></li>').appendTo($('#sprints ul'));
        $('#sprints li').remove(':contains(No sprints here)');
    }).fail(function(){
        errorMessage('Unable to create a new sprint');
    });
}

function syncStories(data){

}

function syncTasks(data){

}

function syncSprints(data){

}

function syncProject(){

}

function toggleStorySelection(element){
    $(element).parent().toggleClass('story_selected');
    $('.empty-task').toggleClass('visible_task');
    $("li[data-story='"+$(element).data('id')+"']").toggleClass('visible_task');
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
        $(e.target).parent().removeClass('empty-story');
        storyField = addNewStoryField();
        storyField.find('input').focus();
    }
}

function onStoryFieldFocus(e){
    if($('.story_selected input').length > 0){
        toggleStorySelection($('.story_selected input'));
    }
    toggleStorySelection(e.target);
}

function onStoryFieldChange(e){
    saveStory(e.target);
}

function onTaskFieldKeydown(e){
    if(e.which == 13 && e.target.value != ''){
        event.preventDefault();
        $(e.target).parent().removeClass('empty-task');
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
    $('#stories').on('focus','input',onStoryFieldFocus);

    $('#tasks').on('change','input',onTaskFieldChange);
    $('#tasks').on('keydown','input',onTaskFieldKeydown);

    $('#add_sprint').click(addNewSprint);

    $('.sprint_number').click(function(){ $(this).parent().find('ul').toggleClass('visible_sprint'); });
    
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
                ui.draggable.remove();
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

