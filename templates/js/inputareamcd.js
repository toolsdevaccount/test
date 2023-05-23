$(function(){
    $('#form').submit(function() {  	 // フォームを送信する直前 tableの行数を取得
        var row = tblrow.rows.length -1; //表題分差引く
        $('[name=McdDtid-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

        var row = tblrowcolor.rows.length -1; //表題分差引く
        $('[name=McdColorId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

        var row = tblrowsize.rows.length -1; //表題分差引く
        $('[name=McdSizeId-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

        var row = tblrowfile.rows.length -1; //表題分差引く
        $('[name=McdDtuploadid-TOTAL_FORMS]').val(row); // 行数を書き換えてPOST

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

      //ホバーイベント発火
      $("#link:not(:animated)").hover(function(){
        $('#tip').show(); //マウスオーバーで表示
        }, function() {
          $('#tip').hide(); //マウスアウトで非表示   

      //ここからマウスムーブイベント
      }).mousemove(function(e) {
        var mousex = e.pageX + 20; //マウスの位置（X座標）を取得
        var mousey = e.pageY + 20; //マウスの位置（Y座標）を取得
        var tipWidth = $('#tip').width(); //ツールチップの幅を取得
        var tipHeight = $('#tip').height(); //ツールチップの高さを取得

        var tipVisX = $(window).width() - (mousex + tipWidth);
        var tipVisY = $(window).height() - (mousey + tipHeight);

        if ( tipVisX < 20 ) { //画面幅を超えた場合はX座標を調節
          mousex = e.pageX - tipWidth - 20;
        } if ( tipVisY < 20 ) { //画面高さを超えた場合はY座標を調節
          mousey = e.pageY - tipHeight - 20;
        }
          $('#tip').css({  top: mousey, left: mousex });
      });
});

$('.DeliveryManageDiv').click(function() {
    if($(".DeliveryManageDiv").prop('checked')){
        $(".DeliveryManageDiv").val(1);
    } else {
        $(".DeliveryManageDiv").val(0);
    }           
});
