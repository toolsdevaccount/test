document.addEventListener('DOMContentLoaded', function(){
    tabs = document.querySelectorAll('#js-tab li');
    for(i = 0; i < tabs.length; i++) {
        tabs[i].addEventListener('click', tabSwitch, false);
    }

    function tabSwitch(){
        tabs = document.querySelectorAll('#js-tab li');
        var node = Array.prototype.slice.call(tabs, 0);
        node.forEach(function (element) {
        element.classList.remove('fds-tabs__item--active');
        });
        this.classList.add('fds-tabs__item--active');

        content = document.querySelectorAll('.tab-contents-item');
        var node = Array.prototype.slice.call(content, 0);
        node.forEach(function (element) {
        element.classList.remove('active');
        });

        const arrayTabs = Array.prototype.slice.call(tabs);
        const index = arrayTabs.indexOf(this);
        
        document.querySelectorAll('.tab-contents-item')[index].classList.add('active');
        };
    });    