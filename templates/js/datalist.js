// プルダウン(datalist)のlabel値をoutputに転記
document.addEventListener ('input', (event)=> {
    let
    e = event.target,
    list = e.list;

    if (list) {
    let
        option = list.querySelector (`option[value="${e.value}"]`),
        output = document.querySelector (`input[type=hidden][name="${e.name}"]`);
    if(option && output)
        output.value = option.label;
    }

}, true);

// 出力区分が通常と染色で入力項目を切り替える
function viewChange(){
    if(document.getElementById('id_OutputDiv')){
        id = document.getElementById('id_OutputDiv').value;                     //出力区分
        if(id == '1'){
            document.getElementById('id_StainPartNumber').readOnly = true;      //品番
            document.getElementById('id_StainMixRatio').readOnly = true;        //混率
            document.getElementById('id_StainShippingDate').readOnly = true;    //原糸出荷日
            document.getElementById('id_ApparelCode').readOnly = true;          //アパレルコード
            document.getElementById('id_StainShippingCode').readOnly = true;    //原糸メーカー
            document.getElementById('id_CustomeCode').readOnly = false;         //得意先コード
        }else if(id == '2'){
            document.getElementById('id_StainPartNumber').readOnly = false;
            document.getElementById('id_StainMixRatio').readOnly = false;
            document.getElementById('id_StainShippingDate').readOnly = false;
            document.getElementById('id_ApparelCode').readOnly = false;
            document.getElementById('id_StainShippingCode').readOnly = false;
            document.getElementById('id_CustomeCode').readOnly = false;
        }
        else if(id == '3'){
            document.getElementById('id_StainPartNumber').readOnly = false;
            document.getElementById('id_StainMixRatio').readOnly = false;
            document.getElementById('id_StainShippingDate').readOnly = false;
            document.getElementById('id_CustomeCode').readOnly = true;
            document.getElementById('id_ApparelCode').readOnly = false;
            document.getElementById('id_StainShippingCode').readOnly = false;
        }
        else if(id == '4'){
            document.getElementById('id_StainPartNumber').readOnly = true;
            document.getElementById('id_StainMixRatio').readOnly = true;
            document.getElementById('id_StainShippingDate').readOnly = true;
            document.getElementById('id_ApparelCode').readOnly = true;
            document.getElementById('id_StainShippingCode').readOnly = true;
            document.getElementById('id_CustomeCode').readOnly = false;
        }
    }

window.onload = viewChange;
}
// 手配先と仕入先を連動する（手配先を選択したら仕入先にも同様のコードをセットする
$('input[id=id_DestinationCode]').on('change', function () {
    // 手配先
    DestVal = $(this).val();
    Destlbl = $("#Destination option[value='" + $(this).val() + "']").prop('label');
    // 仕入先へ
    $("#id_SupplierCode").val(DestVal);
    $('input:hidden[id="id_SupplierCode"]').val(Destlbl);
});

// 出荷先と得意先を連動する（出荷先を選択したら得意先にも同様のコードをセットする
$('input[id=id_ShippingCode]').on('change', function () {
    id = document.getElementById('id_OutputDiv').value;                     //出力区分
    if(id != '3'){
        // 出荷先
        ShipVal = $(this).val();
        Shiplbl = $("#Shipping option[value='" + $(this).val() + "']").prop('label');
        // 得意先へ
        $("#id_CustomeCode").val(ShipVal);
        $('input:hidden[id="id_CustomeCode"]').val(Shiplbl);
    }
});

// 製品受発注入力の手配先と仕入先を連動する（手配先を選択したら仕入先にも同様のコードをセットする
$('input[id=id_ProductOrderDestinationCode]').on('change', function () {
    // 手配先
    DestVal = $(this).val();
    Destlbl = $("#ProductOrderDestination option[value='" + $(this).val() + "']").prop('label');
    // 仕入先へ
    $("#id_ProductOrderSupplierCode").val(DestVal);
    $('input:hidden[id="id_ProductOrderSupplierCode"]').val(Destlbl);
});

// 製品受発注入力の出荷先と得意先を連動する（出荷先を選択したら得意先にも同様のコードをセットする
$('input[id=id_ProductOrderShippingCode]').on('change', function () {
    // 出荷先
    ShipVal = $(this).val();
    Shiplbl = $("#ProductOrderShipping option[value='" + $(this).val() + "']").prop('label');
    // 得意先へ
    $("#id_ProductOrderCustomeCode").val(ShipVal);
    $('input:hidden[id="id_ProductOrderCustomeCode"]').val(Shiplbl);
});