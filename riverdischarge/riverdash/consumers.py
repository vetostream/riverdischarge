from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from riverdash.models import Device, DeviceReading
from datetime import datetime
from decimal import Decimal
import json


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

	push_mode = reading_obj['pm']
	sms = reading_obj['sms']

	sms_data_list = []
	sms_data_list = sms.split(',')

	#validation {'sms':'id,mo,dy,hr,mn,rd1,rd2,battlevel,yr','pm':'1'}

	if int(push_mode) in [1,3]:
		try:
			devread_id = sms_data_list[0]
			devread_time = "{0}/{1}/{2} {3}:{4}".format(sms_data_list[1],sms_data_list[2],sms_data_list[8],sms_data_list[3],sms_data_list[4])
			devread_time_obj = datetime.strptime(devread_time,'%m/%d/%Y %H:%M')
			devread_device = 'RDM1111'
			water_level_one = sms_data_list[5]
			water_level_two = sms_data_list[6]
			device_batt = sms_data_list[7]
			print sms_data_list
			device = Device.objects.get(device_id=devread_device)
			device.device_battery = device_batt
			device.save()
			DeviceReading.objects.create(
					devread_depth_sensor_one = water_level_one,
					devread_depth_sensor_two = water_level_two,
					devread_device = device,
					devread_time = devread_time_obj,
					devread_id = devread_id,
				)
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
