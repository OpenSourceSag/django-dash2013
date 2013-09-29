//UX Functions

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
function onStoryFieldClick(e){
    if($('.story_selected div').length > 0){
        toggleStorySelection($('.story_selected div'));
    }
    toggleStorySelection(e.target);
}


$(function() {
    $('#stories').on('click','div',onStoryFieldClick)

    $('.sprint_number').click(function(){ $(this).parent().find('ul').toggleClass('visible_sprint'); });
    
    
});

