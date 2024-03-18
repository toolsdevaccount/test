// 
var PaymentDate = document.getElementById('id_PaymentDate');
var fp = flatpickr(PaymentDate, {
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
