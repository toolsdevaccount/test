// DailyUpdate日次更新日付
var DailyUpdateDate = document.getElementsByClassName('DailyUpdateDate');
var fp = flatpickr(DailyUpdateDate, {
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

//今日の日付を表示
window.onload = function () {
    //今日の日付を表示
    var date = new Date()
    var year = date.getFullYear()
    var month = date.getMonth() + 1
    var day = date.getDate()
    
    var toTwoDigits = function (num, digit) {
        num += ''
        if (num.length < digit) {
        num = '0' + num
        }
        return num
    }
    
    var yyyy = toTwoDigits(year, 4)
    var mm = toTwoDigits(month, 2)
    var dd = toTwoDigits(day, 2)
    var ymd = yyyy + "-" + mm + "-" + dd;

    if (document.getElementById("id_DailyUpdateDate").value==""){
        document.getElementById("id_DailyUpdateDate").value = ymd;
    }

}
