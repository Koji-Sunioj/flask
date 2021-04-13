

function parse_calendar() 
{	
	
		
   

	function normalize_modal_contract()
	{
		//uncheck supplement box, remove values so it isn't submitted
		$('#add_supplement input:checkbox').prop( "checked", false );
		$('#add_supplement').hide();
		//uncheck years box, remove values so it isn't submitted
		$('#add_google_years input:checkbox').prop( "checked", false );
		$('#add_google_years').hide();
		//uncheck supplement box, remove values so it isn't submitted
		$('#supplement_table tbody tr').remove();
		$("#supplement_table").hide();
		$('#create_contract').hide();
		$('#new_contract_years').hide();
		$("#parse_years option:selected").prop("selected", false)
	}

	//set width of table for supplement values
	$('#cloner tr td').css('width','20%');	

	//set css values for values in data table whose age is this month, or more
	var today = new Date();
	var mm = String(today.getMonth() + 1).padStart(2, '0');
	var yyyy = today.getFullYear();
	var today =yyyy + '-'+  mm;
	var this_month = $(`#${yyyy}`).find(`td:contains(${today})`);
	this_month.parent().css('color','blue').attr('title', 'fetched from Google calendar');
	this_month.parent().nextAll().prev().css('color','blue').attr('title', 'fetched from Google calendar');

	var months = [];
	var test_series = []
	//create header for each table based on their id
	$('table.dataframe.table').each(function(){
		var table_id = $(this).attr('id');
		table_json = {
			name: table_id,
			data: []
		 }
		
		$(this).find('tr:last').css('background-color','#f0e9c7');
		$(this).find('td:last-child').css('background-color','#f0e9c7');
		$(this).before(`<h1>${table_id}</h1>`);
	
		$(this).find('tr').each(function() {
			var month = $(this).find('td:first').text();
			var estimate = $(this).find('td:last').text();
			if (isNaN(	parseInt(month.substring(5, 7))) )
			{	

			}
			else 
			{
				table_json.data.push(parseFloat( estimate.substring(1).replace(/,/g, '')) );
				months.push(month.substring(5, 7));
			}
		}) 
		
		
		
		; 
		test_series.push(table_json);
	});
	
	var unique = new Set(months);
	chart= {
        type: 'column'
    };

	title = {
		  text: 'Estimated paychecks'   
	   };
   
	   subtitle= {
	   text: 'by year, month number'
	 };
	
	 
	 xAxis = { crosshair: true,
		categories: Array.from(unique),
		title: {
            enabled: true,
            text: 'month number',
            style: {
                fontWeight: 'normal'
			},
			
        }
	 };
	  yAxis = {
		title: {
		   text: 'Euros \u20AC'
		},
		plotLines: [{
		   value: 0,
		   width: 1,
		   color: '#808080'
		}]
	 };   
 
	  tooltip = {
		valuePrefix: '\u20AC '
	 }
	  legend = {
		layout: 'vertical',
		align: 'left',
		verticalAlign: 'middle',
		borderWidth: 1
	 };
	
 
	  json = {};
	 json.title = title;
	 json.chart = chart;
	 json.xAxis = xAxis;
	 json.yAxis = yAxis;
	 json.tooltip = tooltip;
	// json.legend = legend;
	 json.series = test_series.reverse();
	 json.subtitle = subtitle;
 
	 $('#highchart').highcharts(json);
	 Highcharts.setOptions({
	 lang: {
	   thousandsSep: ','
   		}, 
   	chart : {
		type: 'column'
		}
 		});


	$('.btn-close').on('click',function() {
		normalize_modal_contract()
		$('input[name=employer]').val(''); 
		$('select[name=paydate_month_offset]').prop("selectedIndex", 0).val(); 
		$('input[name=base]').val('');
		$('#paymet_rules').hide();
	});


	//show modal form on click
	/*$(document).on('click', '#settings_toggle', function() {
		
		$('#settings').modal('show');
		
		});
*/
	// event lister for both employer name and paydate offset:

	$(document).on('change', 'select[name=paydate_month_offset]', function() {
		var employer = $('input[name=employer]').val();
		var month_offset = $(this).val();
		if (employer.length > 0 && month_offset >= 0) 

		{
			$('#paymet_rules').show();
		}
		
		else 
		{
			$('#paymet_rules').hide();
			normalize_modal_contract();
			$('input[name=base]').val('');
		}
	});


	$(document).on('keyup', 'input[name=employer]', function() {
		var employer = $(this).val();
		var month_offset = $('select[name=paydate_month_offset]').val();
		if (employer.length > 0 && month_offset >= 0) 

		{
			$('#paymet_rules').show();
		}
		
		else 
		{
			$('#paymet_rules').hide();
			normalize_modal_contract();
			$('input[name=base]').val('');
		}
	});

	//event listener for keying base input, render three items, ready button, checkboxes for adding years and supplements

	$(document).on('keyup', 'input[name=base]', function() {

	
		
		//hide and remove values if input is keyed to zero
		if (!$(this).val())
		{ 	
			normalize_modal_contract()	
		}

		else if ($.isNumeric($(this).val()) == false) 
		{
			normalize_modal_contract()
			$('#message').text('numbers only');
			$('#message').show();	
		}

		else  
		{
			$('#message').hide();
			$('#add_supplement').show();
			$('#add_google_years').show();
			$('#create_contract').show();
		}


	});

	$('#add_supplement').on('change',function()
	{	
		var row_template = $("#cloner tr").clone();
		if ($(this).children().find('input').is(':checked'))
		{	

			$("#supplement_table tbody").html(row_template);
			$("#supplement_table").show();
		}

		else 
		{
			$("#supplement_table").hide();
			$('#supplement_table tbody tr').remove();
		
		}
		
	})

	$('#add_google_years').on('change',function()
	{	
		if ($(this).children().find('input').is(':checked'))
		{
			$("#new_contract_years").show();
		}

		else 
		{
			$("#new_contract_years").hide();
			$("#parse_years option:selected").prop("selected", false)
		}
		
	})
	
	//changing the value of the button text when selecting checkboxes for table row
	$(document).on('click', '.dropdown_check', function() {
		var selected = [];
		$(this).parent().find('input:checked').each(function() {
			selected.push($(this).val());
		});
		
		//alert($(this).find('input:checkbox').val());
		var new_val = $(this).text();
		var numberOfChecked = $(this).parent().find('input:checkbox:checked').length;
		var button_text = $(this).parent().siblings('button');
		var hidden_arr = $(this).parent().siblings('input:hidden');
		hidden_arr.val( `[${selected}]`)
		if (numberOfChecked > 1)
		{
			button_text.text(`${numberOfChecked} selected`);
		}
	
		else if (numberOfChecked == 0)
	
		{
			button_text.text('Select days');
		}
	
		else 
		{
			button_text.text(new_val);
			
		}
			
		});

	$(document).on('change', 'select[name=start_times]', function() {
			
		var start =  parseInt($(this).val());
		var start_index = $(this).parent().find(`select option[value=${start}]`).index();
		var end = $(this).parent().next();

		if (start >= parseInt(end.find('select option:selected').val())) 
		{
			end.find('select').prop("selectedIndex", start_index).val(); 
		}
	
		$(end.find('select option')).each(function(index) 
			  
			{ 
			var check_option = $(this);
			if (parseInt(check_option.val())  <= start)
			{
				check_option.prop('disabled',true);
				
			}

			else 
			{

				check_option.prop('disabled',false);
			}
				
			});
				
		});
	
	//deleting table row
	$(document).on('click', '#del_row', function() {
		event.preventDefault();
		if ($('#supplement_table tr').length > 2)
		{
			$('#supplement_table tr:last').remove();
		}
	});


	//adding a row
	$('#add_row').on('click',function()
	{	
		event.preventDefault();
		var row_template = $("#cloner tr").clone();
		$("#supplement_table").find('tbody').append('<tr>'+row_template.html()+'</tr>');
	})  

	$('form[name=new_contract]').on('submit', function(event) {
	
		var form = $(this);
		
		var empty_table_check = [];
		var unique_base_chec = [];
		var num_chec = [];

		$("#supplement_table tbody tr").each(function(){

			var row = $(this);
			unique_base_chec.push(row.find('input[name=rule_name]').val())
			num_chec.push($.isNumeric(row.find('input[name=rate]').val()))
			if (!row.find('input[name=days_arr]').val() || !row.find('input[name=rule_name]').val() || !row.find('input[name=rate]').val() || row.find('select[name=start_times]').val() == 'Start time' ||row.find('select[name=end_times]').val() == 'End time' ) 
			{
				empty_table_check.push(true);
			}
			
		});
		var orig_rules = unique_base_chec.length;
		var unique_rules = $.uniqueSort(unique_base_chec).length;
		
		
		if ($("#add_google_years input:checkbox").is(":checked") && !$("#parse_years option:selected").is(':selected') || $.inArray(true, empty_table_check) == 0 || orig_rules != unique_rules || $.inArray(false, num_chec) == 0) 
		{	
			event.preventDefault();
			$('#message').text('empty values in supplement table, parse years or non unique rule names exist');
			$('#message').show();	
		}

		else 
		{	
			event.preventDefault();
			var employer = $('input[name=employer]').val();
			$('#message').hide();
			$.ajax({
				data : 
				{	
					employer : employer
				},
				type : 'POST',
				url : '/contract_validation'
			})
			.done(function(data)
			{
			
			if (data.error)
			
			{
				
				$('#message').text(data.error);
				$('#message').show();
			}
			else
			{   
				///event.preventDefault();
				form[0].submit();
			}

			})
		}
		
	})

// ajax checking if contract exists , used when contract is available, might change it to seperate modal form
	$(document).on('change', 'select[name=search_parameter]', function() {
		var year_selector = $('select[name=year]');
		var calendar_parser  = $('#calendar_parser');
		var search_parameter = $(this).val();
		$('select[name=year] option').remove();
		year_selector.show();
		calendar_parser.show();
		
		if (search_parameter != 'contract')

		{
		$.ajax({
			data : 
			{	
				search_parameter : search_parameter
			},
			type : 'POST',
			url : '/year_validation/'
		})
		.done(function(data) 
		 {
			var years = JSON.parse(data);

			$.each(years, function(index, value) {
			if (value.inserted == 12)
			{
				year_selector.append($("<option></option>").attr("value", value.year).text(value.year).prop("disabled",true).css("color","green").append("&#10003;").attr('title','complete year'))
			}
			else 
			{
				year_selector.append($("<option></option>").attr("value", value.year).text(value.year).attr('title',`${value.inserted} months parsed for this year`)); 
			}
				
			});
			
			
		 })
		}
		
		else 
		{
			year_selector.hide();
			calendar_parser.hide();
		}

	});

	
/*
	$(document).on('click', '#create_contract', function() {
		
		event.preventDefault();
		var employer = $('input[name=employer]').val();
		var paydate_month_offset = $('select[name=paydate_month_offset]').val();
		$.ajax({
			data : 
			{	
				employer : employer,
				paydate_month_offset : paydate_month_offset
			},
			type : 'POST',
			url : '/contract_validation'
		})
		.done(function(data) 
		{ 
			var message_div = $('#ajax_message'); 
		if (data.success)
		{
			message_div.text(data.success);
			message_div.show();
		}
		else 

		{	message_div.attr('class','alert alert-warning')
			message_div.text(data.error);
			message_div.show();
		}
			
		 })


	
	});*/


	



}


function task_page() {
	
	$("p.card-text.errand").css('color','red');
	$("p.card-text.work").css('color','blue');
	$("p.card-text.fun").css('color','green');

	
	

	$('#flexCheckChecked').on('click', function ()
	{
		var checkBox = document.getElementById("flexCheckChecked");
		var text = document.getElementById("text");
		if (checkBox.checked == false)
		{
		  text.style.display = "inline";
		} 
		else 
		{
		   text.style.display = "none";
		}
	  });

	  $(document).on('change', '#fromtime', function() {
		var today = new Date($(this).val());

		$('.to_time').each(function( )
			{ 	target_disable = $(this);
				temp_date = new Date($(this).val());
				if (temp_date<=today) 
				{	
					target_disable.prop('disabled',true);
				}
				else 
				{
					target_disable.prop('disabled',false);
				}

			});
	
		});

		$('#to_do').on('submit', function(event){
			event.preventDefault();
			var form = $(this);
			var checkBox = document.getElementById("flexCheckChecked");
			var category = $('select[name=category]').val();
			var title = $('input[name=title]').val().trim();
			var from_time = $('#fromtime').val();
			var to_time = $('#totime').val(); 

			 if (checkBox.checked)
				
			 {	
				 if (!category || !title)
				{
					$('#warning').text('fill in the fields bro');
					$('#warning').show();
				} 

				else if ($("div.card-body").length> 0)
				{
					$('#warning').text($("div.card-body").length+ ' task(s) already exist for this day!');
					$('#warning').show();
				} 
				else 
				{	form[0].submit();
			
				}
			 }

			 else if (!checkBox.checked)
			 {
				if (!from_time || !to_time || !category || !title)
				{
					$('#warning').text('fill in the fields bro');
					$('#warning').show();
				}
				else 

				{	
					var start_date = new Date(from_time);
					var start_hours = start_date.getHours();
					var end_date =  new Date(to_time);
					var end_hours = end_date.getHours();
					var user_times = [];

					var screen_times = [];
					if (end_hours == 0)
					{
						end_hours = 24;
					}
					for (i = 0; i < end_hours - start_hours; i++) 
					{	
						user_times.push(start_hours + i)
					}
					
					$("p.card-subtitle.mb-2.text-muted").each(function() {
					
						screen_start = parseInt($( this ).text().split('to')[0].split(':')[0]);
						screen_end = parseInt($( this ).text().split('to')[1].split(':')[0]);
						var temp_times = []
						if (screen_end == 0)
						{
							screen_end = 24;
						}
						for (i = 0; i < screen_end - screen_start; i++) 
						{	
							temp_times.push(screen_start + i)
						}
						screen_times.push(temp_times);
						
					  });
					  var bool_array = []
					  for (i = 0; i < screen_times.length; i++) 
					  {
						
						bool_array.push(user_times.some(r=> screen_times[i].includes(r)));

					  }

					  const is_true = (element) => element === true;
					  if (bool_array.some(is_true))
					  {
						var task_count = bool_array.filter(Boolean).length;
						$('#warning').text(task_count + ' task(s) already exist for those times bro');
						$('#warning').show();

					  }
					  else 
					  {	
						form[0].submit();

					  }
					
				}

			 }

		})

}


function calendar() 

{	
	

	if ($('a.navbar-brand:nth-of-type(5)').text().includes('guest'))
	{
		$('#calendar').find('a').css('pointer-events','none');
	
	}
	
	;
	$('#calendar').find('a').css('text-decoration','none');
	$('#calendar').find('li.fun').css('color','green');
	$('#calendar').find('li.work').css('color','blue');
	$('#calendar').find('li.errand').css('color','red');


	$('.someClass').text(function() 
	{  
		if ($(this).prev().find('li').length > 5) 
			{
				return $(this).prev().find('li').length - 5 + ' more item(s)'
			}
		
	});
	$(document).ready( function() {
		var today = new Date();
    	var dd = String(today.getDate()).padStart(2, '0');
   		var mm = String(today.getMonth() + 1).padStart(2, '0');
    	var yyyy = today.getFullYear();
		var today =yyyy + '-'+  mm + '-'+  dd;
		
		var todays_tile = $('input[value='+today+']');
		todays_tile.parent().css("background-color","#FFF5DC");
		todays_tile.parent().find('a').css({
			'padding' : '5px',
			'border-radius' : '50%',
			'background-color' : 'white',
		 });
		
		var calendar_focus = $('#calendar_focus').text();
		var calendar_date = new Date(calendar_focus);
		var calendar_date_month = String(calendar_date.getMonth()+1).padStart(2, '0');
		var calendar_date_year= String(calendar_date.getFullYear());
		var comparison_year_mo = calendar_date_year+calendar_date_month

		$('input[name=date').each(function(index) 
		{	hidden_input = $( this );
			if (hidden_input.val().replace(/-/g, "").substring(0,6) !=comparison_year_mo ) 
			{	
				console.log(  index + ": " + $( this ).val().replace(/-/g, "").substring(0,6) );
				hidden_input.parent().css("background-color","#e6f0ff");
			}
			
		  });
	})

	




}

function check_photo()
{	$('#profile_message').hide();
$('#avatar').attr('title', 'change avatar');
	$('#avatar').on('click',function()
	{
		$('input[type=file]').trigger('click');  
	})

	$('input[type=file]').on('change',function()
	
	{	var form = $(this).parent();
		var alllowed_files = ["image/png","image/jpg","image/jpeg"];
		var file_input = $('input[name=file]').val();
		if (!file_input)
		{	
			$('#profile_message').text('empty field bro!');
			$('#update_success').hide();
			$('#profile_message').show()
		}
		else 
		{	
			files = $('input[name=file]').prop('files');
			for (var i = 0; i < files.length; i++) 
			{
					file = files.item(i);
			}
			if (alllowed_files.includes(file.type))
			
			{
				form[0].submit();
			}

			else 
			{	
				$('#profile_message').text('wrong file type bro');
				$('#update_success').hide();
				$('#profile_message').show();
			}
		}
	})
	
}

function search_check()

{   

	function normalize_modal() 
	{
		$('#myModal').modal('hide');
		setTimeout(function()
		{  	$('#myModal').find('input[name=title]').prop( "disabled", false )
			$('#myModal').find('textarea[name=post]').prop( "disabled", false )
			$('#myModal').find('input[name=thread_id]').remove();
			$('#myModal').find('.btn-group.col-6:nth-of-type(1)').find('button').attr('id','new_post')
			$('#new_post').text('Submit')
			$('#myModal').find('.btn-group.col-6:nth-of-type(2)').find('button').attr('id','cancel_post')
			$('#myModal').find('input:text').show();
			$('#myModal').find('input:text').val('');
			$('#myModal').find('textarea').show();
			$('#myModal').find('textarea').val('');
			$('#myModal').find('.form-group:nth-of-type(1)').find('label').text('title');
			$('#myModal').find('.form-group:nth-of-type(2)').find('label').text('post');
			$('#myModal').find('h4').text('make a post bitch');
			$('#modal_error').hide();
			$('#modal_error').text('');
		}, 1000)
	}
	
	$(function() 
	{
		if ($('#message_success').length == 1)
		{ 	 
			var highlight_target = $('.data_table:nth-of-type(1)')
			setTimeout(function() 
			{
				highlight_target.removeClass("highlight");
		  	}, 2000);
		  	highlight_target.addClass("highlight");
		} 
	});







	$(".dropdown-item[name='delete']").on('click',function(event)
		{	
			$('#myModal').find('input[name=title]').prop( "disabled", true )
			$('#myModal').find('textarea[name=post]').prop( "disabled", true )
			event.preventDefault();
			var thread_id = $(this).parents().eq(5).find('input[name=thread_id]').val();
			var title = $(this).parents().eq(5).find('td:nth-of-type(1)').text();
			var stamp = $(this).parents().eq(5).find('td:nth-of-type(3)').find('p').text();
			var post = $(this).parents().eq(5).find('input[name=post]').val().trim();
			$('#myModal').find('h4').text('are you sure wanna delete this?');
			$('#myModal').find('.form-group:nth-of-type(1)').find('label').text('title: '+title);
			$('#myModal').find('.form-group:nth-of-type(2)').find('label').text('post: '+post);
			$('#myModal').find('.form-group:nth-of-type(2)').find('label').append('<p>created: '+stamp+'</p>')
			$('#myModal').find('input:text').hide();
			$('#myModal').find('textarea').hide();
			$('#new_post').attr("id","delete_post");
			$('#cancel_post').attr("id","cancel_delete");
			$('#myModal').find('form[name=modal]').append('<input type="hidden" value='+thread_id+' name="thread_id">');
			$('#delete_post').text('Delete');
			$('#myModal').modal('show');
		});


	$(document).on('click','#cancel_delete',function(event)
		{ 
			event.preventDefault();
			normalize_modal();
		});


	$(".dropdown-item[name='edit']").on('click',function(event)
		{	
			event.preventDefault();
			var thread_id = $(this).parents().eq(5).find('input[name=thread_id]').val();
			var title = $(this).parents().eq(5).find('td:nth-of-type(1)').text();
			var post = $(this).parents().eq(5).find('input[name=post]').val();
			window.title = title;
			window.post = post;
			$('#myModal').find('h4').text('edit your damn post')
			$('#myModal').find('input:text').val(title);
			$('#myModal').find('textarea').val(post);
			$('#new_post').attr("id","edit_form");
			$('#cancel_post').attr("id","cancel_edit");
			$('#myModal').append('<input type="hidden" value='+thread_id+' name="thread_id">')
			$('#modal_error').hide();
			$('#myModal').modal('show');
		});

	$(document).on('click','#edit_form', function(event) {
		event.preventDefault();
		var edited_title = $('#myModal').find('input:text').val();
		var edited_post = $('#myModal').find('textarea').val();
		var thread_id = $('#myModal').find('input:hidden').val();

		if (window.title ==  edited_title || window.post ==  edited_post)
		{	$('#modal_error').text('');
			$('#modal_error').show();
			$('#modal_error').text('nothing new bro');
		}
		else { 

		$.ajax({
			data : 
			{	
				thread_id : thread_id,
				edited_title : edited_title,
				edited_post : edited_post
			},
			type : 'POST',
			url : '/thread_edit_ajax'
		})

		.done(function()
		{	
			
			$('tbody').find('input[value='+thread_id+']').parents().eq(3).find('td:nth-of-type(1)').html('<strong>'+edited_title+'</strong>');
			
			var highlight_target_target = $('tbody').find('input[value='+thread_id+']').parents().eq(3)

			setTimeout(function() {
				highlight_target_target.removeClass("highlight");
			  }, 2000);
			  highlight_target_target.addClass("highlight");

			normalize_modal();
			$('#query_message').attr('class','alert alert-success')
			$('#query_message').text('post edited!');
			$('#message_success').hide();
			$('#query_message').show();
		})
			}
	});



	$(document).on('click','#cancel_edit', function(event) 
	{
		event.preventDefault();
		normalize_modal();
	});


	//$(document).on('click',function(event) 
	//{
	//	if (event.target.className !== 'btn btn-link dropdown-toggle')
	//	{
	//		$(".dropdown-edit_form").hide();
	//	}
	//});
		
	$('.btn.btn-link.dropdown-toggle').on('click',function() 
	{
		var dropdown_button = $(this);
		var dropdown_menu = dropdown_button.parent().find('ul');
			
		if (dropdown_menu.is(":visible")) 
		{
			$(".dropdown-edit_form").hide();
		}
			
		else 
		{   
			$(".dropdown-edit_form").hide();
			dropdown_menu.toggle();	
		}
	});


$('#show_me').on('click',function() 
{
	$('#myModal').modal('show');
	$('#modal_error').hide();
})


$(document).on('click','#cancel_post',function(event)
	{ 
		event.preventDefault();
		normalize_modal();
		
	});


	$(document).on('click','#new_post', function(event) {
	
		var form = $(this);
		var new_title = $('#myModal').find('input:text').val().trim();
		var new_post = $('#myModal').find('textarea').val().trim();
		
		if (!new_title || !new_post)
			  { event.preventDefault();
				$('#modal_error').text('');
				$('#modal_error').show();
				$('#modal_error').text('fill in the fields bro');
			}
		else 
			{
			 form[0].submit();
			  }
	
	});
	
	$('form[name=search]').on('submit', function(event) 
	{
	event.preventDefault();
	var form = $(this);
	query = $(this).find('input[name=query]').val().trim();
	if (!query ) 
	{ 	$('#query_message').attr('class','alert alert-warning')
		$('#query_message').show();
		$('#query_message').text('empty search field brah');
		$('#message_success').hide();
	}
	else 
	{
		$.ajax({
		data : 
		{
			query : query
		},
		type : 'POST',
		url : '/forum_validation'
	 })
	
	 .done(function(data) 
	 {
		if (data.error) 
		{	$('#query_message').attr('class','alert alert-warning')
			$('#query_message').show();
			$('#query_message').text(data.error);
			$('#message_success').hide();
		}
		else 
		{
			form[0].submit();	
		}
	 });}
	});

}


//login page
function login_page()
{
	$('form').on('submit', function(event) {

	event.preventDefault();
	var form = $(this);
	email_username = $(this).find('input[name ="email_username"]').val().trim();
	password = $(this).find('input[name ="password"]').val().trim();

	if (!email_username || !password) 
	
	{ $('#login_error').show();
	$('#login_error').text('please fill all fields');}
	
	else {$.ajax({
		data : 
		{
			email_username : email_username,
			password : password,
		},
		type : 'POST',
		url : '/user_validation'
	 })
	
	 .done(function(data) 
	 {
		if (data.error) 
		{
			$('#login_error').show();
			$('#login_error').text(data.error);
		}
		else 
		{
			form[0].submit();
		}
	 });}
	});
}

//create profile
function create_profile()

{

	function isEmail(email) {
		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
		return regex.test(email);
	  }


	$('form').on('submit', function(event) 
	
	{
		event.preventDefault();
		var form = $(this);
		var username = $('input[name=username]').val().trim();
		var email = $('input[name=email]').val().trim();
		var home_town = $('input[name=home_town]').val().trim();
		var password = $('input[name=password]').val().trim();
		var password_confirm = $('input[name=password_confirm]').val().trim();
		
		if ( !username || !email || !home_town ||  !password || !password_confirm)
				
		{
			$('#create_error').show();	
			$('#create_error').text('fill all fields');
		}

		else if ( username.length < 5)
		{

			$('#create_error').show();	
			$('#create_error').text('username needs to be at least 5 letters');
		}
	
		else if ( !isEmail(email))
		{

			$('#create_error').show();	
			$('#create_error').text('email not valid');
		}

		else if ( password != password_confirm)
		{

			$('#create_error').show();	
			$('#create_error').text("password doesn't match");
		}


		else 
		{
			$.ajax({
			data : 
			{
				username : username,
				email : email,
			},
			type : 'POST',
			url : '/profile_validation'
		 })
		
		 .done(function(data) 
		 {
			if (data.error) 
			{
				$('#create_error').show();
				$('#create_error').text(data.error);
			}
			else 
			{
				$("#create_error").attr('class', 'alert alert-success');
				$('#create_error').show();
				$('#create_error').text(data.success);
				form[0].submit();
			}
		 });}
		
		
	});


}