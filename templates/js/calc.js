// 指定したエレメント(input)が所属する行(tr)を取得
function detail(obj)
{
    return obj.parentElement.parentElement.parentElement ;
}

// 指定したエレメント(input)と同じ行にある数量を取得
function volume(obj)
{
    return removeComma(detail(obj).querySelectorAll(".DetailVolume")[0].value);
}

// 指定したエレメント(input)と同じ行にある仕入単価を取得
function UnitPrice(obj)
{
    return removeComma(detail(obj).querySelectorAll(".DetailUnitPrice")[0].value);
}

// 指定したエレメント(input)と同じ行にある単価を取得
function price(obj)
{
    return removeComma(detail(obj).querySelectorAll(".DetailPrice")[0].value);
}

// 指定したエレメント(input)と同じ行にあるUP分単価を取得
function overprice(obj)
{
    return removeComma(detail(obj).querySelectorAll(".DetailOverPrice")[0].value);
}

function intcomma(obj)
{
    //桁区切りして配置（仕入単価）
    detailunitprice = Number(UnitPrice(obj)).toLocaleString();
    detail(obj).querySelectorAll(".DetailUnitPrice")[0].value = detailunitprice;
}

// 指定したエレメント(input)の横計を再計算してから取得
function calc(obj)
{
    //detailprice = Number(price(obj)).toLocaleString();
    //detailoverprice = Number(overprice(obj)).toLocaleString(); 

    //detail(obj).querySelectorAll(".DetailPrice")[0].value = detailprice;
    //detail(obj).querySelectorAll(".DetailOverPrice")[0].value = detailoverprice;

    result = Number(price(obj)) + Number(overprice(obj));

    if(Number(overprice(obj))==0){
        detail(obj).querySelectorAll(".DetailOverPrice")[0].value = 0; 
    } 

    detail(obj).querySelectorAll(".DetailSellPrice")[0].value = result;
    //detail(obj).querySelectorAll(".DetailSellPrice")[0].value = result.toLocaleString();
    return result ;
}

function removeComma(number) {
    var removed = number.replace(/,/g, '');
    return parseInt(removed, 10);
}

function order(obj)
{		
    var item = document.getElementById('id_OrderNumber').value ;
    result = item.toString().padStart( 7, '0');
    document.getElementById('id_OrderNumber').value = result;
}

function Productorder(obj)
{		
    var item = document.getElementById('id_ProductOrderOrderNumber').value ;
    result = item.toString().padStart( 7, '0');
    document.getElementById('id_ProductOrderOrderNumber').value = result;
}


const input = document.querySelector('input')

input.checked = true
