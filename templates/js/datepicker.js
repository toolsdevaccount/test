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
// 指定納期
var SpecifyDeliveryDate = document.getElementById('id_SpecifyDeliveryDate');
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
var StainAnswerDeadline = document.getElementById('id_StainAnswerDeadline');
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
// 納期
var AnswerDeadline = document.getElementsByClassName('AnswerDeadline');
var fp = flatpickr(AnswerDeadline, {
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

// 依頼日(From)検索用
var orderdateFrom = document.getElementById('orderdateFrom');
var fp = flatpickr(orderdateFrom, {
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

// 依頼日(To)検索用
var orderdateTo = document.getElementById('orderdateTo');
var fp = flatpickr(orderdateTo, {
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
