from rest_framework import serializers
from riverdash.models import Device, DeviceReading, AverageDailyDischarge

class DeviceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Device
		fields = ('id', 'device_id', 'device_lat', 'device_lng', 'device_auth')

	# device_id = serializers.CharField(max_length=25)
	# device_lat = serializers.DecimalField(max_digits=9, decimal_places=6)
	# device_lng = serializers.DecimalField(max_digits=9, decimal_places=6)
	# device_auth = serializers.CharField(max_length=50, default='!n!t')
	# readings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

	# def create(self, validated_data):
	# 	return Device.objects.create(**validated_data)

	# def update(self, instance, validated_data):
	# 	instance.device_id = validated_data.get('device_id', instance.device_id)
	# 	instance.device_lat = validated_data.get('device_lat', instance.device_lat)
	# 	instance.device_lng = validated_data.get('device_lng',instance.device_lng)
		
	# 	instance.save()
	# 	return instance

class ReadingSerializer(serializers.ModelSerializer):
	class Meta:
		model = DeviceReading
		fields = ('devread_id','devread_depth_sensor_one','devread_depth_sensor_two','devread_device','devread_received','devread_time','devread_discharge','devread_stage')
		

	# def create(self, validated_data):
	# 	return DeviceReading.objects.create(**validated_data)

	# def update(self, instance, validated_data):
	# 	instance.devread_id = validated_data.get('devread_id', instance.devread_id)
	# 	instance.devread_depth_sensor_one = validated_data.get('devread_depth_sensor_one', instance.devread_depth_sensor_one)
	# 	instance.devread_depth_sensor_two = validated_data.get('devread_depth_sensor_two',instance.devread_depth_sensor_two)
	# 	instance.devread_time = validated_data.get('devread_time', instance.devread_time)
	# 	instance.devread_received = validated_data.get('devread_received', instance.devread_received)
		
	# 	instance.save()
	# 	return instances