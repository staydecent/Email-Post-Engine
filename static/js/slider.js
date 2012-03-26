jQuery(document).ready(function($) {
    /*
        Animated content slide
    */
    var slider_link = $('article header h2 a').attr('href');
    $('article').hover(function() {
        $('#slider').fadeIn(250);
        $('section#excerpt').fadeIn(200);
        $(this).css({cursor:'pointer'});
    }, function() {
        $('#slider').fadeOut(50);
        $('section#excerpt').fadeOut(200);
        $(this).css({cursor:'default'});
    });
    $('article').click(function () { document.location = slider_link; });
    var s_height = $('article').height();
    $('#slider').css({top:(s_height/2)-20+'px'});
    $('#excerpt').css({top:(s_height-40)+'px'});
    /*
        Title, excerpt switch
    */
    $('section#latest_articles ol li').hover(function() {

        $(this).children('a').children('p').hide();
        $(this).children('a').children('h2').fadeIn(200);
    }, function() {
        $(this).children('a').children('h2').fadeOut(50);
        $(this).children('a').children('p').fadeIn(200);
    });
});