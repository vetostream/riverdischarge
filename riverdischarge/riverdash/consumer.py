from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from rdmsystem.models import Device, DeviceReading
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

	print "Device ID:{0} Joined readings Channel {1}".format(device_trying[2],message.content)


@channel_session
def reading_message(message):
	reading_obj = json.loads(message.content['text'])

	push_mode = reading_obj['pm']


	if int(push_mode) in [1,3]:
		try:
			water_level_one = reading_obj['w1']
			water_level_two = reading_obj['w2']
			devread_id = reading_obj['di']
			devread_device = 'RDM1111'

			
			device = Device.objects.get(device_id=devread_device)
			DeviceReading.objects.create(
					devread_depth_sensor_one = water_level_one,
					devread_depth_sensor_two = water_level_two,
					devread_device = device,
					devread_id = devread_id,
				)
			print "Stored Device Reading"

		except Exception as e:
			print e

	Group('readings').send({
			'text':message.content['text'],
		})

	print message.content['text']


@channel_session
def reading_disconnect(message):
	device = message.content['path'].split('/')[2]
	Group('readings').send({'text':device})
	Group('readings').discard(message.reply_channel)

# @channel_session
# def reading_disconnect(message):
# 	message.reply_channel.send({'close':True})
# 	Group('readings').send({'close':True})
# 	Group('readings').discard(message.reply_channel)
