from django.contrib import admin
from .models import Project, Story, Task, Sprint, SprintTasks
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple

class ImageInline(admin.StackedInline):
    model = SprintTasks
    
class ProjectAdmin(admin.ModelAdmin):
	model = Project
	
class StoryAdmin(admin.ModelAdmin):
	model = Story
	
class TaskAdmin(admin.ModelAdmin):
	model = Task
	
class SprintAdmin(admin.ModelAdmin):
    model = Sprint
    inlines = [ImageInline,]
	

	
admin.site.register(Project, ProjectAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Sprint, SprintAdmin)
