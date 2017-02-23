from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from riverdash.models import Device, DeviceReading
from riverdash.serializers import DeviceSerializer, ReadingSerializer
from rest_framework.permissions import IsAuthenticated
from riverdash.riverai import RiverDischargeAI
from django.utils import timezone
from datetime import datetime, date
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import pdfkit
import os


@api_view(['GET','POST'])
def device_list(request, format=None):
	if request.method == 'GET':
		devices = Device.objects.all()
		serializer = DeviceSerializer(devices, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = DeviceSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def device_detail(request, pk, format=None):
	try:
		device = Device.objects.get(pk=pk)
	except Device.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = DeviceSerializer(device)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = DeviceSerializer(device, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		device.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
# @authentication_classes((DeviceAuthentication,))
# @permission_classes((IsAuthenticated,))
def reading_list(request, format=None):
    if request.method == 'GET':
        if not request.query_params:
            dt = timezone.now()
        else:
        	dt = request.query_params['dt']
        	if dt == '':
        		dt = timezone.now()
        	else:
        		dt = datetime.strptime(dt,'%d %B, %Y').date()

        readings = DeviceReading.objects.filter(devread_received__day=dt.day,devread_received__month=dt.month,devread_received__year=dt.year)
        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def get_reading_for_chart(request, format=None):
	if request.method == 'GET':
		if not request.query_params:
			dt = timezone.now()
			print "Time for today"
			readings = DeviceReading.objects.filter(devread_received__day=dt.day,devread_received__month=dt.month,devread_received__year=dt.year)
		else:
			dt = request.query_params['dt']
			dt = datetime.strptime(dt,'%d %B, %Y').date()
			readings = DeviceReading.objects.filter(devread_received__day=dt.day,devread_received__month=dt.month,devread_received__year=dt.year)
			print "Data for some time"

		serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)

def index(request, template_dir='rdmsystem/index.html'):
	if not request.user.is_authenticated:
		return redirect('/login')
	else:
		return render(request, template_dir)

def login_user(request, template_dir='rdmsystem/login.html'):
	return render(request, template_dir)

def login_now(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username,password=password)

	if user is not None:
		login(request, user)
		return redirect('/index')
	else:
		return redirect('/login')


def daily_report(request, template_dir='rdmsystem/daily_report.html'):
	if request.method == 'GET':
		dt = request.GET.get('dt','')

		if dt == '':
			dt = timezone.now()
		else:
			dt = datetime.strptime(dt,'%d %B, %Y').date()

		readings = DeviceReading.objects.filter(devread_received__day=dt.day,devread_received__month=dt.month,devread_received__year=dt.year)

		context = {'readings':readings,'dt':dt}

		return render(request, template_dir, context)


def readings_wpagination(request):
	if request.method == 'GET':
		dt = request.GET.get('dt','')
		page = int(request.GET.get('page',''))

		if dt == '':
			dt = timezone.now()
		else:
			dt = datetime.strptime(dt,'%d %B, %Y').date()

		pages = DeviceReading.objects.filter(devread_received__day=dt.day,devread_received__month=dt.month,devread_received__year=dt.year).count()

		if page == 1:
			readings = DeviceReading.objects.filter(devread_received__day=dt.day,devread_received__month=dt.month,devread_received__year=dt.year)[0:10]
		else:
			readings = DeviceReading.objects.filter(devread_received__day=dt.day,devread_received__month=dt.month,devread_received__year=dt.year)[page*10:page*10+10]
		
		data = serializers.serialize('json', readings)

	return JsonResponse({'readings':data,'total':pages})




def html_to_pdf(request):
	path_wkthmltopdf = r'C:\Python27\wkhtmltopdf\bin\wkhtmltopdf.exe'
	config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

	projectUrl = "http://{0}/readings/reports/daily".format(request.get_host())
	pdf = pdfkit.from_url(projectUrl, False, configuration=config, options={'javascript-delay':9000})	

	# pdf
	# response = HttpResponse(pdf,content_type='application/pdf')
	# response['Content-Disposition'] = 'attachment; filename="ourcodeworld.pdf"'

	# return response
	response = HttpResponse(pdf, content_type='application/pdf')
	# response['Content-Disposition'] = 'attachment; filename="outcode.pdf"'

	return response  # returns the response.

def machine_learning(request):
	y = [0.050,0.043,5.372,0.555,0.184,0.086,0.006,0.044,0.520,0.101,0.018,0.728,0.294,0.109,0.425,0.397,0.423,0.809,1.479]
	x = [23,20,(77+74)/2.0,40,30,25,22,22,24,24,18,(42+41)/2.0,32,25,35,33,34,41,(41+43)/2.0]

	if request.method == 'GET':
		quarter = request.GET.get('quarter')

	if quarter == '1':
		readings = DeviceReading.objects.filter(Q(devread_received__month=1) | Q(devread_received__month=2) | Q(devread_received__month=3) ,devread_received__year=timezone.now().year)
	elif quarter == '2':
		readings = DeviceReading.objects.filter(Q(devread_received__month=4) | Q(devread_received__month=5) | Q(devread_received__month=6) ,devread_received__year=timezone.now().year)
	elif quarter == '3':
		readings = DeviceReading.objects.filter(Q(devread_received__month=7) | Q(devread_received__month=8) | Q(devread_received__month=9) ,devread_received__year=timezone.now().year)
	elif quarter == '4':
		readings = DeviceReading.objects.filter(Q(devread_received__month=10) | Q(devread_received__month=11) | Q(devread_received__month=12) ,devread_received__year=timezone.now().year)
	else:
		readings = None

	data_set = [y,x]

	# rd = RiverDischargeAI(data_set,new_data)
	# print rd.get_predicted_value_discharge()

	data = serializers.serialize('json', readings)

	return JsonResponse({'readings':data})
