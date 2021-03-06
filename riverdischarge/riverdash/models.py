from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class Device(models.Model):
	device_id = models.CharField(max_length=25,unique=True)
	device_lat = models.DecimalField(max_digits=9, decimal_places=6)
	device_lng = models.DecimalField(max_digits=9, decimal_places=6)
	device_auth = models.CharField(max_length=128, default='!n!t')
	device_added = models.DateTimeField(auto_now_add=True)
	device_battery = models.DecimalField(max_digits=11, decimal_places=6, null=True)
	device_status = models.IntegerField(null=True)

	def __unicode__(self):
		return u"%s" % self.device_id

	def __str__(self):
		return "%s" % self.device_id

class DeviceReading(models.Model):
	devread_id = models.CharField(max_length=25)
	devread_depth_sensor_one = models.DecimalField(max_digits=12, decimal_places=6, default=0)
	devread_depth_sensor_two = models.DecimalField(max_digits=12, decimal_places=6, default=0)
	devread_time = models.DateTimeField('datetime of reading.',null=True)
	devread_received = models.DateTimeField('datetime of receiving',null=True)
	devread_discharge = models.DecimalField(max_digits=12, decimal_places=6, default=0)
	devread_stage = models.DecimalField(max_digits=12, decimal_places=6, default=0)
	devread_quarter = models.IntegerField(default=0, null=False)
	devread_device = models.ForeignKey(Device, to_field='device_id', on_delete=models.CASCADE)

	def __unicode__(self):
		return u"%s" % self.devread_id

	def __str__(self):
		return self.devread_id

class MonthlyDischarge(models.Model):
	discharge = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=False)
	stage = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=False)
	month = models.IntegerField(default=0, null=False)
	part = models.IntegerField(default=0, null=False)
	quarter = models.IntegerField(default=0, null=False)
	year = models.IntegerField(default=0, null=False)

	def __unicode__(self):
		return u"%s" % self.id

	def __str__(self):
		return self.id

class AverageDailyDischarge(models.Model):
	discharge = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=False)
	stage = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=False)
	discharge_date = models.DateField('date for averaged discharge.')

	def __unicode__(self):
		return u"%s" % self.id

	def __str__(self):
		return self.id	


class QuarterConstants(models.Model):
	a = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=False)
	b = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=False)
	r = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=False)
	rtwo = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=False)
	year = models.IntegerField(default=0, null=False)
	quarter = models.IntegerField(default=0, null=False)
	river_profile = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=False)

class Setconfig(models.Model):
	sensor_height = models.DecimalField(max_digits=12, decimal_places=6, default=0, null=False)






