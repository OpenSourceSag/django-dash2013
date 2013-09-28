from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

TASKS_STATUS = ((TODO, 'To do'),
                (INPROGRESS, 'In progress'),
                (REMOVED, 'Removed'),
                (PROBLEM, 'Problem'),
                (DONE, 'Done'),
                (BACKLOGS, 'Backlogs'),)


class Project(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='Project_users', blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return "%s" % (self.name, )


class Section(models.Model):
    title = models.CharField(unique=True, max_length=255)
    note = models.TextField(blank=True)
    time = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name='Section_project')

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return "%s" % (self.title, )


class Task(models.Model):
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    status = models.CharField(choices=TASKS_STATUS)
    last_modified = models.DateTimeField(auto_now=True)
    assigned_to = models.ManyToManyField(User, related_name='Task_users', blank=True, null=True)
    section = models.ForeignKey(Section, related_name='Task_section')

    class Meta:
        ordering = ('id',)
        verbose_name = "Task"

    def __unicode__(self):
        return "%s" % (self.title,)


class SprintTasks(models.Model):
    task_end_status = models.CharField(choices=TASKS_STATUS)


class Sprint(models.Model):
    number = models.IntegerField()
    is_closed = models.BooleanField()
    project = models.ForeignKey(Project, related_name='Sprint_project')
    tasks = models.ManyToManyField(Task, through='SprintTasks', blank=True, null=True)

    class Meta:
        ordering = ('title',)
        unique_together = ('number', 'project')

    def __unicode__(self):
        return "%s" % (self.sprint_title, )
