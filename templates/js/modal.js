var btn = document.getElementById('modalOpen');
var cls = document.getElementById('modalClose');
var dlt = document.getElementById('delete');
var modal = document.getElementsByClassName('fds-uxhub-preview');

btn.addEventListener('click', function() {
    for(i=0;i<modal.length;i++){
        modal[i].style.opacity = '1';
        modal[i].style.visibility = 'visible';
    }
})
dlt.addEventListener('click', function() {
    document.delform.submit();
})
cls.addEventListener('click', function() {
    for(i=0;i<modal.length;i++){
        modal[i].style.opacity = '0';
        modal[i].style.visibility = 'hidden';
    }
})
