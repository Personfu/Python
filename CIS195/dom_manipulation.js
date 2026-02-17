// JavaScript DOM Manipulation
// CIS 195 — Web Development | Preston Furulie

// Task list with add/remove functionality
const tasks = [];

function addTask(text) {
    const task = {
        id: Date.now(),
        text: text,
        completed: false
    };
    tasks.push(task);
    renderTasks();
}

function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (task) task.completed = !task.completed;
    renderTasks();
}

function renderTasks() {
    const list = document.getElementById("task-list");
    list.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");
        li.textContent = task.text;
        li.className = task.completed ? "done" : "";
        li.addEventListener("click", () => toggleTask(task.id));
        list.appendChild(li);
    });
}

// Event listener for the form
document.getElementById("task-form")
    .addEventListener("submit", (e) => {
        e.preventDefault();
        const input = document.getElementById("task-input");
        if (input.value.trim()) {
            addTask(input.value.trim());
            input.value = "";
        }
    });
