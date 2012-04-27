/* @projectDescription jQuery Serialize Anything - Serialize anything (and not just forms!)
 * @author Bramus! (Bram Van Damme)
 * @version 1.0
 * @website: http://www.bram.us/
 * @license : BSD
*/

(function($) {

    $.fn.serializeAnything = function() {

        var toReturn    = [];
        var els         = $(this).find(':input').get();

        $.each(els, function() {
            if (this.name && !this.disabled && (this.checked || /select|textarea/i.test(this.nodeName) || /text|hidden|password/i.test(this.type))) {
                var val = $(this).val();
                toReturn.push( encodeURIComponent(this.name) + "=" + encodeURIComponent( val ) );
            }
        });

        return toReturn.join("&").replace(/%20/g, "+");

    }

})(django.jQuery);
//-------------------------- end serialize enything --------------------------//

$(function() {
    //Drag and Drop actions
	$( ".sidebar_container" ).sortable({
	        items: " .sidebar_item:not(.ui-state-disabled)",
            stop: function(event, ui) {
                reorder_widgets();
            }
    });

	//Menu Hover
    $('.sidebar_container .sidebar_item').hover(
        function(){
            $(this).addClass('hovered');
            },
        function(){
            $(this).removeClass('hovered');
            }
        );

    //load widgets
    load_wigets();
});

function load_wigets(){
    $('.sidebar_loading').show();
    var params = {
    'csrfmiddlewaretoken': window.csrf_token,
    'sidebar_id': window.sidebar_id
    }
    $('.sidebar_container .sidebars').load(window.sidebar, params ,function(){
        $('.sidebar_loading').hide();
    });
}

function add_widget(widget_id, sidebar_id){
    //Add widget to sidebar
    $('.sidebar_loading').show();
    $.post(window.add_url, {'widget': widget_id, 'sidebar': sidebar_id, 'csrfmiddlewaretoken': window.csrf_token}, function(response){
        $('.sidebar_loading').hide();
        if(response.status == '1'){
            load_wigets();
        }
    },'json');
}

function update_widget(widget_id){
    $('.widget_loading_'+widget_id).show();
    reset_errors();
    var formdata = django.jQuery('.editor_'+widget_id).serializeAnything();
    $.post(window.update_url, formdata, function(response){
        $('.widget_loading_'+widget_id).hide();
        if(response.status == 'success'){
            $('.widget_'+widget_id+' .title').text(response.title);
        }else{
            set_errors(response.error_fields);
        }
    },'json');
}


function reorder_widgets(){
    $('.sidebar_loading').show();
    var widgets = new Array();
    $('.sidebar_container .sidebar_item').each(function(){
        var id = $(this).attr('rel');
        widgets.push(id);
    });

    //If menu empty, than don't reorder.
    if(widgets.length > 0){
        var widgets_str = widgets.join(',');
        data = {
            'csrfmiddlewaretoken': window.csrf_token,
            'order' : widgets_str
        }
        $.post(window.reorder_url, data, function(response){
            $('.sidebar_loading').hide();
        },'json');
    }else{
        $('.sidebar_loading').hide();
    }

}

function delete_widget(widget_id){
    $('.sidebar_loading').show();
    $.post(window.delete_url, {'csrfmiddlewaretoken': window.csrf_token, 'widget_id': widget_id}, function(response){
        $('.sidebar_loading').hide();
        if(response.status == 'success'){
            $('.sidebar_item.widget_'+widget_id).css('background','#cc3434').animate({opacity:0}, 500, function(){
                $(this).remove();
            });
        }
    }, 'json');
}

function toggle_widget_editor(widget_id){
    $('.editor_'+widget_id).slideToggle('fast');
}

function set_errors(fields){
    for(i in fields){
        field = fields[i];
        $('.sidebar_item #id_'+field).addClass('error');
    }
}

function reset_errors(){
    $('.sidebar_item input, .sidebar_item select').removeClass('error');
}

