// REST API Integration
// CIS 195 — Web Development | Preston Furulie

// Fetch users from JSONPlaceholder API
async function fetchUsers() {
    try {
        const response = await fetch(
            "https://jsonplaceholder.typicode.com/users"
        );

        if (!response.ok) {
            throw new Error("HTTP error: " + response.status);
        }

        const users = await response.json();

        // Display each user as a card
        const container = document.getElementById("users");
        users.forEach(user => {
            const card = document.createElement("div");
            card.className = "user-card";
            card.innerHTML = `
                <h3>${user.name}</h3>
                <p>${user.email}</p>
                <p>${user.company.name}</p>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Failed to fetch:", error);
    }
}

// POST request example
async function createPost(title, body) {
    const response = await fetch(
        "https://jsonplaceholder.typicode.com/posts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, body, userId: 1 })
    });
    return await response.json();
}

fetchUsers();
