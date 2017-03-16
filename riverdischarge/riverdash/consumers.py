from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from riverdash.models import Device, DeviceReading, AverageDailyDischarge, Setconfig
from django.db.models import Avg
from datetime import datetime
from decimal import Decimal
import pytz
import json


tz = pytz.timezone('Asia/Taipei')

@channel_session
def reading_connect(message):
	#retrieve from message path
	device_trying = message.content['path'].split('/')
	device = []

	try:
		device = Device.objects.filter(device_id=device_trying[2]).filter(device_auth=device_trying[3])
	except Exception as e:
		raise ValueError('Something went wrong!')

	if not device:
		message.reply_channel.send({'close':True})
		raise ValueError('Device not found!')

	message.reply_channel.send({'accept': True})
	Group('readings').send({'text':'{0}c'.format(device_trying[2])})
	Group('readings').add(message.reply_channel)

	#update device
	try:
		device = Device.objects.get(device_id=device_trying[2])
		device.device_status = 1
		device.save()
		print "Device status updated after connection"
	except:
		print "Unable to update device status after connection."


	print "Device ID:{0} Joined readings Channel {1}".format(device_trying[2],message.content)


# @channel_session
# def reading_message(message):
# 	reading_obj = json.loads(message.content['text'])

# 	push_mode = reading_obj['pm']


# 	if int(push_mode) in [1,3]:
# 		try:
# 			water_level_one = reading_obj['w1']
# 			water_level_two = reading_obj['w2']
# 			devread_id = reading_obj['di']
# 			devread_device = 'RDM1111'

			
# 			device = Device.objects.get(device_id=devread_device)
# 			DeviceReading.objects.create(
# 					devread_depth_sensor_one = water_level_one,
# 					devread_depth_sensor_two = water_level_two,
# 					devread_device = device,
# 					devread_id = devread_id,
# 				)
# 			print "Stored Device Reading"

# 		except Exception as e:
# 			print e

# 	Group('readings').send({
# 			'text':message.content['text'],
# 		})

# 	print "SMS FORMAT: {0}, JSON OBJ: {1}".format(message.content['text'],reading_obj)

@channel_session
def reading_message(message):
	reading_obj = json.loads(message.content['text'])
	print reading_obj

	push_mode = reading_obj['pm']
	sms = reading_obj['sms']

	sms_data_list = []
	sms_data_list = sms.split(',')

	#validation {"sms":"id,mo,dy,hr,mn,rd1,rd2,battlevel,yr","pm":"1"}

	if int(push_mode) in [1,3]:
		devread_id = sms_data_list[0]
		try:
			read = DeviceReading.objects.get(devread_id=devread_id)
		except:
			try:
				devread_id = sms_data_list[0]
				dday = sms_data_list[2]
				dmonth = sms_data_list[1]
				dyear = sms_data_list[8]
				devread_time = "{0}/{1}/{2} {3}:{4}".format(sms_data_list[1],sms_data_list[2],sms_data_list[8],sms_data_list[3],sms_data_list[4])
				devread_time_obj = datetime.strptime(devread_time,'%m/%d/%Y %H:%M')
				if devread_time_obj.month in [1,2,3]:
					quarter = 1
				elif devread_time_obj.month in [4,5,6]:
					quarter = 2
				elif devread_time_obj.month in [7,8,9]:
					quarter = 3
				elif devread_time_obj.month in [10,11,12]:
					quarter = 4
				else:
					quarter = "None"

				sense = Setconfig.objects.get(pk=1)
				sensor_height = sense.sensor_height
				received = datetime.now(tz)
				rc = received.strftime("%m/%d/%Y %H:%M")
				r = datetime.strptime(rc,"%m/%d/%Y %H:%M")

				devread_device = 'RDM1111'
				water_level_one = Decimal(float(sensor_height) - (float(sms_data_list[5]) * (0.01))) #convert cm to m
				water_level_two = Decimal(float(sensor_height) - (float(sms_data_list[6]) * (0.01))) #convert cm to m
				device_batt = sms_data_list[7]
				device = Device.objects.get(device_id=devread_device)
				device.device_battery = device_batt
				device.save()
				print "Quarter({0}) Water_one({1}), Water_two({2})".format(quarter,water_level_one,water_level_two)
				DeviceReading.objects.create(
						devread_depth_sensor_one = "{0:,.2f}".format(water_level_one),
						devread_depth_sensor_two = "{0:,.2f}".format(water_level_two),
						devread_device = device,
						devread_time = devread_time_obj,
						devread_received = r,
						devread_id = devread_id,
						devread_quarter = quarter,
					)
				obj = DeviceReading.objects.filter(devread_time__day=dday,devread_time__month=dmonth,devread_time__year=dyear)
				discharge_ave = obj.aggregate(Avg('devread_discharge'))['devread_discharge__avg']
				stage_ave = obj.aggregate(Avg('devread_stage'))['devread_stage__avg']
				disc_obj = AverageDailyDischarge.objects.filter(discharge_date=devread_time_obj.date())

				if not disc_obj:
					AverageDailyDischarge.objects.create(discharge=discharge_ave,stage=stage_ave,discharge_date=devread_time_obj.date())
				else:
					for d in disc_obj:
						d.discharge = discharge_ave
						d.stage = stage_ave
						d.save()

				print "Stored Device Reading"
				Group('readings').send({
					'text':message.content['text'],
					})

			except Exception as e:
				Group('readings').send({
						'text':'404',
					})
				print e			

	print "SMS FORMAT: {0}, JSON OBJ: {1}, FORMATTED DATA: {2}".format(message.content['text'],reading_obj,sms_data_list)


@channel_session
def reading_disconnect(message):
	device = message.content['path'].split('/')[2]
	Group('readings').send({'text':device})
	Group('readings').discard(message.reply_channel)

	#update device status
	try:
		device = Device.objects.get(device_id=device)
		device.device_status = 0
		device.device_battery = 0
		device.save()
		print "Device status updated after disconnection."
	except:
		print "Unable to update device status after device disconnection."


# @channel_session
# def reading_disconnect(message):
# 	message.reply_channel.send({'close':True})
# 	Group('readings').send({'close':True})
# 	Group('readings').discard(message.reply_channel)
