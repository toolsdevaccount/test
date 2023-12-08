$(function(){
    $('#form').submit(function() {  	 // フォームを送信する直前 tableの行数を取得
        var row = tblrow.rows.length -1; //表題分差引く
        $('[name=OrderingId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST
    });

    $('#list').addInputArea({
        after_add: function () {
            var tbl = document.querySelector('#tblrow');
            var num = tbl.querySelectorAll('.ResultItemNumber').length;
            var item = tbl.querySelectorAll('.ResultItemNumber')[num -2].value;
                item = parseInt(item ,10) +1;
            var result = item.toString().padStart( 4, '0');
            tbl.querySelectorAll('.ResultItemNumber')[num -1].value = result;

            $('#detail').append(
				'<input type="hidden" data-id-format="id_OrderingId-%d-DELETE" data-name-format="OrderingId-%d-DELETE" name="OrderingId-' + [num -1] + '-DELETE" id="id_OrderingId-' + [num -1] + '-DELETE">' +
				'<input type="hidden" data-id-format="id_OrderingId-%d-OrderingDetailId" data-name-format="OrderingId-%d-OrderingDetailId" name="OrderingId-' + [num -1] + '-OrderingDetailId" id="id_OrderingId-' + [num -1] + '-OrderingDetailId" value="">'
			);

            var id = document.getElementById('id_OrderingId-' + [num -2] + '-OrderingDetailId').value;
            document.getElementById('id_OrderingId-' + [num -1] + '-OrderingDetailId').value = id;

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
        }
    });
});

$('.DeliveryManageDiv').click(function() {
    if($(".DeliveryManageDiv").prop('checked')){
        $(".DeliveryManageDiv").val(1);
    } else {
        $(".DeliveryManageDiv").val(0);
    }           
});

$('.PrintDiv').click(function() {
    if($(".PrintDiv").prop('checked')){
        $(".PrintDiv").val(1);
    } else {
        $(".PrintDiv").val(0);
    }           
});