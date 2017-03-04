//Device Object Schema

var Device = {
	getQuerySet:function(){
		$.ajax({
			url:'/devices',
			data:{},
			type:'GET',
			dataType:'json',
		}).done(function(response){
			$.each(response, function(key, value){
				$( "#device-list ").append("<tr data-id="+value.device_id+"><td>"+value.device_id+"</td><td>"+value.device_lat+"</td><td>"+value.device_lng+"</td><td id='device-batt'><b>Initializing...</b></td><td id='device-stat'><b>Initializing...</b></td></tr>");
			});
		}).fail(function(xhr, status, errThrown){
			console.log("Something went wrong.");
			console.log("Error: " + errThrown);
			console.log("Status: " + status);
			console.log(xhr);
		}).always(function(xhr, status){
			console.log("The request is complete!");
		});
	},
	getDeviceDetail:function($pk){
		$.ajax({
			url:'/devices/'+$pk,
			data:{},
			type:'GET',
			dataType:'json',
		}).done(function(response){
			console.log(response);
		}).fail(function(xhr, status, errThrown){
			console.log("Something went wrong. Cant give device detail.");
			console.log("Error: " + errThrown);
			console.log("Status: " + status);
			console.log(xhr);
		}).always(function(xhr, status){
			console.log("The request is complete!");
		});
	},
	getDeviceBattStat:function($device_id){
		$.ajax({
			url:'/devices/activity',
			data:{'device_id':$device_id},
			type:'GET',
			dataType:'json',
		}).done(function(response){
			console.log(response);
			$("#device-batt").html(response.device_batt);
            $("#device-stat").html("<b class='online-device'>"+response.device_status.toUpperCase()+"</b>");
		}).fail(function(xhr, status, errThrown){
			console.log("Something went wrong. Cant give device detail.");
			console.log("Error: " + errThrown);
			console.log("Status: " + status);
			console.log(xhr);
		}).always(function(xhr, status){
			console.log("The request is complete!");
		});
	},
	postDevice:function(){
		$.ajax({
			url:'/devices/'+$pk,
			data:{},
			type:'POST',
			dataType:'json',
		}).done(function(response){
			console.log(response);
		}).fail(function(xhr, status, errThrown){
			console.log("Something went wrong. Cant POST device.");
			console.log("Error: " + errThrown);
			console.log("Status: " + status);
			console.log(xhr);
		}).always(function(xhr, status){
			console.log("The request is complete!");
		});
	},
};

/* Reading Object Schema */
var Reading = {
	getQuerySet:function(){
		$.ajax({
			url:'/readings',
			data:{},
			type:'GET',
			dataType:'json',
		}).done(function(response){
			$.each(response, function(key, value){
				var devread_time = new Date(value.devread_time);
				var devread_received = new Date(value.devread_received);
				var devread_time_stringify = devread_time.getFullYear() + "-" + devread_time.getMonth() + "-" + devread_time.getDate() + "  T" + devread_time.getHours() + ":" + devread_time.getMinutes();
				var devread_received_stringify = devread_received.getFullYear() + "-" + devread_received.getMonth() + "-" + devread_received.getDate() + "  T" + devread_received.getHours() + ":" + devread_received.getMinutes();

				console.log("devread_time: " + devread_time_stringify + ", devread_received: "+devread_received_stringify);
				$( ".device-reading-block" ).append('<blockquote><p>Sensor Alpha WL: '+value.devread_depth_sensor_one+' <br> Sensor Beta WL: '+value.devread_depth_sensor_two+'\
					<br>Read Time: '+devread_time_stringify+'<br>Received: '+devread_received_stringify+'</p></blockquote>');
			});
		}).fail(function(xhr, status, errThrown){
			console.log("Something went wrong.");
			console.log("Error: " + errThrown);
			console.log("Status: " + status);
			console.log(xhr);
		}).always(function(xhr, status){
			console.log("The request is complete!");
		});
	},
	getDeviceDetail:function($pk){
		$.ajax({
			url:'/devices/'+$pk,
			data:{},
			type:'GET',
			dataType:'json',
		}).done(function(response){
			console.log(response);
		}).fail(function(xhr, status, errThrown){
			console.log("Something went wrong. Cant give device detail.");
			console.log("Error: " + errThrown);
			console.log("Status: " + status);
			console.log(xhr);
		}).always(function(xhr, status){
			console.log("The request is complete!");
		});
	},
	postDevice:function(){
		$.ajax({
			url:'/devices/'+$pk,
			data:{},
			type:'POST',
			dataType:'json',
		}).done(function(response){
			console.log(response);
		}).fail(function(xhr, status, errThrown){
			console.log("Something went wrong. Cant POST device.");
			console.log("Error: " + errThrown);
			console.log("Status: " + status);
			console.log(xhr);
		}).always(function(xhr, status){
			console.log("The request is complete!");
		});
	},
	getQuerySetSpecDate:function($date,$page,$status){
		$.ajax({
			url:'/readings/listing',
			data:{'dt':$date,'page':$page},
			type:'GET',
			dataType:'json',
		}).done(function(response){
			console.log(response);
			$("#data-reading-body").empty();
			var cnt = response.total;
			console.log(cnt);
			$.each(response, function(key, value){
				json_data = JSON.parse(value);
				$.each(json_data, function(key,value){
					$( "#data-reading-body" ).append('<tr><td>'+value.fields.devread_depth_sensor_one+'</td><td>'+value.fields.devread_depth_sensor_two+'</td><td>'+value.fields.devread_received+'</td></tr>').hide().fadeIn('fast');
				});
			});

			if ($status == 'paginate'){
				createPagination(cnt,10);
			}
			// var cnt = 0;
			// $.each(response, function(key, value){
			// 	cnt += 1;
			// 	$( "#data-reading-body" ).append('<tr><td>'+value.devread_depth_sensor_one+'</td><td>'+value.devread_depth_sensor_two+'</td><td>'+value.devread_received+'</td></tr>');
			// });

			// console.log(cnt);
			// createPagination(cnt,5);
		}).fail(function(xhr, status, errThrown){
			console.log("Something went wrong.");
			console.log("Error: " + errThrown);
			console.log("Status: " + status);
			console.log(xhr);
		}).always(function(xhr, status){
			console.log("The request is complete!");
			$('#loader').hide();
		});
	},
};


function getSummaryDischarge($quarter){
	$.ajax({
		url:'/machine/run',
		data:{'quarter':$quarter},
		type:'GET',
		dataType:'json',
	}).done(function(response){
		var monthNames = ["January", "February", "March", "April", "May", "June",
		  "July", "August", "September", "October", "November", "December"
		];		
		console.log(response);
		$("#data-summary").empty();
		$.each(response, function(key, value){
			json_data = JSON.parse(value);
			$.each(json_data, function(key,value){
				date_of_data = new Date(value.fields.devread_received);
				console.log(value.devread_received);
				$( "#data-summary" ).append('<tr><td>'+monthNames[date_of_data.getMonth()]+'</td><td>'+date_of_data.getDate()+'</td><td></td><td>'+value.fields.devread_depth_sensor_one+'</td><td>'+value.fields.devread_depth_sensor_two+'</td>').hide().fadeIn('fast');
			});
		});
		// var cnt = 0;
		// $.each(response, function(key, value){
		// 	cnt += 1;
		// 	$( "#data-reading-body" ).append('<tr><td>'+value.devread_depth_sensor_one+'</td><td>'+value.devread_depth_sensor_two+'</td><td>'+value.devread_received+'</td></tr>');
		// });

		// console.log(cnt);
		// createPagination(cnt,5);	
	}).fail(function(xhr, status, errThrown){
		console.log("Something went wrong.");
		console.log("Error: " + errThrown);
		console.log("Status: " + status);
		console.log(xhr);
	}).always(function(xhr, status){
		console.log("The request is complete!");
	});	
}

function process_regression($data_points){
	$.ajax({
		url:'/regression/calculate',
		data:$data_points,
		type:'GET',
		dataType:'json',
	}).done(function(response){
		if(response.err == '0'){
			$("#quote-regression").html("<blockquote><h5>The calculated values from your given data.</h5><br><h6><b>Power Regression Equation: y=\
				"+response.a+"(h)<sup>"+response.b+"</sup></b><br><b>a: "+response.a+"</b><br><b>b: "+response.b+"</b>\
				<br><b>r: "+response.r+"</b><br><b>r<sup>2</sup>: "+response.r2+"</b></h6></blockquote>");
			var $arr_date_chart = [['River Level','River Discharge']]
			var len_arr = response.data_plot.length;
			var count;
			for(count = 0; count < len_arr; count++){
				$arr_date_chart.push(response.data_plot[count]);
			}

			console.log($arr_date_chart);

			google.charts.load('current', {'packages':['corechart']});
	        var data = google.visualization.arrayToDataTable($arr_date_chart);

	        var options = {
	          title: 'River Level (h) vs River Discharge (Q)',
	          hAxis: {title: 'River Level (h)', minValue: 0, maxValue: response.maxvalh},
	          vAxis: {title: 'River Discharge (Q)', minValue: 0, maxValue: response.maxvalq},
	          legend: 'none'
	        };

	        var chart = new google.visualization.ScatterChart(document.getElementById('scatter_chart_regression'));

	        chart.draw(data, options);
	        $('#error-tag-regression').html("");
	        $('#content-regression').show();
		}else{
			console.log(response.err);
			$('#error-tag-regression').html(response.err);
			$('#content-regression').hide();
		}
	}).fail(function(xhr, status, errThrown,response){
		console.log("Something went wrong.");
		console.log("Error: " + errThrown);
		console.log("Status: " + status);
		console.log(xhr);
	}).always(function(xhr, status){
		console.log("The request is complete!");
		$('#loader-regression').hide();
	});	
}



function drawBasic() {

	$.ajax({
		url:'/readings/charting',
		data:{},
		type:'GET',
		dataType:'json',
	}).done(function(response){
		var array_data_points = [];

		$.each(response, function(key,value){
			date_of_data = new Date(value.devread_received);
			t_date = date_of_data.getHours();
			m_date = date_of_data.getMinutes();
			console.log(t_date + " " + m_date);
			array_data_points.push([date_of_data,parseFloat(value.devread_depth_sensor_one)]);
		});

	  console.log(array_data_points);
      var data = new google.visualization.DataTable();
      data.addColumn({type:'date', id:'Time'});
      data.addColumn({type:'number', id:'Water Level'});
      // data.addColumn(type:'float', 'X');
      // data.addColumn('number', 'RDM1111');

      data.addRows(array_data_points);

      var options = {
        hAxis: {
          title: 'Time'
        },
        vAxis: {
          title: 'Water Level'
        },
      };

      var chart = new google.visualization.LineChart(document.getElementById('dashboard-plot'));

      chart.draw(data, options);
	}).fail(function(xhr, status, errThrown){
		console.log("Something went wrong.");
		console.log("Error: " + errThrown);
		console.log("Status: " + status);
		console.log(xhr);
	}).always(function(xhr, status){
		console.log("The request is complete!");
	});
}

function drawWaterReading($date) {

	$.ajax({
		url:'/readings/charting',
		data:{'dt':$date},
		type:'GET',
		dataType:'json',
	}).done(function(response){
		var array_data_points = [];

		$.each(response, function(key,value){
			date_of_data = new Date(value.devread_received);
			t_date = date_of_data.getHours();
			m_date = date_of_data.getMinutes();
			console.log(t_date + " " + m_date);
			array_data_points.push([date_of_data,parseFloat(value.devread_depth_sensor_one)]);
		});

	  console.log(array_data_points);
      var data = new google.visualization.DataTable();
      data.addColumn({type:'date', id:'Time'});
      data.addColumn({type:'number', id:'Water Level'});
      // data.addColumn(type:'float', 'X');
      // data.addColumn('number', 'RDM1111');

      data.addRows(array_data_points);

      var options = {
        hAxis: {
          title: 'Time'
        },
        vAxis: {
          title: 'Water Level'
        },
      };

      var chart = new google.visualization.LineChart(document.getElementById('water-reading'));

      chart.draw(data, options);
	}).fail(function(xhr, status, errThrown){
		console.log("Something went wrong.");
		console.log("Error: " + errThrown);
		console.log("Status: " + status);
		console.log(xhr);
	}).always(function(xhr, status){
		console.log("The request is complete!");
	});
}


function reveal($div){
	$( ".main-wrapper" ).hide();
	$( $div ).show("slow");
}

function createPagination($numberOfData,$limitEntry){
	$( "#readings-pagination" ).empty();
	var $pages = $numberOfData/$limitEntry;
	var count;

	var $number_of_pages_context = "";

	for(count = 0; count < $pages-1; count++){
		var page = count+1;
		$number_of_pages_context += (page==1) ? '<li class="active pager" data-page="'+page+'"><a href="#!">'+page+'</a></li>':'<li class="pager" data-page="'+page+'"><a href="#">'+page+'</a></li>';
	}

	$( "#readings-pagination" ).append($number_of_pages_context);
}

function quarter_stream($data){
	$.ajax({
		url:'/regression/activate',
		data:$data,
		type:'GET',
		dataType:'text',
	}).done(function(response){
		console.log(response);
	}).fail(function(xhr, status, errThrown){
		console.log("Something went wrong.");
		console.log("Error: " + errThrown);
		console.log("Status: " + status);
		console.log(xhr);
		$('.error-tag').show();
	}).always(function(xhr, status){
		console.log("The request is complete!");
	});	
}

function get_quarter_constants($quarter,$year){
	$.ajax({
		url:'/regression/constants',
		data:{'quarter':$quarter,'year':$year},
		type:'GET',
		dataType:'json',
	}).done(function(response){
		$('.error-tag').hide();
		if(response.data_points.length === 0){
			$("#quarter-constants").hide("slow");
			$("#quarter-wrapper").show("slow");
			console.log("Date" + response.data_points);			
		}else{
			$("#print-stream").attr('href',"/reports/stream/?quarter="+$quarter+"&year="+$year);			
			$("#quarter-constants").show("slow");
			$("#quarter-wrapper").hide("slow");
			console.log('#quarter-wrapper hidden');
			$.each(response.data_points,function(key,value){
				if($quarter == 1){
					$("#quarter-table-data").append('<tr><td>'+((key <= 1) ? 'January':(key <= 3 ? 'February':(key <=5 ? 'March':'')))+'</td>\
						<td>'+value[0]+'</td><td>'+value[1]+'</td></tr>');
				}else if($quarter == 2){
					$("#quarter-table-data").append('<tr><td>'+((key <= 1) ? 'April':(key <= 3 ? 'May':(key <=5 ? 'June':'')))+'</td>\
						<td>'+value[0]+'</td><td>'+value[1]+'</td></tr>');
				}else if($quarter == 3){
					$("#quarter-table-data").append('<tr><td>'+((key <= 1) ? 'July':(key <= 3 ? 'August':(key <=5 ? 'September':'')))+'</td>\
						<td>'+value[0]+'</td><td>'+value[1]+'</td></tr>');				
				}else{
					$("#quarter-table-data").append('<tr><td>'+((key <= 1) ? 'October':(key <= 3 ? 'November':(key <=5 ? 'December':'')))+'</td>\
						<td>'+value[0]+'</td><td>'+value[1]+'</td></tr>');
				}
			});

		  $("#quarter-regression-constants").html("<blockquote><h5>The calculated values from your given data.</h5><br><h6><b>Power Regression Equation: y=\
		  	"+response.a+"(h)<sup>"+response.b+"</sup></b><br><b>a: "+response.a+"</b><br><b>b: "+response.b+"</b>\
		  	<br><b>r: "+response.r+"</b><br><b>r<sup>2</sup>: "+response.r2+"</b></h6></blockquote>");
		  google.charts.load('current', {packages: ['corechart', 'line']});
	      var data = new google.visualization.DataTable();
	      data.addColumn('number', 'h');
	      data.addColumn('number', 'Q');
	      console.log(response.data_function);
	      data.addRows(response.data_function);

	      var options = {
	        hAxis: {
	          title: 'River Discharge (Q)',
	          minValue:0,
	          maxValue:10
	        },
	        vAxis: {
	          title: 'Adjusted River Stage (h)',
	          minValue:0,
	          maxValue:1
	        },
	        legend:'none',
	        title:'Rating Curve Quarter ' + $quarter + ' of '+$year,
	      };

	      var chart = new google.visualization.LineChart(document.getElementById('rating-curve'));

	      chart.draw(data, options);			

		}
	}).fail(function(xhr, status, errThrown){
		console.log("Something went wrong.");
		console.log("Error: " + errThrown);
		console.log("Status: " + status);
		console.log(xhr);
		$('.error-tag').show();
	}).always(function(xhr, status){
		console.log("The request is complete!");
	});		
}


function get_avg_measurement($month,$year){
	$.ajax({
		url:'/readings/daily/avgdischarge',
		data: {'river-month':$month,'river-year':$year},
		type:'GET',
		dataType:'json',
	}).done(function(response){
		// if(response.readings === []){
		// 	alert("test");
		// }
		json_p = JSON.parse(response.readings);
		if (json_p.length == 0){
			$('.error-tag-river').show();
			$('.error-tag-river-cons').hide();
		}else{
			$('.error-tag-river').hide();
			$('.error-tag-river-cons').hide();
			$('#quarter-constants-select-river').show("slow");
		}

		$.each(response,function(key,value){
			json_data = JSON.parse(value);
			$("#quarter-table-data-river").empty();
			$.each(json_data,function(key,value){
				$day = new Date(value.fields.discharge_date);
				$("#quarter-table-data-river").append("<tr><td>"+$day.getDate()+"</td><td>"+value.fields.discharge+"</td><td>"+value.fields.stage+"</td></tr>");
			});
		});


	}).fail(function(xhr, status, errThrown){
		console.log("Something went wrong.");
		console.log("Error: " + errThrown);
		console.log("Status: " + status);
		console.log(xhr);
		$('.error-tag-river-cons').show();
	}).always(function(xhr, status){
		console.log("The request is complete!");
	});
}



$( document ).on('click',' #dashboard-btn ', function(){
	console.log("dashboard active");
	reveal("#dashboard");
	$( '.page-title' ).text("Dashboard");
});

$( document ).on('click',' #data-analysis-btn ',function(){
	console.log("devices active");
	reveal("#data-analysis");
	$( '.page-title' ).text("Daily River Stages");
});

$( document ).on('click',' #reports-btn ',function(){
	reveal("#reports-page");
	$( '.page-title' ).text("Streamflow Measurements");
});

$( document ).on('click',' #regression-btn ',function(){
	reveal("#regression-page");
	$( '.page-title' ).text("Power Regression");
});

$( document ).on('click',' #river-discharge-machine ',function(){
	reveal("#river-discharge-machine-page");
	$( '.page-title' ).text("Averaged Daily Measurements");
});

$('.datepicker').pickadate({
	selectMonths: true, // Creates a dropdown to control month
	selectYears: 15 // Creates a dropdown of 15 years to control year
});

$( document ).on('change', '.datepicker',function(){
	console.log("Date picked.");
	var reading_obj = Reading;

	var $dateVal = $( ".picker__input" ).val();
	var $page = 1;
	console.log($dateVal);
	reading_obj.getQuerySetSpecDate($dateVal,$page,'paginate');
	google.charts.load('current', {packages: ['corechart', 'line']});
	google.charts.setOnLoadCallback(drawWaterReading($dateVal));
});

$( document ).on('click','#go-chart',function(){
	var $dateVal = $( ".picker__input" ).val();
	google.charts.load('current', {packages: ['corechart', 'line']});
	google.charts.setOnLoadCallback(drawWaterReading($dateVal));
});

$( document ).on('click','.pager',function(){
	var $dateVal = $( ".picker__input" ).val();
	var $page = $(this).data('page');

	var reading_obj = Reading;
	reading_obj.getQuerySetSpecDate($dateVal,$page,'');
	$('#loader').show();
	$("ul.pagination").find("li").removeClass('active');
	$(this).addClass('active');
});

$( document ).on('change',' #quarter-select ',function(){
	// queryDischarge();
	$quarter = $('select[name="quarter"]').val();
	$year = $("input[name='year']").val();
	// console.log($year);
	get_quarter_constants($quarter,$year);
	// $("#quarter-wrapper").show("slow");

	if ($quarter == 1){
		$("#aone").html("January I");
		$("#atwo").html("January II");
		$("#bone").html("February I");
		$("#btwo").html("February II");
		$("#cone").html("March I");
		$("#ctwo").html("March II");
	}else if($quarter == 2){
		$("#aone").html("April I");
		$("#atwo").html("April II");
		$("#bone").html("May I");
		$("#btwo").html("May II");
		$("#cone").html("June I");
		$("#ctwo").html("June II");
	}else if($quarter == 3){
		$("#aone").html("July I");
		$("#atwo").html("July II");
		$("#bone").html("August I");
		$("#btwo").html("August II");
		$("#cone").html("September I");
		$("#ctwo").html("September II");		
	}else{
		$("#aone").html("October I");
		$("#atwo").html("October II");
		$("#bone").html("November I");
		$("#btwo").html("November II");
		$("#cone").html("December I");
		$("#ctwo").html("December II");		
	}
	// getSummaryDischarge($quarter);
});


$( document ).on('submit','form[id="regression-form"]',function(e){
	e.preventDefault();
	console.log($(this).serialize());
	$('#loader-regression').show();
	process_regression($(this).serialize());
});

$( document ).on('submit','form[id="quarter-datum"]',function(e){
	e.preventDefault();
	var $data = $(this).serialize()+"&quarter="+$('select[name="quarter"]').val()+"&year="+$("input[name='year']").val();
	console.log($data);
	quarter_stream($data);
	$('.error-tag').hide();
	// $('#loader-regression').show();
	// process_regression($(this).serialize());
});

$( document ).on('change','input[name="year"]',function(){
	$quarter = $('select[name="quarter"]').val();
	$year = $(this).val();
	// console.log($year);
	get_quarter_constants($quarter,$year);
});

$( document ).on('change','input[name="river-year"]',function(){
	$month = $('select[name="river-month"]').val();
	$year = $('input[name="river-year"]').val();
	// console.log($year);

	get_avg_measurement($month,$year);
});

$( document ).on('change','select[name="river-month"]',function(){
	$month = $('select[name="river-month"]').val();
	$year = $('input[name="river-year"]').val();

	get_avg_measurement($month,$year);
});

// $( document ).on('click','#print-stream',function(){
// 	$quarter = $('select[name="quarter"]').val();
// 	$year = $("input[name='year']").val();

// 	$.ajax({
// 		url:'/reports/stream',
// 		data:{'quarter':$quarter,'year':$year},
// 		type:'GET',
// 		dataType:'text',
// 	}).done(function(response){
// 		console.log(response.url);
// 	}).fail(function(xhr, status, errThrown){
// 		console.log("Something went wrong.");
// 		console.log("Error: " + errThrown);
// 		console.log("Status: " + status);
// 		console.log(xhr);
// 		$('.error-tag').show();
// 	}).always(function(xhr, status){
// 		console.log("The request is complete!");
// 	});	
// });


$( document ).ready(function(){
	console.log('document is ready...');
	var deviceObj = Device;
	var readingObj = Reading;
	deviceObj.getQuerySet();
	deviceObj.getDeviceBattStat('RDM1111');
	readingObj.getQuerySet();
	
	google.charts.load('current', {packages: ['corechart', 'line']});
	google.charts.setOnLoadCallback(drawBasic);
	$('#loader').hide();
	$('#loader-regression').hide();
	$('#content-regression').hide();
	$('#quarter-wrapper').hide();
	$('#quarter-constants').hide();
	$('#quarter-constants-select-river').hide();
});