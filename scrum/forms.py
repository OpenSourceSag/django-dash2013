from django.forms import ModelForm
from .models import Project, Story, Task, Sprint

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
         
         
         
