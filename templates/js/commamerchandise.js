    function removeComma(number) {
        var removed = number.replace(/,/g, '');
        return parseFloat(removed);
        //return parseInt(removed, 10);
    }

    // 指定したエレメント(input)が所属する行(tr)を取得
    function detail(obj)
    {
        return obj.parentElement.parentElement.parentElement ;
        // return obj.parentElement.parentElement ;
    }

    // 指定したエレメント(input)と同じ行にある仕入単価を取得
    function McdUnitPrice(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".McdUnitPrice")[0].value);
    }

    // 指定したエレメント(input)と同じ行にある販売単価を取得
    function McdSellPrice(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".McdSellPrice")[0].value);
    }

    // 指定したエレメント(input)と同じ行にある仕入単価を取得
    function McdProcessfee(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".McdProcessfee")[0].value);
    }

    // 指定したエレメント(input)と同じ行にある加工賃を取得
    function McdDtlPrice(obj)
    {
        return removeComma(detail(obj).querySelectorAll(".McdDtlPrice")[0].value);
    }

    function comma(obj)
    {
        //桁区切りして配置（仕入単価）
        UnitPrice = Number(McdUnitPrice(obj)).toLocaleString();
        detail(obj).querySelectorAll(".McdUnitPrice")[0].value = UnitPrice;

        //桁区切りして配置（販売単価）
        SellPrice = Number(McdSellPrice(obj)).toLocaleString();
        detail(obj).querySelectorAll(".McdSellPrice")[0].value = SellPrice;
        
        //桁区切りして配置（加工賃）
        Processfee = Number(McdProcessfee(obj)).toLocaleString();
        detail(obj).querySelectorAll(".McdProcessfee")[0].value = Processfee;
    }
   
    function detailcomma(obj)
    {
        //桁区切りして配置（仕入単価）
        DtlPrice = Number(McdDtlPrice(obj)).toLocaleString();
        detail(obj).querySelectorAll(".McdDtlPrice")[0].value = DtlPrice;
    }