$(document).ready(function (){


    // Allow the double input to get a focus color when selecting one of the two input
    $('.label-input-double').each(function(){
        let parent = $(this);
        parent.find('div.input-field').each(function (){
            $(this).focusin(function (){
                $(this).parent().addClass('active');
            });
            $(this).focusout(function (){
                $(this).parent().removeClass('active');
            });
        });
    });



});

