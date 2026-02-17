// ============================================================
// JavaScript DOM Manipulation — Complete Implementation
// CIS 195 — Web Development | Preston Furulie
// ============================================================
// Covers: DOM selection (getElementById, querySelector, etc.),
// element creation, event handling, delegation, classList,
// data attributes, form handling, local storage, dynamic
// rendering, and a full interactive task manager app.
// ============================================================


// ── Section 1: DOM Selection Methods ───────────────────────

// document.getElementById("id")        → single element
// document.querySelector(".class")     → first match (CSS selector)
// document.querySelectorAll("div")     → NodeList of all matches
// document.getElementsByClassName()    → HTMLCollection (live)
// document.getElementsByTagName()      → HTMLCollection (live)

function demonstrateSelectors() {
    const header     = document.getElementById("app-header");
    const firstCard  = document.querySelector(".card");
    const allCards   = document.querySelectorAll(".card");
    const buttons    = document.getElementsByTagName("button");

    console.log("Header:", header);
    console.log("First card:", firstCard);
    console.log("All cards:", allCards.length);
    console.log("Buttons:", buttons.length);
}


// ── Section 2: Element Creation & Manipulation ─────────────

function createElement(tag, attributes = {}, children = []) {
    /**
     * Factory function for creating DOM elements.
     * @param {string} tag - HTML tag name
     * @param {object} attributes - key/value pairs for attributes
     * @param {Array} children - child elements or text strings
     * @returns {HTMLElement}
     */
    const el = document.createElement(tag);

    for (const [key, value] of Object.entries(attributes)) {
        if (key === "className") {
            el.className = value;
        } else if (key === "textContent") {
            el.textContent = value;
        } else if (key === "innerHTML") {
            el.innerHTML = value;
        } else if (key.startsWith("on")) {
            el.addEventListener(key.slice(2).toLowerCase(), value);
        } else if (key.startsWith("data-")) {
            el.dataset[key.slice(5)] = value;
        } else {
            el.setAttribute(key, value);
        }
    }

    children.forEach(child => {
        if (typeof child === "string") {
            el.appendChild(document.createTextNode(child));
        } else if (child instanceof HTMLElement) {
            el.appendChild(child);
        }
    });

    return el;
}


// ── Section 3: Event Handling ──────────────────────────────

// addEventListener(type, handler, options)
// Event types: click, submit, input, change, keydown, keyup,
//              mouseover, mouseout, focus, blur, scroll, load

function setupEventHandlers() {
    // Click event
    const btn = document.getElementById("action-btn");
    if (btn) {
        btn.addEventListener("click", (e) => {
            console.log("Button clicked!", e.target);
        });
    }

    // Keyboard event
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            closeModal();
        }
    });

    // Input event (real-time as user types)
    const searchInput = document.getElementById("search");
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            const query = e.target.value.toLowerCase();
            filterTasks(query);
        });
    }
}


// ── Section 4: Event Delegation ────────────────────────────

// Instead of attaching events to each child element,
// attach ONE handler to the parent and use e.target to determine
// which child was clicked. More efficient for dynamic lists.

function setupDelegation() {
    const taskList = document.getElementById("task-list");
    if (!taskList) return;

    taskList.addEventListener("click", (e) => {
        const target = e.target;

        // Check which action button was clicked
        if (target.classList.contains("btn-complete")) {
            const taskId = target.closest("[data-id]").dataset.id;
            toggleTask(parseInt(taskId));
        } else if (target.classList.contains("btn-delete")) {
            const taskId = target.closest("[data-id]").dataset.id;
            deleteTask(parseInt(taskId));
        } else if (target.classList.contains("btn-edit")) {
            const taskId = target.closest("[data-id]").dataset.id;
            editTask(parseInt(taskId));
        }
    });
}


// ── Section 5: classList API ───────────────────────────────

// element.classList.add("class")        → add a class
// element.classList.remove("class")     → remove a class
// element.classList.toggle("class")     → add if missing, remove if present
// element.classList.contains("class")   → check if class exists
// element.classList.replace("old", "new") → swap classes

function animateElement(el) {
    el.classList.add("fade-in");
    el.addEventListener("animationend", () => {
        el.classList.remove("fade-in");
    }, { once: true });
}


// ── Section 6: Local Storage ───────────────────────────────

const StorageHelper = {
    save(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (e) {
            console.error("Storage save failed:", e);
        }
    },

    load(key, defaultValue = null) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : defaultValue;
        } catch (e) {
            console.error("Storage load failed:", e);
            return defaultValue;
        }
    },

    remove(key) {
        localStorage.removeItem(key);
    },

    clear() {
        localStorage.clear();
    }
};


// ── Section 7: Full Task Manager Application ───────────────

class TaskManager {
    /**
     * Complete task manager with CRUD operations, filtering,
     * local storage persistence, and dynamic DOM rendering.
     */

    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.tasks = StorageHelper.load("tasks", []);
        this.nextId = this.tasks.length > 0
            ? Math.max(...this.tasks.map(t => t.id)) + 1
            : 1;
        this.filter = "all"; // all, active, completed
    }

    addTask(text, priority = "medium") {
        if (!text.trim()) return;

        const task = {
            id: this.nextId++,
            text: text.trim(),
            completed: false,
            priority: priority,       // low, medium, high
            createdAt: new Date().toISOString(),
            completedAt: null
        };

        this.tasks.push(task);
        this._save();
        this.render();
    }

    toggleTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.completed = !task.completed;
            task.completedAt = task.completed ? new Date().toISOString() : null;
            this._save();
            this.render();
        }
    }

    deleteTask(id) {
        this.tasks = this.tasks.filter(t => t.id !== id);
        this._save();
        this.render();
    }

    editTask(id, newText) {
        const task = this.tasks.find(t => t.id === id);
        if (task && newText.trim()) {
            task.text = newText.trim();
            this._save();
            this.render();
        }
    }

    setFilter(filter) {
        this.filter = filter;
        this.render();
    }

    getFilteredTasks() {
        switch (this.filter) {
            case "active":
                return this.tasks.filter(t => !t.completed);
            case "completed":
                return this.tasks.filter(t => t.completed);
            default:
                return this.tasks;
        }
    }

    getStats() {
        return {
            total: this.tasks.length,
            active: this.tasks.filter(t => !t.completed).length,
            completed: this.tasks.filter(t => t.completed).length
        };
    }

    clearCompleted() {
        this.tasks = this.tasks.filter(t => !t.completed);
        this._save();
        this.render();
    }

    render() {
        if (!this.container) return;

        const filteredTasks = this.getFilteredTasks();
        const stats = this.getStats();

        this.container.innerHTML = "";

        // Stats bar
        const statsBar = createElement("div", { className: "stats-bar" }, [
            `${stats.active} active, ${stats.completed} completed, ${stats.total} total`
        ]);
        this.container.appendChild(statsBar);

        // Task list
        const list = createElement("ul", { className: "task-list", id: "task-list" });

        filteredTasks.forEach(task => {
            const priorityClass = `priority-${task.priority}`;
            const completedClass = task.completed ? "completed" : "";

            const li = createElement("li", {
                className: `task-item ${completedClass} ${priorityClass}`,
                "data-id": task.id
            }, [
                createElement("span", {
                    className: "task-text",
                    textContent: task.text
                }),
                createElement("div", { className: "task-actions" }, [
                    createElement("button", {
                        className: "btn-complete",
                        textContent: task.completed ? "Undo" : "Done"
                    }),
                    createElement("button", {
                        className: "btn-delete",
                        textContent: "Delete"
                    })
                ])
            ]);

            list.appendChild(li);
        });

        this.container.appendChild(list);

        // Filter buttons
        const filterBar = createElement("div", { className: "filter-bar" });
        ["all", "active", "completed"].forEach(f => {
            const btn = createElement("button", {
                className: `filter-btn ${f === this.filter ? "active" : ""}`,
                textContent: f.charAt(0).toUpperCase() + f.slice(1),
                onClick: () => this.setFilter(f)
            });
            filterBar.appendChild(btn);
        });
        this.container.appendChild(filterBar);
    }

    _save() {
        StorageHelper.save("tasks", this.tasks);
    }
}


// ── Section 8: Modal Dialog ────────────────────────────────

function showModal(title, message) {
    const overlay = createElement("div", { className: "modal-overlay", id: "modal" });
    const modal = createElement("div", { className: "modal" }, [
        createElement("h3", { textContent: title }),
        createElement("p", { textContent: message }),
        createElement("button", {
            textContent: "Close",
            className: "btn-close",
            onClick: closeModal
        })
    ]);
    overlay.appendChild(modal);
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) closeModal();
    });
    document.body.appendChild(overlay);
}

function closeModal() {
    const modal = document.getElementById("modal");
    if (modal) modal.remove();
}


// ── Section 9: Initialization ──────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
    const app = new TaskManager("app");

    // Add form handler
    const form = document.getElementById("task-form");
    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const input = document.getElementById("task-input");
            const priority = document.getElementById("task-priority");
            if (input && input.value.trim()) {
                app.addTask(input.value, priority ? priority.value : "medium");
                input.value = "";
                input.focus();
            }
        });
    }

    // Event delegation for task actions
    setupDelegation();

    // Initial render
    app.render();
});
