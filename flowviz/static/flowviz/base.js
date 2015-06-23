var BaseModule = ( function (window, undefined) {
    
    function initialize() {
        $('.buttonlink').button();
        $('h1').addClass('ui-widget-header');
        $('h2').addClass('ui-widget-header');
    }
    
    return {
        initialize: initialize
    }
    
})(window)