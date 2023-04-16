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

// 依頼日
//var OrderingDate = document.getElementById('id_OrderingDate');
//var fp = flatpickr(OrderingDate, {
//    'locale': 'ja',
//    // onCloseは入力フォームが閉じられた時に発火する
//    onClose: (selectedDates, dateStr, instance) => {
//        if (selectedDates.length === 1) {
//            // プロパティにユーザーが選択した日付を代入
//            this.dateProps = selectedDates[0];
//        }
//    }
//});

// 原糸出荷日
//var StainShippingDate = document.getElementById('id_StainShippingDate');
//var fp = flatpickr(StainShippingDate, {
//    'locale': 'ja',
    // onCloseは入力フォームが閉じられた時に発火する
//    onClose: (selectedDates, dateStr, instance) => {
//        if (selectedDates.length === 1) {
            // プロパティにユーザーが選択した日付を代入
//            this.dateProps = selectedDates[0];
//        }
//    }
//});

// 指定納期

//var SpecifyDeliveryDate = document.getElementById('id_SpecifyDeliveryDate');
//var fp = flatpickr(SpecifyDeliveryDate, {
//    'locale': 'ja',
    // onCloseは入力フォームが閉じられた時に発火する
//    onClose: (selectedDates, dateStr, instance) => {
//        if (selectedDates.length === 1) {
            // プロパティにユーザーが選択した日付を代入
//            this.dateProps = selectedDates[0];
//        }
//    }
//});

// 回答納期
//var StainAnswerDeadline = document.getElementById('id_StainAnswerDeadline');
//var fp = flatpickr(StainAnswerDeadline, {
//    'locale': 'ja',
    // onCloseは入力フォームが閉じられた時に発火する
//    onClose: (selectedDates, dateStr, instance) => {
//        if (selectedDates.length === 1) {
            // プロパティにユーザーが選択した日付を代入
//            this.dateProps = selectedDates[0];
//        }
//    }
//});
