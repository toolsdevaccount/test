    function removeComma(number) {
        var removed = number.replace(/,/g, '');
        return parseInt(removed, 10);
    }

    // 指定したエレメント(input)が所属する行(tr)を取得
    function detail(obj)
    {
        return obj.parentElement.parentElement.parentElement ;
    }

    // 指定したエレメント(input)と同じ行にある前回請求残を取得
    function LastClaimBalance(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".LastClaimBalance")[0].value);
    }

    // 指定したエレメント(input)と同じ行にある前月売掛残を取得
    function LastReceivable(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".LastReceivable")[0].value);
    }

    // 指定したエレメント(input)と同じ行にある前月買掛残を取得
    function LastPayable(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".LastPayable")[0].value);
    }

    // 指定したエレメント(input)と同じ行にある前年売上実績を取得
    function LastProceeds(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".LastProceeds")[0].value);
    }

    // 指定したエレメント(input)と同じ行にある当年売上目標を取得
    function ProceedsTarget(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".ProceedsTarget")[0].value);
    }

    function comma(obj)
    {
        //桁区切りして配置（前回請求残）
        lastclaim = Number(LastClaimBalance(obj)).toLocaleString();
        detail(obj).querySelectorAll(".LastClaimBalance")[0].value = lastclaim;

        //桁区切りして配置（前月売掛残）
        receivable = Number(LastReceivable(obj)).toLocaleString();
        detail(obj).querySelectorAll(".LastReceivable")[0].value = receivable;
        
        //桁区切りして配置（前月買掛残）
        payable = Number(LastPayable(obj)).toLocaleString();
        detail(obj).querySelectorAll(".LastPayable")[0].value = payable;

        //桁区切りして配置（前年売上実績）
        proceeds = Number(LastProceeds(obj)).toLocaleString();
        detail(obj).querySelectorAll(".LastProceeds")[0].value = proceeds;

        //桁区切りして配置（当年売上目標）
        target = Number(ProceedsTarget(obj)).toLocaleString();
        detail(obj).querySelectorAll(".ProceedsTarget")[0].value = target;
    }

    $('#form').submit(function(){
        var lastclaim = removeComma($(".LastClaimBalance").val());
        var receivable = removeComma($(".LastReceivable").val());
        var payable = removeComma($(".LastPayable").val());
        var proceeds = removeComma($(".LastProceeds").val());
        var target = removeComma($(".ProceedsTarget").val());

        $(".LastClaimBalance").val(lastclaim);
        $(".LastReceivable").val(receivable);
        $(".LastPayable").val(payable);
        $(".LastProceeds").val(proceeds);
        $(".ProceedsTarget").val(target);
    });
