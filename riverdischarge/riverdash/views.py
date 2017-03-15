from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from riverdash.models import Device, DeviceReading, MonthlyDischarge, QuarterConstants, AverageDailyDischarge, Setconfig
from riverdash.serializers import DeviceSerializer, ReadingSerializer
from rest_framework.permissions import IsAuthenticated
from riverdash.riverai import RiverDischargeAI
from riverdash.powerregression import PowerRegression
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
import json
import pdfkit
import os
import cStringIO as StringIO
from xhtml2pdf import pisa
from cgi import escape
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt


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

        readings = DeviceReading.objects.filter(devread_time__day=dt.day,devread_time__month=dt.month,devread_time__year=dt.year).order_by('-devread_time')
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
		return render(request, template_dir,{'username':request.user,'email':request.user.email})

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


# def daily_report(request, template_dir='rdmsystem/daily_report.html'):
# 	if request.method == 'GET':
# 		dt = request.GET.get('dt','')

# 		if dt == '':
# 			dt = timezone.now()
# 		else:
# 			dt = datetime.strptime(dt,'%d %B, %Y').date()

# 		readings = DeviceReading.objects.filter(devread_received__day=dt.day,devread_received__month=dt.month,devread_received__year=dt.year)

# 		context = {'readings':readings,'dt':dt}

# 		return render(request, template_dir, context)

def stream_report(request, template_dir='rdmsystem/streamflow.html'):
	if request.method == 'GET':
		quarter = request.GET.get('quarter')
		year = request.GET.get('year');

		context = {'quarter':quarter,'year':year}

		return render(request, template_dir, context)


def readings_wpagination(request):
	if request.method == 'GET':
		dt = request.GET.get('dt','')
		page = int(request.GET.get('page',''))

		if dt == '':
			dt = timezone.now()
		else:
			dt = datetime.strptime(dt,'%d %B, %Y').date()

		pages = DeviceReading.objects.filter(devread_time__day=dt.day,devread_time__month=dt.month,devread_time__year=dt.year).count()

		if page == 1:
			readings = DeviceReading.objects.filter(devread_time__day=dt.day,devread_time__month=dt.month,devread_time__year=dt.year)[0:10]
		else:
			readings = DeviceReading.objects.filter(devread_time__day=dt.day,devread_time__month=dt.month,devread_time__year=dt.year)[page*10:page*10+10]
		
		data = serializers.serialize('json', readings)

	return JsonResponse({'readings':data,'total':pages})




# def html_to_pdf(request):
# 	path_wkthmltopdf = r'C:\Python27\wkhtmltopdf\bin\wkhtmltopdf.exe'
# 	config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

# 	projectUrl = "http://{0}/readings/reports/daily".format(request.get_host())
# 	pdf = pdfkit.from_url(projectUrl, False, configuration=config, options={'javascript-delay':9000})	

# 	# pdf
# 	# response = HttpResponse(pdf,content_type='application/pdf')
# 	# response['Content-Disposition'] = 'attachment; filename="ourcodeworld.pdf"'

# 	# return response
# 	response = HttpResponse(pdf, content_type='application/pdf')
# 	# response['Content-Disposition'] = 'attachment; filename="outcode.pdf"'

# 	return response  # returns the response.

def stream_to_pdf(request):
	# path_wkthmltopdf = r'C:\Python27\wkhtmltopdf\bin\wkhtmltopdf.exe'
	# path_wkthmltopdf = '/usr/local/bin/xvfb.sh'
	path_wkthmltopdf = r'C:\Python27\wkhtmltopdf\bin\wkhtmltopdf.exe'
	
	config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

	projectUrl = "http://{0}/reports/stream/raw/?quarter={1}&year={2}".format(request.get_host(),request.GET.get('quarter'),request.GET.get('year'))
	pdf = pdfkit.from_url(projectUrl, False, configuration=config,options={'javascript-delay':9000})

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

def get_regression_working(request):
	data_q_points = list()
	data_h_points = list()
	a = None
	b = None
	r = None
	r2 = None

	resp = JsonResponse({})

	if request.method == 'GET':
		data_q = request.GET.get('data_q')
		data_h = request.GET.get('data_h')

	if not data_q or not data_h:
		print "Empty set of data."
		return JsonResponse({'data_q':data_q_points,'data_h':data_h_points,
			'a':a,'b':b,'r':r,'r2':r2,'err':'Missing values.','maxvalq':100,'maxvalh':100})
	else:
		print "Ready to decode string."
		data_q_points = data_q.split(',')
		data_h_points = data_h.split(',')

		#parse the data into floating point
		try:
			data_q_points = [float(q) if q != '' else float(0) for q in data_q_points]
			data_h_points = [float(h) if h != '' else float(0) for h in data_h_points]
		except:
			return JsonResponse({'data_q':data_q_points,'data_h':data_h_points,
				'a':a,'b':b,'r':r,'r2':r2,'err':'Only Numbers are allowed.','maxvalq':100,'maxvalh':100})

		print "String decoded. Stored into list."
		if len(data_q_points) != len(data_h_points):
			print "Data points length not equal."
			return JsonResponse({'data_q':data_q_points,'data_h':data_h_points,
				'a':a,'b':b,'r':r,'r2':r2,'err':'Data points should be equal','maxvalq':100,'maxvalh':100})
		else:
			#start regression
			print "starting regression."
			try:
				pwreg = PowerRegression(data_q_points,data_h_points)
				a = pwreg.cons_asubzero_final
				b = pwreg.cons_asubone_final
				r = pwreg.r
				r2 = pow(pwreg.r,2)
				maxvalq = max(data_q_points) + 5
				maxvalh = max(data_h_points) + 5
				data_forchart = [[x,y] for x,y in zip(data_h_points,data_q_points)]
				return JsonResponse({'data_q':data_q_points,'data_h':data_h_points,
					'a':a,'b':b,'r':r,'r2':r2,'err':'0','maxvalq':maxvalq,'maxvalh':maxvalh,'data_plot':data_forchart})
			except:
				return JsonResponse({'data_q':data_q_points,'data_h':data_h_points,
					'a':a,'b':b,'r':r,'r2':r2,'err':'Data points should be equal','maxvalq':100,'maxvalh':100})

def get_device_status(request):
	if request.method == 'GET':
		device_id = request.GET.get('device_id');

	device_batt = '---'
	device_status = '---'

	if not device_id:
		print "Device id not found."
	else:
		device = Device.objects.get(device_id=device_id)
		device_batt = "{0:,.2f}%".format(device.device_battery) or '---'
		device_status = "ONLINE" if device.device_status == 1 else "OFFLINE"

	return JsonResponse({'device_batt':device_batt,'device_status':device_status})

def monthly_flow_constants(request):
	if request.method == 'GET':
		quarter = request.GET.get('quarter');
		year = request.GET.get('year');
		adisc = request.GET.get('adisc');
		astage = request.GET.get('astage');
		bdisc = request.GET.get('bdisc');
		bstage = request.GET.get('bstage');
		cdisc = request.GET.get('cdisc');
		cstage = request.GET.get('cstage');
		ddisc = request.GET.get('ddisc');
		dstage = request.GET.get('dstage');
		edisc = request.GET.get('edisc');
		estage = request.GET.get('estage');
		fdisc = request.GET.get('fdisc');
		fstage = request.GET.get('fstage');
		ho = request.GET.get('ho');

	if quarter == '1':
		month_one_one = MonthlyDischarge.objects.create(discharge=adisc,stage=astage,month=1,part=1,quarter=quarter,year=year)
		month_one_two = MonthlyDischarge.objects.create(discharge=bdisc,stage=bstage,month=1,part=2,quarter=quarter,year=year)

		month_two_one = MonthlyDischarge.objects.create(discharge=cdisc,stage=cstage,month=2,part=1,quarter=quarter,year=year)
		month_two_two = MonthlyDischarge.objects.create(discharge=ddisc,stage=dstage,month=2,part=2,quarter=quarter,year=year)

		month_th_one = MonthlyDischarge.objects.create(discharge=edisc,stage=estage,month=3,part=1,quarter=quarter,year=year)
		month_th_two = MonthlyDischarge.objects.create(discharge=fdisc,stage=fstage,month=3,part=2,quarter=quarter,year=year)
	elif quarter == '2':
		month_one_one = MonthlyDischarge.objects.create(discharge=adisc,stage=astage,month=4,part=1,quarter=quarter,year=year)
		month_one_two = MonthlyDischarge.objects.create(discharge=bdisc,stage=bstage,month=4,part=2,quarter=quarter,year=year)

		month_two_one = MonthlyDischarge.objects.create(discharge=cdisc,stage=cstage,month=5,part=1,quarter=quarter,year=year)
		month_two_two = MonthlyDischarge.objects.create(discharge=ddisc,stage=dstage,month=5,part=2,quarter=quarter,year=year)

		month_th_one = MonthlyDischarge.objects.create(discharge=edisc,stage=estage,month=6,part=1,quarter=quarter,year=year)
		month_th_two = MonthlyDischarge.objects.create(discharge=fdisc,stage=fstage,month=6,part=2,quarter=quarter,year=year)
	elif quarter == '3':
		month_one_one = MonthlyDischarge.objects.create(discharge=adisc,stage=astage,month=7,part=1,quarter=quarter,year=year)
		month_one_two = MonthlyDischarge.objects.create(discharge=bdisc,stage=bstage,month=7,part=2,quarter=quarter,year=year)

		month_two_one = MonthlyDischarge.objects.create(discharge=cdisc,stage=cstage,month=8,part=1,quarter=quarter,year=year)
		month_two_two = MonthlyDischarge.objects.create(discharge=ddisc,stage=dstage,month=8,part=2,quarter=quarter,year=year)

		month_th_one = MonthlyDischarge.objects.create(discharge=edisc,stage=estage,month=9,part=1,quarter=quarter,year=year)
		month_th_two = MonthlyDischarge.objects.create(discharge=fdisc,stage=fstage,month=9,part=2,quarter=quarter,year=year)
	elif quarter == '4':
		month_one_one = MonthlyDischarge.objects.create(discharge=adisc,stage=astage,month=10,part=1,quarter=quarter,year=year)
		month_one_two = MonthlyDischarge.objects.create(discharge=bdisc,stage=bstage,month=10,part=2,quarter=quarter,year=year)

		month_two_one = MonthlyDischarge.objects.create(discharge=cdisc,stage=cstage,month=11,part=1,quarter=quarter,year=year)
		month_two_two = MonthlyDischarge.objects.create(discharge=ddisc,stage=dstage,month=11,part=2,quarter=quarter,year=year)

		month_th_one = MonthlyDischarge.objects.create(discharge=edisc,stage=estage,month=12,part=1,quarter=quarter,year=year)
		month_th_two = MonthlyDischarge.objects.create(discharge=fdisc,stage=fstage,month=12,part=2,quarter=quarter,year=year)

	#calculate regression
	data_q_points = [float(adisc),float(bdisc),float(cdisc),float(edisc),float(fdisc)]
	data_h_points = [float(astage),float(bstage),float(cstage),float(estage),float(fstage)]
	pwreg = PowerRegression(data_q_points,data_h_points)
	a = pwreg.cons_asubzero_final
	b = pwreg.cons_asubone_final
	r = pwreg.r
	r2 = pow(pwreg.r,2)

	qconstants = QuarterConstants(a=a,b=b,r=r,rtwo=r2,year=year,quarter=quarter,river_profile=ho)
	qconstants.save()

	return HttpResponse("1")
	# maxvalq = max(data_q_points) + 5
	# maxvalh = max(data_h_points) + 5
	# data_forchart = [[x,y] for x,y in zip(data_h_points,data_q_points)]


def get_quarter_constants(request):
	if request.method == 'GET':
		quarter = request.GET.get('quarter');
		year = request.GET.get('year');

	quarter_constants = QuarterConstants.objects.filter(quarter=quarter,year=year)
	monthly_stream = MonthlyDischarge.objects.filter(quarter=quarter,year=year)
	a = 0
	b = 0
	r = 0
	r2 = 0
	count = 0
	data_points = []
	data_function = []

	for q in quarter_constants:
		print "a:{0}".format(q.a)
		a = q.a or 0
		b = q.b or 0
		r = q.r or 0
		r2 = q.rtwo or 0

	for ms in monthly_stream:
		data_points += [[round(float(ms.discharge),2),round(float(ms.stage),2)]]


	while count < 8:
		q = (a*pow(count,b))
		stage = count
		data_function += [[round(float(q),2),round(float(stage),2)]]
		count+=1		


	json_resp = {'a':a,'b':b,'r':r,'r2':r2,'data_points':data_points,'data_function':data_function}
	return JsonResponse(json_resp)

def get_avg_discharge(request):
	if request.method == 'GET':
		month = request.GET.get('river-month')
		year = request.GET.get('river-year')

	if int(month) in [1,2,3]:
		quarter = 1
	elif int(month) in [4,5,6]:
		quarter = 2
	elif int(month) in [7,8,9]:
		quarter = 3
	elif int(month) in [10,11,12]:
		quarter = 4
	else:
		print "Unable to determine quarter"

	#Check if there are constants available for the year and quarter
	constants = QuarterConstants.objects.filter(quarter=quarter,year=year)

	if not constants:
		print "There are no constants yet."
	else:
		print "Constants are found. Yay!"
		AvgReading = AverageDailyDischarge.objects.filter(discharge_date__month=month,discharge_date__year=year)


	data = serializers.serialize('json', AvgReading)

	json_resp = {'readings':data}
	return JsonResponse(json_resp)

def render_to_pdf(template_src,context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html = template.render(context)
	result = StringIO.StringIO()

	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')

	return HttpResponse("We had some errors")


def daily_stage_report(request):
	if request.method == 'GET':
		dt = request.GET.get('dt','')

		if dt == '':
			dt = timezone.now()
		else:
			dt = datetime.strptime(dt,'%d %B, %Y').date()

	readings = DeviceReading.objects.filter(devread_time__day=dt.day,devread_time__month=dt.month,devread_time__year=dt.year).order_by('-devread_time')
	return render_to_pdf('rdmsystem/dailystage.html',{'pagesize':'A4','title':'Daily River Stage','readings':readings,'date':dt})

def logout_user(request):
	logout(request)
	return render(request, 'rdmsystem/login.html')

@csrf_exempt
def check_user(request):
	username = request.POST.get('username', False)
	password = request.POST.get('password', False)
	user = authenticate(username=username,password=password)

	if user is not None:
		return HttpResponse("1")
	else:
		return HttpResponse("0")

@csrf_exempt
def sensor_height(request):
	sensor_height = request.POST.get('sensor_height', False)
	response = JsonResponse({'data':0})

	if not sensor_height:
		response = JsonResponse({'data':0})
	else:
		try:
			sense = Setconfig.objects.get(pk=1)
			sense.sensor_height = sensor_height
			sense.save()
			response = JsonResponse({'data':1})
		except:
			response = JsonResponse({'data':0})

	return response




	










