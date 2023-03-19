$(document).ready(function () {
    $('table').accordion({
        header: '.category',
        collapsible: true,
        activate: function(e, ui) {
            localStorage.setItem('accordion-active', $(this).accordion( "option", "active" ));
        },
        active: parseInt(localStorage.getItem('accordion-active'))
    });
   }); 