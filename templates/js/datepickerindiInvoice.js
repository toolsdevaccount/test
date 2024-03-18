// 納期(From)検索用
var ShippingDateFrom = document.getElementById('ShippingDateFrom');
var fp = flatpickr(ShippingDateFrom, {
    'locale': 'ja',
    allowInput: true,
    // onCloseは入力フォームが閉じられた時に発火する
    onClose: (selectedDates, dateStr, instance) => {
        if (selectedDates.length === 1) {
            // プロパティにユーザーが選択した日付を代入
            this.dateProps = selectedDates[0];
        }
    }
});

// 個別請求書発行日用
var Dateissue = document.getElementById('id_date_issue');
var fp = flatpickr(Dateissue, {
    'locale': 'ja',
    allowInput: true,
    // onCloseは入力フォームが閉じられた時に発火する
    onClose: (selectedDates, dateStr, instance) => {
        if (selectedDates.length === 1) {
            // プロパティにユーザーが選択した日付を代入
            this.dateProps = selectedDates[0];
        }
    }
});

// 納期(To)検索用
//var ShippingDateTo = document.getElementById('ShippingDateTo');
//var fp = flatpickr(ShippingDateTo, {
//    'locale': 'ja',
//    allowInput: true,
//    // onCloseは入力フォームが閉じられた時に発火する
//    onClose: (selectedDates, dateStr, instance) => {
//        if (selectedDates.length === 1) {
//            // プロパティにユーザーが選択した日付を代入
//            this.dateProps = selectedDates[0];
//        }
//    }
//});