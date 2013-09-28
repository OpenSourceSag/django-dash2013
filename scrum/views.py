from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import Project, Story, Task, Sprint, SprintTasks, TASKS_STATUS
from django.http import HttpResponseNotFound, HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, StoryForm, TaskForm, SprintForm

import string
import json

#@login_required
class SprintView(DetailView):
    template_name = 'scrum/sprint.html'
    model = Sprint
    
    def get_context_data(self, **kwargs):
        context = super(SprintView, self).get_context_data(**kwargs)
        sprint = kwargs.get('object')

        sprint_tasks = sprint.tasks.all()

        context['sprint'] = sprint
        context['todos'] = sprint_tasks.filter(status='TO')
        context['doings'] = sprint_tasks.filter(status='IN')
        context['dones'] = sprint_tasks.filter(status='DO')
        context['bugs'] = sprint_tasks.filter(status='PR')
        context['backlogs'] = sprint_tasks.filter(status='BA')

        return context

#@login_required
class WhiteBoardView(DetailView):
    template_name = 'scrum/whiteboard.html'
    model = Project
    

    def get_context_data(self, **kwargs):
        context = super(WhiteBoardView, self).get_context_data(**kwargs)

        print self.request.method
        print self.request.method
        print self.request.method
        project = kwargs.get('object')
        project_stories = Story.objects.filter(project=project)
        project_tasks = Task.objects.filter(story__in=project_stories)
        project_tasks_backlog = project_tasks.filter(status='BACKLOGS')

        context['stories'] = project_stories
        context['tasks'] = project_tasks
        context['tasks_backlog'] = project_tasks_backlog

        return context

#@login_required
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
        project_tasks_backlog = project_tasks.filter(status='BACKLOGS')

        context['stories'] = project_stories
        context['tasks'] = project_tasks
        context['tasks_backlog'] = project_tasks_backlog

        return context
    
    
#@login_required
def add_story(request, pk_project):
    if request.method == 'POST':
        response_data = {}

        post_values = request.POST.copy()
        post_values['project'] = pk_project

        f = StoryForm(post_values)
        if f.is_valid():
            new_story = f.save()
            response_data['story_pk'] = new_story.pk
        else:
            print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404

#@login_required
def update_story(request, pk_project, pk_story):
    if request.method == 'POST':
        response_data = {}
        
        if pk_story:
            story = Story.objects.get(pk=pk_story)
            
            post_values = request.POST.copy()
            post_values['project'] = story.project.pk
            
            f = StoryForm(post_values, instance=story)
            if f.is_valid():
                story = f.save()
                response_data['story_pk'] = story.pk
            else:
                print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404
    
#@login_required
def add_task(request, pk_project):
    if request.method == 'POST':
        response_data = {}
        
        post_values = request.POST.copy()
        post_values['project'] = pk_project
        post_values['status'] = 'TO'
        
        f = TaskForm(post_values)
        if f.is_valid():
            new_task = f.save()
            response_data['task_pk'] = new_task.pk
        else:
            print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404
    
#@login_required
def update_task(request, pk_project, pk_task):
    if request.method == 'POST':
        response_data = {}
        
        if pk_task:
            task = Task.objects.get(pk=pk_task)
            
            post_values = request.POST.copy()
            post_values['status'] = task.status
            
            f = TaskForm(post_values, instance=task)
            if f.is_valid():
                task = f.save()
                response_data['task_pk'] = task.pk
            else:
                print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404

#@login_required
def add_project(request):
    if request.method == 'POST':
        response_data = {}
        
        f = ProjectForm(request.POST)
        if f.is_valid():
            new_project = f.save()
            response_data['project_pk'] = new_project.pk
        else:
            print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404

#@login_required
def update_project(request, pk_project):
    if request.method == 'POST':
        response_data = {}
        
        if pk_project:
            project = Project.objects.get(pk=pk_project)
            
            f = ProjectForm(request.POST, instance=project)
            if f.is_valid():
                project = f.save()
                response_data['project_pk'] = project.pk
            else:
                print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404
    
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        #else:
            # Return a 'disabled account' error message
    #else:
        # Return an 'invalid login' error message.

@login_required
def logout(request):
    logout(request)
    # Redirect to a success page