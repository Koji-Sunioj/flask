function search_check()

{   
	

	function normalize_modal() {
		$('#myModal').find('input[name=thread_id]').remove();
		$('#edit_form').attr("id","new_post");
		$('#cancel_edit').attr("id","cancel_post");
		$('#myModal').find('input:text').val('');
		$('#myModal').find('textarea').val('');
		$('#myModal').modal('hide');
	}
	
	$(function() {
		if ($('#message_success').length == 1)
		{ 
			
			
			$('.data_table:nth-of-type(1)').addClass("highlight");
			setTimeout(function () {
				$('#YourElement').removeClass('highlight');
		  }, 2000);
		
		} 
	});
	
 $(".dropdown-item[name='edit']").on('click',function(event)
 
 {
	event.preventDefault();
	var thread_id = $(this).parents().eq(5).find('input[name=thread_id]').val();
	var title = $(this).parents().eq(5).find('td:nth-of-type(1)').text();
	var post = $(this).parents().eq(5).find('input[name=post]').val();

	$('#myModal').find('h4').text('edit your damn post')
	$('#myModal').find('input:text').val(title);
	$('#myModal').find('textarea').val(post);

	$('#new_post').attr("id","edit_form");
	$('#cancel_post').attr("id","cancel_edit");

	$('#myModal').append('<input type="hidden" value='+thread_id+' name="thread_id">')

	$('#myModal').modal('show');
	$('#modal_error').hide();


});
	

$(document).on('click','#edit_form', function(event) {
	event.preventDefault();
	var edited_title = $('#myModal').find('input:text').val();
	var edited_post = $('#myModal').find('textarea').val();
	var thread_id = $('#myModal').find('input:hidden').val();
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
		normalize_modal();

	 }
	 
	 )
	
});



$(document).on('click','#cancel_edit', function(event) {
	event.preventDefault();
	normalize_modal();
});


	$( document ).on('click',function(event) {

		if (event.target.className !== 'btn btn-link dropdown-toggle')
		{
			$(".dropdown-edit_form").hide();
		}

	});
	
	$('.btn.btn-link.dropdown-toggle').on('click',function() {
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






$('#show_me').on('click',function() {
	$('#myModal').modal('show');
	$('#modal_error').hide();
})


$(document).on('click','#cancel_post',function(event)
	{ 
		event.preventDefault();
		$('#myModal').find('input:text').val('');
		$('#myModal').find('textarea').val('');
		$('#myModal').modal('hide');
		
	});


$(document).on('submit','#new_post', function(event) {
	event.preventDefault();
	alert($(this).attr('name'));
	var form = $(this);
	var new_title = $('#myModal').find('input:text').val().trim();
	var new_post = $('#myModal').find('textarea').val().trim();

	if (!new_title || !new_post)
	  	{ 
			$('#modal_error').show();
			$('#modal_error').text('fill in the fields bro');
			
		  //alert('fill in both fields bro');
		}
	else 
		{
		 form[0].submit();
		  }

});
	
	
	$('form[name=search]').on('submit', function(event) {

	event.preventDefault();
	var form = $(this);
	query = $(this).find('input[name=query]').val().trim();
	if (!query ) 
	{ 
		$('#query_error').show();
		$('#query_error').text('empty search field brah');
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
		{
			$('#query_error').show();
			$('#query_error').text(data.error);
		}
		else 
		{
			form[0].submit();
			
		}
	 });}
});

}



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