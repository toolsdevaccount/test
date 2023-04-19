function calc() {
    const Price = isNumber(document.getElementById('id_OrderingTableId-0-DetailPrice').value);
    const OverPrice = isNumber(document.getElementById('id_OrderingTableId-0-DetailOverPrice').value);

    const lean_value = parseInt(Price,10) + parseInt(OverPrice,10);

    var resultForm = document.getElementById('id_OrderingTableId-0-DetailSellPrice');

    resultForm.value = lean_value;
}

function isNumber(numVal){
    var pattern = /^[-]?([1-9]\d*|0)(\.\d+)?$/;
    var result = pattern.test(numVal);
    if(result==false){
        numVal = 0;
    }
    return numVal;
}