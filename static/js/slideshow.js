jQuery(document).ready(function($) {
    // photo slideshow
    var pID = 1;
    var p = $('#slideshow .photo');
    var c = p.size();

    p.css({opacity: 0.0,zIndex: '8'});
    var slide_init = function() { $('#photo-'+pID).animate({opacity: 1.0,zIndex: '10'}, 250, function() { $('#slideshow').css({height: $('#photo-'+pID).height()},500); }); }
    $('#photo-count').html('('+pID+' of '+c+')');
    if ( $('#slideshow').height() == 0 ) { slide_init(); };

    $('#next-photo,a .photo').click(function() {
        p.css({zIndex: '8'});
        if (pID < c) { 
            ++pID;
            $('#photo-'+pID).css({opacity: 0.0,zIndex: '10'}).animate({opacity: 1.0}, 500, function() {
                $('#photo-'+(pID-1)).css({opacity: 0.0,zIndex: '9'});
            });
        }
        else {
            pID = 1;
            $('#photo-'+pID).css({opacity: 0.0,zIndex: '10'}).animate({opacity: 1.0}, 500, function() {
                $('#photo-'+c).css({opacity: 0.0,zIndex: '9'});
            });
        }
        
        $('#slideshow').css({height: $('#photo-'+pID).height()});
        $('#photo-count').html('('+pID+' of '+c+')');
        return false;
    });
    $('#prev-photo').click(function() {
        p.css({zIndex: '8'});
        if (pID > 1) {  
            --pID;
            $('#photo-'+pID).css({opacity: 0.0,zIndex: '10'}).animate({opacity: 1.0}, 500, function() {
                $('#photo-'+(pID+1)).css({opacity: 0.0,zIndex: '9'});
            });
        }
        else {
            pID = c;
            $('#photo-'+pID).css({opacity: 0.0,zIndex: '10'}).animate({opacity: 1.0}, 500, function() {
                $('#photo-1').css({opacity: 0.0,zIndex: '9'});
            });
        }
        
        $('#slideshow').css({height: $('#photo-'+pID).height()});
        $('#photo-count').html('('+pID+' of '+c+')');
        return false;
    });
});