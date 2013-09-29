from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

TASKS_STATUS = (('TO', 'To do'),
                ('IN', 'In progress'),
                ('PR', 'Problem'),
                ('DO', 'Done'),
                ('BA', 'Backlogs'),)


class Project(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='Project_users', blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return "%s" % (self.name, )


class Story(models.Model):
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name='stories')
    estimated_time = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return "%s" % (self.title, )


class TaskManager(models.Manager):
    use_for_related_fields = True

    def unassigned(self):
        return self.filter(sprint__id__isnull=True)


class Task(models.Model):
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=2, choices=TASKS_STATUS)
    last_modified = models.DateTimeField(auto_now=True)
    assigned_to = models.ManyToManyField(User, related_name='Task_users', blank=True, null=True)
    story = models.ForeignKey(Story, related_name='Task_story')
    estimated_time = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(8)])
    objects = TaskManager()

    class Meta:
        ordering = ('id',)
        verbose_name = "Task"

    def __unicode__(self):
        return "%s" % (self.title,)


class SprintManager(models.Manager):
    use_for_related_fields = True

    def active(self):
        sprint = self.filter(is_closed=False).order_by('number')[:1]
        if sprint.count() == 1:
            return sprint
        else:
            return ()


class Sprint(models.Model):
    number = models.IntegerField()
    is_closed = models.BooleanField()
    project = models.ForeignKey(Project, related_name='sprints')
    last_modified = models.DateTimeField(auto_now=True)
    tasks = models.ManyToManyField(Task, through='SprintTasks', blank=True, null=True)
    objects = SprintManager()

    class Meta:
        ordering = ('number',)
        unique_together = ('number', 'project')

    def __unicode__(self):
        return "sprint %s" % (self.number, )

    def save(self, *args, **kwargs):
        if self.id is None:
            self.number = (Sprint.objects.filter(project_id=self.project_id).aggregate(Max('number'))['number__max'] or 0) + 1

        super(Sprint, self).save(*args, **kwargs)


class SprintTasks(models.Model):
    sprint = models.ForeignKey(Sprint, related_name='sprints')
    task = models.ForeignKey(Task, related_name='tasks')
    task_end_status = models.CharField(max_length=2, choices=TASKS_STATUS)

    class Meta:
        unique_together = ('sprint', 'task')
