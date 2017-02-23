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
	device_battery = models.DecimalField(max_digits=3, decimal_places=2, null=True)
	device_status = models.IntegerField(null=True)

	def __unicode__(self):
		return u"%s" % self.device_id

	def __str__(self):
		return "%s" % self.device_id

class DeviceReading(models.Model):
	devread_id = models.CharField(max_length=25)
	devread_depth_sensor_one = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	devread_depth_sensor_two = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	devread_time = models.DateTimeField('datetime of reading.',null=True)
	devread_received = models.DateTimeField(auto_now_add=True)
	devread_device = models.ForeignKey(Device, to_field='device_id', on_delete=models.CASCADE)

	def __unicode__(self):
		return u"%s" % self.devread_id

	def __str__(self):
		return self.devread_id
