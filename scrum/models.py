from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

TASKS_STATUS = (('TODO', 'To do'),
                ('INPROGRESS', 'In progress'),
                ('REMOVED', 'Removed'),
                ('PROBLEM', 'Problem'),
                ('DONE', 'Done'),
                ('BACKLOGS', 'Backlogs'),)


class Project(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='Project_users', blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return "%s" % (self.name, )


class Story(models.Model):
    title = models.CharField(unique=True, max_length=255)
    note = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name='Story_project')
    estimated_time = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return "%s" % (self.title, )


class Task(models.Model):
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=TASKS_STATUS)
    last_modified = models.DateTimeField(auto_now=True)
    assigned_to = models.ManyToManyField(User, related_name='Task_users', blank=True, null=True)
    story = models.ForeignKey(Story, related_name='Task_story')
    estimated_time = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(8)])

    class Meta:
        ordering = ('id',)
        verbose_name = "Task"

    def __unicode__(self):
        return "%s" % (self.title,)



class Sprint(models.Model):
    number = models.IntegerField()
    is_closed = models.BooleanField()
    project = models.ForeignKey(Project, related_name='Sprint_project')
    last_modified = models.DateTimeField(auto_now=True)
    tasks = models.ManyToManyField(Task, through='SprintTasks', blank=True, null=True)

    class Meta:
        ordering = ('number',)
        unique_together = ('number', 'project')

    def __unicode__(self):
        return "sprint %s" % (self.number, )


class SprintTasks(models.Model):
    sprint = models.ForeignKey(Sprint, related_name='sprints')
    task = models.ForeignKey(Task, related_name='tasks')
    task_end_status = models.CharField(max_length=10, choices=TASKS_STATUS)

