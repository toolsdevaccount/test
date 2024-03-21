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
//window.onload = viewChange;
}

window.addEventListener('load', function() {
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

    var select = document.getElementById('id_OrderingTableId-0-DetailUnitDiv');
    select.options[1].selected = true;
})