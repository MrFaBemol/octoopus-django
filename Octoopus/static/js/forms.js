$(document).ready(function (){


    $('select.dropdown').each(function() {

        let dropdown = $('<div />').addClass('dropdown selectDropdown');

        $(this).wrap(dropdown);

        let label = $('<span />').text($(this).attr('placeholder')).insertAfter($(this));
        let list = $('<ul />');

        $(this).find('option').each(function() {
            list.append($('<li />').append($('<a />').text($(this).text())));
        });

        list.insertAfter($(this));

        if($(this).find('option:selected').length) {
            label.text($(this).find('option:selected').text());
            list.find('li:contains(' + $(this).find('option:selected').text() + ')').addClass('active');
            $(this).parent().addClass('filled');
        }

    });

    $(document).on('click touch', '.selectDropdown ul li a', function(e) {
        e.preventDefault();
        let dropdown = $(this).parent().parent().parent();
        let active = $(this).parent().hasClass('active');
        let label = active ? dropdown.find('select').attr('placeholder') : $(this).text();

        dropdown.find('option').prop('selected', false);
        dropdown.find('ul li').removeClass('active');

        dropdown.toggleClass('filled', !active);
        dropdown.children('span').text(label);

        if(!active) {
            dropdown.find('option:contains(' + $(this).text() + ')').prop('selected', true);
            $(this).parent().addClass('active');
        }

        dropdown.removeClass('open');
        dropdown.find('select').trigger('change');
    });

    $('.dropdown > span').on('click touch', function(e) {
        let self = $(this).parent();
        self.toggleClass('open');
    });

    $(document).on('click touch', function(e) {
        let dropdown = $('.dropdown');
        if(dropdown !== e.target && !dropdown.has(e.target).length) {
            dropdown.removeClass('open');
        }
    });



    // For the switch
    $('.switch').each(function(){
        let input = $(this).find('input');
        input.val('off');
        input.prev().addClass('active');
        input.on('change', function(e) {
            if ($(this).is(':checked')){
                $(this).next().addClass('active');
                $(this).prev().removeClass('active');
                $(this).val('on');
            } else {
                $(this).prev().addClass('active');
                $(this).next().removeClass('active');
                $(this).val('off');
            }
        });
    });



});

