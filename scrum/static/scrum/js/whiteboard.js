//UX Functions

function saveStory(projectId, storyField){
    debugger;
}

function saveTask(projectId, taskField){
    debugger;
}

function addSprint(projectId){

}

function sprintAddTask(sprintArea){

}

function sprintDelTask(sprintId, taskId){

}

function saveProject(projectId){

}

function addNewStoryField(){
    // debugger;
    storyUl = $('#stories ul')
    newField = $('<li><input class="whiteboard_field"></input></li>');
    newField.appendTo(storyUl);
    return newField;
}

function addNewTaskField(){
    taskUl = $('#tasks ul')
    newField = $('<li><input class="whiteboard_field"></input></li>');
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
    if(e.which == 13){
        event.preventDefault();
    }
}

function onHeaderFieldChange(e){
    debugger;
}

function onStoryFieldKeydown(e){
    if(e.which == 13){
        event.preventDefault();
        storyField = addNewStoryField();
        storyField.find('input').focus();
    }
}

function onStoryFieldChange(e){
    debugger;
}

function onTaskFieldKeydown(e){
    if(e.which == 13){
        event.preventDefault();
        taskField = addNewTaskField();
        taskField.find('input').focus();
    }
}

function onTaskFieldChange(e){
    debugger;
}

//TODO: Add the sprint drag&drop events

$(function() {
    $('header .whiteboard_field').change(onHeaderFieldChange);
    $('#project_title').keydown(onHeaderFieldKeydown);

    $('#stories').on('change','input',onStoryFieldChange);
    $('#stories').on('keydown','input',onStoryFieldKeydown);

    $('#tasks').on('change','input',onTaskFieldChange);
    $('#tasks').on('keydown','input',onTaskFieldKeydown);
    
});


