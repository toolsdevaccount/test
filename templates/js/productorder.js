$(function(){
    $('#form').submit(function() {  	 // フォームを送信する直前 tableの行数を取得
        var row = tblrowclsz.rows.length -1; //表題分差引く
        $('[name=PodDetailId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST
    });
});
