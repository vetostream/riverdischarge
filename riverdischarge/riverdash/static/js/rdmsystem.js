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
				$( ".device-reading-block" ).append('<blockquote><p>Sensor Alpha WL: '+value.devread_depth_sensor_one+' <br> Sensor Beta WL: '+value.devread_depth_sensor_two+'<br>Received: '+value.devread_received+'</p></blockquote>');
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
        'width':500,
        'height':100,
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

$( document ).ready(function(){
	console.log('document is ready...');
	var deviceObj = Device;
	var readingObj = Reading;
	deviceObj.getQuerySet();
	readingObj.getQuerySet();
	
	google.charts.load('current', {packages: ['corechart', 'line']});
	google.charts.setOnLoadCallback(drawBasic);
	$('#loader').hide();
});

$( document ).on('click',' #dashboard-btn ', function(){
	console.log("dashboard active");
	reveal("#dashboard");
	$( '.page-title' ).text("Dashboard");
});

$( document ).on('click',' #data-analysis-btn ',function(){
	console.log("devices active");
	reveal("#data-analysis");
	$( '.page-title' ).text("Data Gathered and Analysis");
});

$( document ).on('click',' #reports-btn ',function(){
	reveal("#reports-page");
	$( '.page-title' ).text("Reports");
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
	getSummaryDischarge($quarter);
});