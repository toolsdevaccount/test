$(function(){
    $('#form').submit(function() {  	 // フォームを送信する直前 tableの行数を取得
        var row = tblrow.rows.length -1; //表題分差引く
        $('[name=OrderingTableId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST
    });

    //$('#list').addInputArea();

    $('#list').addInputArea({
        after_add: function () {
            var tbl = document.querySelector('#tblrow');
            var num = tbl.querySelectorAll('.DetailItemNumber').length;
            var item = tbl.querySelectorAll('.DetailItemNumber')[num -2].value;
                item = parseInt(item ,10) +1;
            var result = item.toString().padStart( 4, '0');

            tbl.querySelectorAll('.DetailItemNumber')[num -1].value = result;

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
