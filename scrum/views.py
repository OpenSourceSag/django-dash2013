from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q

from .models import Project, Story, Task, Sprint, SprintTasks
from .forms import ProjectForm, StoryForm, TaskForm, SprintTasksForm

import json


def is_manager(user):
    return 'manager' in (s.lower() for s in user.groups.values_list('name', flat=True))


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
        #Can close a sprint if the user is a manager, if the sprint is not closed and if there is at least one task
        context['can_close_sprint'] = is_manager(self.request.user) and not sprint.is_closed and sprint.tasks.count() > 0

        return context


class ProjectListView(ListView):
    model = Project


class WhiteBoardView(DetailView):

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

    def render_to_response(self, context, **response_kwargs):
        #If the user is not a manager
        if is_manager(self.request.user):
            #Display whiteboard in read only
            self.template_name = 'scrum/whiteboard.html'
        else:
            self.template_name = 'scrum/whiteboard_read.html'

        return self.response_class(
            request=self.request,
            template=self.template_name,
            context=context,
            **response_kwargs
        )


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
            old_task_status = task.status

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

                    #Get the sprint id
                    sprint_id = referer_url[referer_url.find('/sprint/')+8:referer_url.rfind('/')]
                    sprint = Sprint.objects.get(pk=sprint_id)

                    #If the sprint is closed, send error message
                    if sprint.is_closed:
                        response_data['error_message'] = 'This sprint is closed!'
                        return HttpResponse(json.dumps(response_data), content_type="application/json")

                post_values['status'] = post_status
                post_values['estimated_time'] = task.estimated_time
                post_values['story'] = task.story.pk
                post_values['title'] = task.title
                post_values['assigned_to'] = None
                
                if task.assigned_to:
                    post_values['assigned_to'] = task.assigned_to.pk

                #if in progress, affect user
                if post_status == 'IN':
                    post_values['assigned_to'] = request.user.pk
                  
                #if to do, delete assignated user    
                elif post_status == 'TO':
                    post_values['assigned_to'] = None

                #Only manager can move to or from backlog
                elif (old_task_status != 'BA' and post_status == 'BA') or (old_task_status == 'BA' and post_status != 'BA'):
                    #If the user is not a manager
                    if not(is_manager(request.user)):

                        response_data['error_message'] = 'You are not allowed to do that!'
                        return HttpResponse(json.dumps(response_data), content_type="application/json")

            #Call form with post values
            f = TaskForm(post_values, instance=task)
            if f.is_valid():
                task = f.save()
                response_data['task_pk'] = task.pk

                first_name = request.user.first_name
                last_name = request.user.last_name

                #Send username if no first_name nor last_name
                if first_name or last_name:
                    response_data['full_name'] = ' '.join(filter(None, (first_name, last_name)))
                else:
                    response_data['full_name'] = request.user.username
                print response_data['full_name']
            else:
                print f.errors

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404


def add_project(request):
    if request.method == 'GET':

        newProject = Project.objects.create()
        return HttpResponseRedirect(reverse('project', args=(newProject.pk,)))
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
        post_data['sprint'] = request.POST.get('sprint', None)
        post_data['task'] = request.POST.get('task', None)

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
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        raise Http404


def close_sprint(request, pk):
    if request.method == 'POST':

        response_data = {}
        #If all tasks are not in backlog or done
        if SprintTasks.objects.filter(sprint__pk=pk).exclude(Q(task__status='DO') | Q(task__status='BA')).count() != 0:
            response_data['error_message'] = 'All tasks must be done or backloged!'
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        #We change the task end status of each sprinttask
        for st in SprintTasks.objects.filter(sprint__pk=pk):
            st.task_end_status = st.task.status
            st.save()

        sprint = Sprint.objects.get(pk=pk)
        sprint.is_closed = True
        sprint.save()

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        raise Http404

