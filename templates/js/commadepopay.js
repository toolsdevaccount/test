    function removeComma(number) {
        var removed = number.replace(/,/g, '');
        return parseInt(removed, 10);
    }

    // 指定したエレメント(input)が所属する行(tr)を取得
    function detail(obj)
    {
        return obj.parentElement.parentElement.parentElement ;
    }

    // 指定したエレメント(input)と同じ行にある入金金額を取得
    function DepositMoney(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".DepositMoney")[0].value);
    }

    function comma(obj)
    {
        //桁区切りして配置（前回請求残）
        DepoMoney = Number(DepositMoney(obj)).toLocaleString();
        detail(obj).querySelectorAll(".DepositMoney")[0].value = DepoMoney;
    }

    $('#form').submit(function(){
        var DepoMoney = removeComma($(".DepositMoney").val());

        $(".DepositMoney").val(DepoMoney);
    });
