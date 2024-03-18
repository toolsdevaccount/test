$('form').on('keydown', 'input, button, select', function(e) {
    if (e.keyCode == 13) {
        if ($(this).attr("type") == 'submit') return;

        var form = $(this).closest('form');
        var focusable = form.find('input, button[type="submit"], select, textarea')
            .not('[readonly]').filter(':visible');

        if (e.shiftKey) {
            focusable.eq(focusable.index(this) - 1).focus();
        } else {
            var next = focusable.eq(focusable.index(this) + 1);
            if (next.length) {
                next.focus();
            } else {
                focusable.eq(0).focus();
            }
        }

        e.preventDefault();
    }
});

function checkForm($this)
{
    var str=$this.value;
    while(str.match(/[^A-Z^a-z\d\-]/))
    {
        str=str.replace(/[^A-Z^a-z\d\-]/,"");
    }
    $this.value=str;
}