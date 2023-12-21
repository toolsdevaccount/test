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
    function PaymentMoney(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".PaymentMoney")[0].value);
    }

    function comma(obj)
    {
        //桁区切りして配置
        PayMoney = Number(PaymentMoney(obj)).toLocaleString();
        detail(obj).querySelectorAll(".PaymentMoney")[0].value = PayMoney;
    }

    $('#form').submit(function(){
        var PayMoney = removeComma($(".PaymentMoney").val());

        $(".PaymentMoney").val(PayMoney);
    });
