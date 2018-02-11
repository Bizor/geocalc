from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User

# Create your models here.

class CoordSys(models.Model):
	class Meta:
		db_table = "CoordSys"
		verbose_name = "Система координат"
		verbose_name_plural = "Системы координат"
	coordsys_name = models.CharField(max_length = 255 , verbose_name="Наименование Системы Координат")
	coordsys_param = models.CharField(max_length = 255 , verbose_name="Параметры Системы координат")
	def __str__(self):
		return "%s" % (self.coordsys_name)


class Project(models.Model):
	class Meta:
		db_table = "Project"
		verbose_name = "Проект"
		verbose_name_plural = "Проекты"
	project_name = models.CharField(max_length = 255 , verbose_name="Наименование Проекта")
	project_owner = models.ForeignKey(User, verbose_name="Создал", on_delete=models.CASCADE)
	project_points = models.TextField(default='', verbose_name="Каталог точек")
	def __str__(self):
		return "%s" % (self.project_name)