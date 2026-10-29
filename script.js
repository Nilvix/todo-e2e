// Задачи хранятся в localStorage, чтобы не пропадать после перезагрузки
const STORAGE_KEY = 'todos';
let todos = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
let filter = 'all';

const form = document.getElementById('todo-form');
const input = document.getElementById('todo-input');
const list = document.getElementById('todo-list');
const counter = document.getElementById('counter');
const error = document.getElementById('error');

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}

function render() {
  list.innerHTML = '';
  todos
    .filter(t => filter === 'all' || (filter === 'done' ? t.done : !t.done))
    .forEach(t => {
      const li = document.createElement('li');
      li.className = t.done ? 'todo-item done' : 'todo-item';
      li.dataset.id = t.id;
      li.innerHTML = `<input type="checkbox" class="toggle" ${t.done ? 'checked' : ''}>
        <span class="text"></span><button class="delete" title="Удалить">✕</button>`;
      li.querySelector('.text').textContent = t.text;   // без innerHTML, чтобы не было XSS
      list.appendChild(li);
    });
  counter.textContent = `Осталось задач: ${todos.filter(t => !t.done).length}`;
}

form.addEventListener('submit', e => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) {
    error.textContent = 'Введите текст задачи';
    error.hidden = false;
    return;
  }
  error.hidden = true;
  todos.push({ id: Date.now() + Math.random(), text, done: false });
  input.value = '';
  save();
  render();
});

list.addEventListener('click', e => {
  const id = Number(e.target.closest('li')?.dataset.id);
  if (e.target.classList.contains('toggle')) {
    const t = todos.find(t => t.id === id);
    t.done = !t.done;
  } else if (e.target.classList.contains('delete')) {
    todos = todos.filter(t => t.id !== id);
  } else {
    return;
  }
  save();
  render();
});

document.querySelectorAll('.filters button').forEach(btn => {
  btn.addEventListener('click', () => {
    filter = btn.dataset.filter;
    document.querySelectorAll('.filters button').forEach(b => b.classList.toggle('active', b === btn));
    render();
  });
});

document.getElementById('clear-done').addEventListener('click', () => {
  todos = todos.filter(t => !t.done);
  save();
  render();
});

render();
