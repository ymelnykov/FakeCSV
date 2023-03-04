function showMessage() {
    // Show message, if any, as alert
    try {actMessage = document.getElementById('actMessage').innerText;
        if (actMessage) {
            setTimeout(function() {alert(actMessage)}, 500);
        }
    }
    catch (e) {
        console.log(e);
    }
}


function removeColumn(i) {
    // Remove column using Delete button
    if (i == 1) {
        alert('This column cannot be deleted!');
    } else {
        document.querySelector(`#column${i}`).remove();
    }
}


function addColumn() {
    // Add new column using Add column button
    let columnList = document.querySelector('#columns');
    let lastColumn = columnList.lastElementChild;
    let i = parseInt(lastColumn.id.slice(6));
    i = i + 1;
    let newColumn = document.createElement('div');
    newColumn.className = 'mb-2';
    newColumn.id = 'column' + i;
    newColumn.innerHTML = lastColumn.innerHTML;
    columnList.append(newColumn);
    let columnType = newColumn.querySelector('#id_type');
    columnType.setAttribute('onchange', `showHideRangeLimits('${i}')`);
    let deleteColumnButton = newColumn.querySelector('#delete');
    deleteColumnButton.setAttribute('onclick', `removeColumn('${i}')`);
    deleteColumnButton.removeAttribute('disabled');
    let rangeLimits = newColumn.querySelectorAll('.range-tag');
    rangeLimits.forEach(rangeLimit => {
        rangeLimit.className = 'col-1 invisible range-tag';
    })
    let columnFields = newColumn.querySelectorAll('.column-tag');
    columnFields.forEach(columnField => {
        columnField.value = '';
        if (columnField.tagName == 'select') {
            columnField.setAttribute('data-value', '');
        }
    })
}


function showHideRangeLimits(i) {
    // Show/hide range limits upon selecting Integer or Text column type
    let column = document.querySelector(`#column${i}`);
    let columnType = column.querySelector('#id_type');
    let rangeLimits = column.querySelectorAll('.range-tag');
    let type = columnType.value;
    if (type =='pyint' | type =='paragraph') {
        rangeLimits.forEach(rangeLimit => {
            let list = rangeLimit.classList;
            if (list.contains('invisible')) {
                list.remove('invisible');
            }
        })
    } else {
        rangeLimits.forEach(rangeLimit => {
            let list = rangeLimit.classList;
            if (!list.contains('invisible')) {
                list.add('invisible')
            }
        })
    }
}


function validateColumnOrder() {
    // Check if column order is unique for all columns
    const columnOrders = document.querySelectorAll('.order-tag');
    let orderList = [];
    columnOrders.forEach(columnOrder => {
        if (orderList.includes(columnOrder.value)) {
            alert('Please check columns order. It must be unique positive integer number.');
            return false;
        } else {
            orderList.push(columnOrder.value);
        }
    })
    return true;
}


function createDataSet(schemaId) {
    // Create new dataset using Fetch API
    const rowsNumber = document.querySelector('#id_rows').value;
    const dataSetList = document.querySelector('#datasets');
    let lastDataSet = dataSetList.lastElementChild;
    let i = parseInt(lastDataSet.id.slice(7));
    if (i === 1) {
        let newDataSet = lastDataSet;
        newDataSet.classList.remove('d-none');
        newDataSet.querySelector('#number1').innerText = '1';
    } else {
        i = i + 1;
        let newDataSet = document.createElement('div');
        newDataSet.className = 'row mb-2';
        newDataSet.id = 'dataset' + i;
        newDataSet.innerHTML = dataSetList.querySelector('#dataset1').innerHTML;
        dataSetList.append(newDataSet);
        const dataSetFields = newDataSet.querySelectorAll('.dataset-tag');
        dataSetFields.forEach(dataSetField => {
            dataSetField.id = dataSetField.id.replace('1', `${i}`);
        })
        newDataSet.querySelector(`#number${i}`).innerText = `${i}`;
    }
    fetch('/create_dataset', {
        method: 'POST',
        body: JSON.stringify({
            schemaId: schemaId,
            rowsNumber: rowsNumber
        })
    })
    .then(response=> response.json())
    .then(response => {
        newDataSet = dataSetList.lastElementChild;
        newDataSet.querySelector(`#created${i}`).innerText = response.created;
        newDataSet.querySelector(`#badge_processing${i}`).classList.add('d-none');
        newDataSet.querySelector(`#badge_ready${i}`).classList.remove('d-none');
        newDataSet.querySelector(`#link${i}`).innerHTML = `<a href="${response.url}">Download</a>`;
    })
}


document.addEventListener('DOMContentLoaded', function() {
    showMessage();
})