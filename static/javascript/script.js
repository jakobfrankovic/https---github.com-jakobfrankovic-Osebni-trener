// Get elements
const input = document.querySelector('.input');
const datalist = document.querySelector('#hrana');
const column = document.querySelector('#column');
const trashcan = document.querySelector('#trashcan');

// Event listeners
input.addEventListener('input', addToList);
column.addEventListener('dragstart', dragStart);
column.addEventListener('dragover', dragOver);
column.addEventListener('drop', drop);
trashcan.addEventListener('dragover', dragOver);
trashcan.addEventListener('drop', deleteItem);

// Add item to list
function addToList() {
  const value = input.value;
  const option = datalist.querySelector(`[value="${value}"]`);

  if (option) {
    const item = document.createElement('div');
    item.classList.add('item');
    item.textContent = value;
    item.setAttribute('draggable', true);
    column.appendChild(item);
  }

  input.value = '';
}

// Drag and drop functions
function dragStart(event) {
  event.dataTransfer.setData('text/plain', event.target.textContent);
  event.dataTransfer.dropEffect = 'move';
}

function dragOver(event) {
  event.preventDefault();
  event.dataTransfer.dropEffect = 'move';
}

function drop(event) {
  event.preventDefault();
  const data = event.dataTransfer.getData('text/plain');
  const item = document.createElement('div');
  item.classList.add('item');
  item.textContent = data;
  item.setAttribute('draggable', true);
  column.appendChild(item);
}

function deleteItem(event) {
  event.preventDefault();
  const data = event.dataTransfer.getData('text/plain');
  const item = column.querySelector(`.item:contains("${data}")`);

  if (item) {
    column.removeChild(item);
  }
}