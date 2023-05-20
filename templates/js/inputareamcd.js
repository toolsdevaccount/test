$(function(){
    $('#form').submit(function() {  	 // フォームを送信する直前 tableの行数を取得
        var row = tblrow.rows.length -1; //表題分差引く
        $('[name=McdDtid-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

        var row = tblrowcolor.rows.length -1; //表題分差引く
        $('[name=McdColorId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

        var row = tblrowsize.rows.length -1; //表題分差引く
        $('[name=McdSizeId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

        var row = tblrowfile.rows.length -1; //表題分差引く
        $('[name=McdFileId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

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
