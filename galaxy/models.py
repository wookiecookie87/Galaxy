from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
import datetime

# Create your models here.
@python_2_unicode_compatible
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField()

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

@python_2_unicode_compatible
class Choice(models.Model):
	question = models.TextField()
	choice_text = models.CharField(max_length=200)
	votes =models.TextField()

	def __str__(self):
		return self.choice_text


@python_2_unicode_compatible
class Galaxy_Image(models.Model):
	file_name = models.CharField(max_length=300)
	computed = models.BooleanField(default = 'false')

	def __str__(self):
		return self.file_name

@python_2_unicode_compatible
class Action_Log(models.Model):
	user_id = models.CharField(max_length=100)
	file_name = models.CharField(max_length=300)
	graph_num = models.IntegerField()
	completed = models.BooleanField(default = 'false')	

	def __str__(self):
		return self.user_id

@python_2_unicode_compatible
class Graph_Info(models.Model):
	file_name = models.CharField(max_length=300)
	graph_count = models.IntegerField(default = 0)
	graph_name = models.CharField(max_length=300)
	y_min = models.DecimalField(max_digits=6, decimal_places=2)
	y_max = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return {"y_min" : self.y_min, "y_max" : self.y_max}

	def __unicode__(self):
		return unicode(self.y_min)

@python_2_unicode_compatible
class Action_Info(models.Model):
	user_id = models.CharField(max_length=100)
	point_1_x = models.DecimalField(max_digits=8, decimal_places=3)
	point_1_y = models.DecimalField(max_digits=8, decimal_places=3)
	point_2_x = models.DecimalField(max_digits=8, decimal_places=3)
	point_2_y = models.DecimalField(max_digits=8, decimal_places=3)
	file_name = models.CharField(max_length=300)
	graph_num = models.IntegerField()

	def __str__(self):
		return self.user_id
