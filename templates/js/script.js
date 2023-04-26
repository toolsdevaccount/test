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

// 指定したエレメント(input)が所属する行(tr)を取得
function detail(obj)
{
    return obj.parentElement.parentElement.parentElement ;
}

// 指定したエレメント(input)と同じ行にある単価を取得
function price(obj)
{
    return detail(obj).querySelectorAll(".DetailPrice")[0].value ;
}

// 指定したエレメント(input)と同じ行にある数量を取得
function overprice(obj)
{
    return detail(obj).querySelectorAll(".DetailOverPrice")[0].value ;
}

// 指定したエレメント(input)の横計(単価×数量)を再計算してから取得
function calc(obj)
{
    result = Number(price(obj)) + Number(overprice(obj));

    if(Number(overprice(obj))==0){
        detail(obj).querySelectorAll(".DetailOverPrice")[0].value = 0; 
    } 

    detail(obj).querySelectorAll(".DetailSellPrice")[0].value = result ;
    return result ;
}

function startitem(obj)
{		
    var item = document.getElementById('id_StartItemNumber').value ;
    result = item.toString().padStart( 4, '0');
    document.getElementById('id_StartItemNumber').value = result;
}

function enditem(obj)
{		
    var item = document.getElementById('id_EndItemNumber').value ;
    result = item.toString().padStart( 4, '0');
    document.getElementById('id_EndItemNumber').value = result;
}

$(function(){
    $('#form').submit(function() {  	 // フォームを送信する直前 tableの行数を取得
        var row = tblrow.rows.length -1; //表題分差引く
        $('[name=OrderingTableId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST
    });

    $('#list').addInputArea();
});
