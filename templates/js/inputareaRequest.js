$(function(){
    $('#form').submit(function() {
        var DetailUnitPrice = removeComma($(".DetailUnitPrice").val());
        var DetailPrice = removeComma($(".DetailPrice").val());
        var DetailOverPrice = removeComma($(".DetailOverPrice").val());
        var DetailSellPrice = removeComma($(".DetailSellPrice").val());

        $(".DetailUnitPrice").val(DetailUnitPrice);
        $(".DetailPrice").val(DetailPrice);
        $(".DetailOverPrice").val(DetailOverPrice);
        $(".DetailSellPrice").val(DetailSellPrice);

        //フォームを送信する直前 tableの行数を取得
        var row = tblrow.rows.length -1;                    //表題分差引く
        $('[name=OrderingId-TOTAL_FORMS]').val(row);        // 行数を書き換えてPOST

        //明細行選択チェック
        var table = document.querySelector("table");
        var tr = table.querySelectorAll("tr");
        for(var i = 0; i < tr.length; i++) {
            var item = tr[i].style.backgroundColor;
            if(item=='rgb(238, 238, 255)'){
                return;
            }
        }
        alert("明細行が選択されていません.");
        return false;
    });

    $('#list').addInputArea({
        after_add: function () {
            var tbl = document.querySelector('#tblrow');
            var num = tbl.querySelectorAll('.ResultItemNumber').length;
            var item = tbl.querySelectorAll('.ResultItemNumber')[num -2].value;
                item = parseInt(item ,10);
            // 項番に前ゼロ付加
            var result = item.toString().padStart( 4, '0');
            tbl.querySelectorAll('.ResultItemNumber')[num -1].value = result;
            // OrderingDetailId取得し、追加行に設定する
            var id = document.getElementById('id_OrderingId-' + [num -2] + '-OrderingDetailId').value;
            document.getElementById('id_OrderingId-' + [num -1] + '-OrderingDetailId').value = id;
            // id値削除
            list = document.getElementById('id_OrderingId-' + [num -1] + '-id');
            list.remove();

            // 出荷日datepicker
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

            // 実績日datepicker
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
