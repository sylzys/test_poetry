$(document).ready(function () {
    // alert("hello");
    $('#loader').hide();
    $('form').on('click', function(e) {
        $('#loader').show();
    });

    const onChangeElement = (qSelector, cb)=>{
    const targetNode = document.querySelector(qSelector);
    if(targetNode){
        const config = { attributes: true, childList: false, subtree: false };
        const callback = function(mutationsList, observer) {
            cb($(qSelector))
        };
        const observer = new MutationObserver(callback);
        observer.observe(targetNode, config);
    }else {
        console.error("onChangeElement: Invalid Selector")
    }
    }
    onChangeElement('#prediction', function(jqueryElement){
        alert('changed')
    })
});