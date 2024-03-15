from django.db import models

class Projects(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=50)

class Tasks(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Projects, on_delete = models.CASCADE)
    task_name = models.CharField(max_length=50)