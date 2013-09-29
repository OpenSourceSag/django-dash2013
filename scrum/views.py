from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import Project, Story, Task, Sprint, SprintTasks
from .forms import ProjectForm, StoryForm, TaskForm, SprintForm, SprintTasksForm, UserForm

import string
import json


class SprintView(DetailView):
    template_name = 'scrum/sprint.html'
    model = Sprint

    def get_context_data(self, **kwargs):
        context = super(SprintView, self).get_context_data(**kwargs)
        sprint = kwargs.get('object')

        #Get all tasks
        sprint_tasks = sprint.tasks.all()

        #Set template's data
        context['sprint'] = sprint
        context['todos'] = sprint_tasks.filter(status='TO')
        context['doings'] = sprint_tasks.filter(status='IN')
        context['dones'] = sprint_tasks.filter(status='DO')
        context['bugs'] = sprint_tasks.filter(status='PR')
        context['backlogs'] = sprint_tasks.filter(status='BA')

        return context


class WhiteBoardView(DetailView):
    template_name = 'scrum/whiteboard.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(WhiteBoardView, self).get_context_data(**kwargs)

        #Get project's stories
        project = kwargs.get('object')
        #project_stories = Story.objects.filter(project=project)
        #Get project's tasks
        project_tasks = Task.objects.unassigned().filter(story__project_id=project.id)
        #Get project's tasks with a status backlog in a sprint with a end status backlog
        project_tasks_backlog = Task.objects.filter(pk__in=SprintTasks.objects.filter(task_end_status='BA', task__status='BA', task__story__project_id=project.id).values_list('task', flat=True))

        #Set template's data
        context['tasks'] = project_tasks
        context['backlogs'] = project_tasks_backlog

        return context


def add_story(request, pk_project):
    if request.method == 'POST':
        response_data = {}

        #Add the project to post values
        post_values = request.POST.copy()
        post_values['project'] = pk_project

        #Call form with post values
        f = StoryForm(post_values)
        if f.is_valid():
            new_story = f.save()
            response_data['story_pk'] = new_story.pk
        else:
            print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404


def update_story(request, pk_story):
    if request.method == 'POST':
        response_data = {}

        if pk_story:
            story = Story.objects.get(pk=pk_story)

            #Add the project to post values
            post_values = request.POST.copy()
            post_values['project'] = story.project.pk

            #Call form with post values and instance
            f = StoryForm(post_values, instance=story)
            if f.is_valid():
                story = f.save()
                response_data['story_pk'] = story.pk
            else:
                print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404


def add_task(request, pk_project):
    if request.method == 'POST':
        response_data = {}


        post_values = request.POST.copy()
        post_values['project'] = pk_project
        post_values['status'] = 'TO'

        #Call form with post values
        f = TaskForm(post_values)
        if f.is_valid():
            new_task = f.save()
            response_data['task_pk'] = new_task.pk
        else:
            print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404


def update_task(request, pk_task):
    if request.method == 'POST':
        response_data = {}

        if pk_task:
            task = Task.objects.get(pk=pk_task)

            #Add the task's status to post values
            post_values = request.POST.copy()
            post_values['status'] = task.status

            #If a POST status exist (update a task's status) 
            post_status = request.POST.get('status', None)
            if post_status:
                
                #Get the referer URL
                referer_url = request.META.get('HTTP_REFERER', None)
                
                #If called from the Sprint page
                if referer_url and '/sprint/' in referer_url:
                    
                    sprint_id = referer_url[referer_url.find('/sprint/')+8:referer_url.rfind('/')]
                    sprint = Sprint.objects.get(pk=sprint_id)
                    
                    #If the sprint is closed
                    if sprint.is_closed:
                        response_data['error_message'] = 'This sprint is closed!'
                        return HttpResponse(json.dumps(response_data), content_type="application/json")

                post_values['status'] = post_status
                post_values['estimated_time'] = task.estimated_time
                post_values['story'] = task.story.pk
                post_values['title'] = task.title

                #if in progress, affect user
                if post_status == 'IN':
                    post_values['assigned_to'] = request.user.pk

                #Only manager can move to backlog
                elif post_status == 'BA':
                    #If the user is not a manager
                    if not(any(s.lower() == 'manager' for s in request.user.groups.values_list('name',flat=True))):

                        response_data['error_message'] = 'You are not allowed to do that!'
                        return HttpResponse(json.dumps(response_data), content_type="application/json")


            #Call form with post values
            f = TaskForm(post_values, instance=task)
            if f.is_valid():
                task = f.save()
                response_data['task_pk'] = task.pk
            else:
                print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404


def add_project(request):
    if request.method == 'POST':
        response_data = {}

        #Call form with post values
        f = ProjectForm(request.POST)
        if f.is_valid():
            new_project = f.save()
            response_data['project_pk'] = new_project.pk
        else:
            print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404


def update_project(request, pk_project):
    if request.method == 'POST':
        response_data = {}

        if pk_project:
            project = Project.objects.get(pk=pk_project)

            #Call form with post values and instance
            f = ProjectForm(request.POST, instance=project)
            if f.is_valid():
                project = f.save()
                response_data['project_pk'] = project.pk
            else:
                print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404


def add_sprint_task(request):
    if request.method == 'POST':
        post_data = {}

        #Add the task, sprint and task_end_status to post values
        post_data['task_end_status'] = 'DO'
        post_data['sprint'] = request.POST.get('sprint',None)
        post_data['task'] = request.POST.get('task',None)

        #Call form with post values
        f = SprintTasksForm(post_data)
        if f.is_valid():
            f.save()
        else:
            print f.errors

        return HttpResponse()
    else:
        raise Http404


def add_sprint(request, pk):
    if request.method == 'GET':
        newSprint = Sprint.objects.create(project_id=pk)
        response = {'id': newSprint.id, 'number': newSprint.number}
        return HttpResponse(json.dumps(response))
    else:
        raise Http404


class ProjectListView(ListView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        sprint = kwargs.get('object')
        #
        ##Get all tasks
        #sprint_tasks = sprint.tasks.all()
        #
        ##Set template's data
        #context['sprint'] = sprint
        #context['todos'] = sprint_tasks.filter(status='TO')
        #context['doings'] = sprint_tasks.filter(status='IN')
        #context['dones'] = sprint_tasks.filter(status='DO')
        #context['bugs'] = sprint_tasks.filter(status='PR')
        #context['backlogs'] = sprint_tasks.filter(status='BA')
        #
        return context


def sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'])
            new_user.is_staff = form.cleaned_data['is_staff']
            new_user.is_superuser = form.cleaned_data['is_superuser']
            new_user.save()

            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('/login')
    else:
        form = UserForm()

    return render(request, 'scrum/registration/sign_up.html', {'form': form})
