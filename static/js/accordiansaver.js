<<<<<<< HEAD
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
=======
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

function restoreAccordionPanel(storageKey, accordionId) {
    var activeItem = localStorage.getItem(storageKey);
    if (activeItem) {
        //remove default collapse settings
        $(accordionId + " .panel-collapse").removeClass('in');

        //show the account_last visible group
        $("#" + activeItem).addClass("in");
    }
}

function restoreActiveTab(storageKey, tabId) {
    var activeItem = localStorage.getItem(storageKey);
    if (activeItem) {
        $(tabId + ' a[href="' + activeItem + '"]').tab('show');
    }
}

function saveActiveAccordionPanel(storageKey, e) {
    localStorage.setItem(storageKey, e.target.id);
}

function saveActiveTab(storageKey, e) {
    localStorage.setItem(storageKey, $(e.target).attr('href'));
}
>>>>>>> 76ba665 (20232203)
