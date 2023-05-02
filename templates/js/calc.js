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

function order(obj)
{		
    var item = document.getElementById('id_OrderNumber').value ;
    result = item.toString().padStart( 7, '0');
    document.getElementById('id_OrderNumber').value = result;
}

const input = document.querySelector('input')

input.checked = true
