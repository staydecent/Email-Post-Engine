jQuery(document).ready(function($) {
    /*
        Swap value for input
    */
    swap_value = [];
    $('input').each(function(i) {
        swap_value[i] = $(this).val();
        $(this).focus(function() {
            if ($(this).val() == swap_value[i]) {
                $(this).val("");
            }
        }).blur(function() {
            if ($.trim($(this).val()) == "") { 
                $(this).val(swap_value[i]);
            }
        });
    });
});