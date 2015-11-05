$(document).ready(function(){
	
	$('#project-form-paid-group').hide();

    $('#add-2').hide();
    $('#add-3').hide();
    $('#add-4').hide();

    $('#faculty-optional-1').hide();
    $('#faculty-optional-2').hide();
    $('#faculty-optional-3').hide();
    $('#faculty-optional-4').hide();

    $('#project-form-summer').change(function(){
	
        if($('#project-form-summer').val()=="YES" )
        {
            $('#project-form-paid-group').show();
        }
        else {
            $('#project-form-paid-group').hide();
    }});
    $('#add-1').click(function(){
        $('#add-1').hide();
        $('#faculty-optional-1').show();
        $('#add-2').show();
    });
	$('#add-2').click(function(){
       $('#add-1').hide();
       $('#add-2').hide();
       $('#faculty-optional-2').show();
       $('#add-3').show();  
    });
    $('#add-3').click(function(){
       $('#add-1').hide();
       $('#add-2').hide();
       $('#add-3').hide(); 
       $('#add-4').show();
       $('#faculty-optional-3').show();
    });
    $('#add-4').click(function(){
        $('#add-1').hide();
       $('#add-2').hide();
       $('#add-3').hide();
       $('#add-4').hide();
       $('#faculty-optional-4').show();
    });
});
