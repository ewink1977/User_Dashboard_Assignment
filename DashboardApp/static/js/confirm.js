$(document).ready(function() {
    $("#confirm-text").dialog({
        resizable: false,
        autoOpen: false,
        show: false,
        height: "auto",
        width: 400,
        modal: true,
        classes: {
            "ui-dialog": "modal-content",
            "ui-dialog-titlebar": "modal-header",
            "ui-dialog-title": "modal-title",
            "ui-dialog-titlebar-close": "close",
            "ui-dialog-content": "modal-body",
            "ui-dialog-buttonpane": "modal-footer"
        },
    });

$(".deletion").click(function(e) {
    e.preventDefault();
    var theHREF = $(this).attr("href")

    $("#confirm-text").dialog('option', 'buttons', {
        "Confirm User Deletion": function() {
                window.location.href = theHREF;
            },
            Cancel: function() {
                $( this ).dialog("close");
            }
    });

        $("#confirm-text").dialog("open");
    });
});