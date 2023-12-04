// 依頼日
var OrderingDate = document.getElementById('id_OrderingDate');
var fp = flatpickr(OrderingDate, {
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
// 原糸出荷日
var StainShippingDate = document.getElementById('id_StainShippingDate');
var fp = flatpickr(StainShippingDate, {
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
// 希望納期
var SpecifyDeliveryDate = document.getElementsByClassName('SpecifyDeliveryDate');
var fp = flatpickr(SpecifyDeliveryDate, {
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
// 回答納期
var StainAnswerDeadline = document.getElementsByClassName('StainAnswerDeadline');
var fp = flatpickr(StainAnswerDeadline, {
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
	//
	var ShippingDate = document.getElementsByClassName('ShippingDate');
	var fp = flatpickr(ShippingDate, {
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

	// 
	var ResultDate = document.getElementsByClassName('ResultDate');
	var fp = flatpickr(ResultDate, {
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
