    function removeComma(number) {
        var removed = number.replace(/,/g, '');
        return parseInt(removed, 10);
    }

    // 指定したエレメント(input)が所属する行(tr)を取得
    function detail(obj)
    {
        return obj.parentElement.parentElement.parentElement ;
    }

    // 指定したエレメント(input)と同じ行にある仕入単価を取得
    function DetailUnitPrice(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".DetailUnitPrice")[0].value);
    }

    // 指定したエレメント(input)と同じ行にある通常単価を取得
    function DetailPrice(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".DetailPrice")[0].value);
    }

    // 指定したエレメント(input)と同じ行にあるUP分単価を取得
    function DetailOverPrice(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".DetailOverPrice")[0].value);
    }

    // 指定したエレメント(input)と同じ行にある販売単価を取得
    function DetailSellPrice(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".DetailSellPrice")[0].value);
    }

    $('#form').submit(function(){
        var DetailUnitPrice = removeComma($(".DetailUnitPrice").val());
        var DetailPrice = removeComma($(".DetailPrice").val());
        var DetailOverPrice = removeComma($(".DetailOverPrice").val());
        var DetailSellPrice = removeComma($(".DetailSellPrice").val());

        $(".DetailUnitPrice").val(DetailUnitPrice);
        $(".DetailPrice").val(DetailPrice);
        $(".DetailOverPrice").val(DetailOverPrice);
        $(".DetailSellPrice").val(DetailSellPrice);
    });
