from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import Project, Story, Task, Sprint, SprintTasks

class WhiteBoardView(TemplateView):
    template_name = 'scrum/whiteboard.html'


class WhiteBoardView(DetailView):
    template_name = 'scrum/whiteboard.html'
    model = Project
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(WhiteBoardView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        project = kwargs.get('object')
        project_stories = Story.objects.filter(project=project)
        project_tasks = Task.objects.filter(story__in=project_stories)
        
        
        context['stories'] = project_stories
        context['tasks'] = project_tasks
        
        return context