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
    // submit前にカンマをはずす
    var DetailUnitPrice = removeComma($(".DetailUnitPrice").val());
    var DetailPrice = removeComma($(".DetailPrice").val());
    var DetailOverPrice = removeComma($(".DetailOverPrice").val());
    var DetailSellPrice = removeComma($(".DetailSellPrice").val());

    $(".DetailUnitPrice").val(DetailUnitPrice);
    $(".DetailPrice").val(DetailPrice);
    $(".DetailOverPrice").val(DetailOverPrice);
    $(".DetailSellPrice").val(DetailSellPrice);

    document.delform.submit();
})
cls.addEventListener('click', function() {
    for(i=0;i<modal.length;i++){
        modal[i].style.opacity = '0';
        modal[i].style.visibility = 'hidden';
    }
})

function removeComma(number) {
    var removed = number.replace(/,/g, '');
    return parseInt(removed, 10);
}

