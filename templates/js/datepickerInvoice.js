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

// 一括請求書年月日FROM用
var InvoiceDate_From = document.getElementById('id_InvoiceDate_From');
var fp = flatpickr(InvoiceDate_From, {
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

// 一括請求書年月日To用
var InvoiceDate_To = document.getElementById('id_InvoiceDate_To');
var fp = flatpickr(InvoiceDate_To, {
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