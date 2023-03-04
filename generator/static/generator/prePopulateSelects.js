function prePopulateSelects() {
    // Prepopulate select elements
    try {
        const selects = document.querySelectorAll('select');
        selects.forEach(select => {
            if (select.dataset.value) {
                if (select.dataset.value =='pyint' | select.dataset.value =='paragraph') {
                    showRangeLimits(select.dataset.column)
                };
                let options = select.querySelectorAll('option');
                options = [].slice.call(options);
                options.every(option => {
                    if (option.value == '') {
                        option.removeAttribute('selected');
                    };
                    if (option.value == select.dataset.value) {
                        if (option.hasAttribute('selected')) {
                            return false;
                        } else {
                            option.setAttribute('selected', '')
                            return false;
                        }
                    }
                    return true;
                })
            }
        });
    } catch(e) {
        console.log(e)
    }
};


function showRangeLimits(i) {
    // Show range limits for Integer or Text column type
    let column = document.querySelector(`#column${i}`);
    let rangeLimits = column.querySelectorAll('.range-tag');
        rangeLimits.forEach(rangeLimit => {
            rangeLimit.classList.remove('invisible');
            })
}

document.addEventListener('DOMContentLoaded', function() {
    prePopulateSelects();
})