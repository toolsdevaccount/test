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

document.getElementById('Destination').addEventListener('load', (e) => {
    let obj = e.target;
    let key = obj.value;
    let a = null;
    console.log(obj);
    Array.from(document.getElementById('Destination').children).forEach((opt) => {
        if(opt.value == key){
            a = opt.label;
        }
    });
    console.log(a);
});
/*
$(function(){
    var option =  document.querySelector(`input[type=hidden][name="DestinationCode"]`).value;
    var list =  document.querySelector(`datalist[id="Destination"]`);
    console.log(list);
}); */
