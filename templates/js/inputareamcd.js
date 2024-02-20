$(function(){
    $('#form').submit(function() {  	 // フォームを送信する直前 tableの行数を取得
        //仕入単価のカンマを取り除く
        $(".McdUnitPrice").each(function() {
            $(this).val(removeComma($(this).val()));
        });
        //販売単価のカンマを取り除く
        $(".McdSellPrice").each(function() {
            $(this).val(removeComma($(this).val()));
        });
        //加工賃のカンマを取り除く
        $(".McdProcessfee").each(function() {
            $(this).val(removeComma($(this).val()));
        });
        //明細の単価のカンマを取り除く
        $(".McdDtlPrice").each(function() {
            $(this).val(removeComma($(this).val()));
        });
	
		var row = tblrow.rows.length -1; //表題分差引く
        $('[name=McdDtid-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

        var row = tblrowcolor.rows.length -1; //表題分差引く
        $('[name=McdColorId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

        var row = tblrowsize.rows.length -1; //表題分差引く
        $('[name=McdSizeId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

        var row = tblrowfile.rows.length -1; //表題分差引く
        $('[name=McdDtuploadid-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

        var row = tblrowclsz.rows.length -1; //表題分差引く
        $('[name=PodDetailId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST
    });

    $('#list').addInputArea();

    $('#listcolor').addInputArea({
        area_var: '.colorarea',
        btn_add: '.addcolor',
        btn_del: '.delcolor'
      });
    
      $('#listsize').addInputArea({
        area_var: '.sizearea',
        btn_add: '.addsize',
        btn_del: '.delsize'
      });

      $('#listfile').addInputArea({
        area_var: '.filearea',
        btn_add: '.addfile',
        btn_del: '.delfile'
      });
});

$('.DeliveryManageDiv').click(function() {
    if($(".DeliveryManageDiv").prop('checked')){
        $(".DeliveryManageDiv").val(1);
    } else {
        $(".DeliveryManageDiv").val(0);
    }           
});
