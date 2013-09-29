from django.forms import ModelForm
from .models import Project, Story, Task, Sprint, SprintTasks
from django.contrib.auth.models import User

class ProjectForm(ModelForm):
     class Meta:
         model = Project
         
class StoryForm(ModelForm):
     class Meta:
         model = Story
         
class TaskForm(ModelForm):
     class Meta:
         model = Task
         
class SprintForm(ModelForm):
     class Meta:
         model = Sprint
         
class SprintTasksForm(ModelForm):
     class Meta:
         model = SprintTasks

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff','is_superuser')