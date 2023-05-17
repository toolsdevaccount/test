// 発注日
var ProductOrderOrderingDate = document.getElementById('id_ProductOrderOrderingDate');
var fp = flatpickr(ProductOrderOrderingDate, {
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
// 納期
var ProductOrderDeliveryDate = document.getElementById('id_ProductOrderDeliveryDate');
var fp = flatpickr(ProductOrderDeliveryDate, {
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

