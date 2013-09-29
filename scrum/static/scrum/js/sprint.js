function setTaskStatus(taskId, status, postIt){
    if($.inArray(status, ['TO', 'IN', 'PR', 'DO', 'BA']) > -1){
        $.ajax({
            method: 'POST',
            url: '/task/'+taskId+'/update-status/',
            data: {
               status: status
            }
        }).done(function(data){
            if(data.error_message){
            errorMessage(data.error_message);
            $(postIt).remove();}
        }).fail(function(){
            $(postIt).remove();
            errorMessage('Unable to change the status of the task');
        });
        
        
    }
}


function CloseSprint(sprintId)
{
    $.ajax({
            method: 'POST',
            url: '/sprint/'+sprintId+'/close/',
            data: {}
        }).done(function(data){
            if(data.error_message){
                errorMessage(data.error_message);
            }else{
                document.getElementById('sprint-close-button').style.display = "none";
            }
        }).fail(function(){
            errorMessage('Unable to close this sprint');
        });
}

$(function() {
    $("li").draggable({
        appendTo: "body",
        helper: "clone"
    });
    $("#todo ul").droppable({
        activeClass: "ui-state-default",
        hoverClass: "ui-state-hover",
        accept: ":not(.ui-sortable-helper)",
        drop: function( event, ui ) {
            $(this).find(".placeholder").remove();
            var id = ui.draggable.find('.post-it').data('id');
            var postItTag = ui.draggable.appendTo( this );
            setTaskStatus(id, 'TO', postItTag);
        }
    });
    $("#doing ul").droppable({
        activeClass: "ui-state-default",
        hoverClass: "ui-state-hover",
        accept: ":not(.ui-sortable-helper)",
        drop: function( event, ui ) {
            $(this).find(".placeholder").remove();
            var id = ui.draggable.find('.post-it').data('id');
            var postItTag = ui.draggable.appendTo( this );
            setTaskStatus(id, 'IN', postItTag);
        }
    });
    $("#done ul").droppable({
        activeClass: "ui-state-default",
        hoverClass: "ui-state-hover",
        accept: ":not(.ui-sortable-helper)",
        drop: function( event, ui ) {
            $(this).find(".placeholder").remove();
            var id = ui.draggable.find('.post-it').data('id');
            var postItTag = ui.draggable.appendTo( this );
            setTaskStatus(id, 'DO', postItTag);
        }
    });
    $("#bug ul").droppable({
        activeClass: "ui-state-default",
        hoverClass: "ui-state-hover",
        accept: ":not(.ui-sortable-helper)",
        drop: function( event, ui ) {
            $(this).find(".placeholder").remove();
            var id = ui.draggable.find('.post-it').data('id');
            var postItTag = ui.draggable.appendTo( this );
            setTaskStatus(id, 'PR', postItTag);
        }
    });
    $("#backlog ul").droppable({
        activeClass: "ui-state-default",
        hoverClass: "ui-state-hover",
        accept: ":not(.ui-sortable-helper)",
        drop: function( event, ui ) {
            $(this).find(".placeholder").remove();
            var id = ui.draggable.find('.post-it').data('id');
            var postItTag = ui.draggable.appendTo( this );
            setTaskStatus(id, 'BA', postItTag);
        }
    });
});
