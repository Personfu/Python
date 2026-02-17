// ============================================================
// REST API Integration — Complete Implementation
// CIS 195 — Web Development | Preston Furulie
// ============================================================
// Covers: fetch API, async/await, GET/POST/PUT/DELETE,
// error handling, request headers, query parameters,
// pagination, loading states, retry logic, abort controller,
// response caching, and a full API client class.
// ============================================================


// ── Section 1: Basic Fetch (GET) ───────────────────────────

async function fetchUsers() {
    /**
     * Simple GET request using async/await.
     * JSONPlaceholder is a free fake REST API for testing.
     */
    try {
        const response = await fetch(
            "https://jsonplaceholder.typicode.com/users"
        );

        // Check if the response was successful (status 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status} ${response.statusText}`);
        }

        const users = await response.json();

        console.log(`Fetched ${users.length} users:`);
        users.forEach(user => {
            console.log(`  ${user.id}. ${user.name} (${user.email})`);
        });

        return users;

    } catch (error) {
        console.error("Failed to fetch users:", error.message);
        return [];
    }
}


// ── Section 2: POST Request ────────────────────────────────

async function createPost(title, body, userId = 1) {
    /**
     * POST request: send JSON data to create a new resource.
     * Must include Content-Type header for JSON bodies.
     */
    try {
        const response = await fetch(
            "https://jsonplaceholder.typicode.com/posts",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // "Authorization": "Bearer <token>"  // for auth APIs
                },
                body: JSON.stringify({
                    title: title,
                    body: body,
                    userId: userId
                })
            }
        );

        if (!response.ok) {
            throw new Error(`POST failed: ${response.status}`);
        }

        const data = await response.json();
        console.log("Created:", data);
        return data;

    } catch (error) {
        console.error("Create failed:", error.message);
        return null;
    }
}


// ── Section 3: PUT and DELETE ──────────────────────────────

async function updatePost(id, updates) {
    /**
     * PUT request: update an existing resource.
     * Sends the full updated object.
     */
    const response = await fetch(
        `https://jsonplaceholder.typicode.com/posts/${id}`,
        {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updates)
        }
    );
    return await response.json();
}

async function deletePost(id) {
    /**
     * DELETE request: remove a resource.
     * Usually returns empty body with 200 or 204 status.
     */
    const response = await fetch(
        `https://jsonplaceholder.typicode.com/posts/${id}`,
        { method: "DELETE" }
    );
    return response.ok;
}


// ── Section 4: Query Parameters ────────────────────────────

async function fetchWithParams(baseUrl, params = {}) {
    /**
     * Build a URL with query parameters programmatically.
     * URLSearchParams handles encoding special characters.
     */
    const url = new URL(baseUrl);
    Object.entries(params).forEach(([key, value]) => {
        url.searchParams.append(key, value);
    });

    console.log("Request URL:", url.toString());
    const response = await fetch(url);
    return await response.json();
}

// Usage: fetchWithParams("https://jsonplaceholder.typicode.com/posts", {
//     userId: 1, _limit: 5, _sort: "title"
// });


// ── Section 5: Abort Controller (Cancel Requests) ──────────

async function fetchWithTimeout(url, timeoutMs = 5000) {
    /**
     * Abort a request if it takes too long.
     * AbortController allows cancelling in-flight fetch requests.
     */
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    try {
        const response = await fetch(url, {
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        return await response.json();

    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === "AbortError") {
            console.error(`Request aborted after ${timeoutMs}ms`);
        }
        throw error;
    }
}


// ── Section 6: Retry Logic ─────────────────────────────────

async function fetchWithRetry(url, options = {}, maxRetries = 3) {
    /**
     * Retry failed requests with exponential backoff.
     * Waits 1s, 2s, 4s between retries.
     */
    let lastError;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return await response.json();

        } catch (error) {
            lastError = error;
            const delay = Math.pow(2, attempt) * 1000; // exponential backoff
            console.warn(`Attempt ${attempt + 1} failed. Retrying in ${delay}ms...`);

            if (attempt < maxRetries - 1) {
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    }

    throw new Error(`Failed after ${maxRetries} attempts: ${lastError.message}`);
}


// ── Section 7: Full API Client Class ───────────────────────

class APIClient {
    /**
     * Reusable API client with base URL, auth, error handling,
     * and convenience methods for all HTTP verbs.
     */

    constructor(baseUrl, options = {}) {
        this.baseUrl = baseUrl.replace(/\/$/, ""); // remove trailing slash
        this.defaultHeaders = {
            "Content-Type": "application/json",
            ...options.headers
        };
        this.token = options.token || null;
    }

    setToken(token) {
        this.token = token;
    }

    _getHeaders() {
        const headers = { ...this.defaultHeaders };
        if (this.token) {
            headers["Authorization"] = `Bearer ${this.token}`;
        }
        return headers;
    }

    async _request(method, path, body = null, params = {}) {
        const url = new URL(`${this.baseUrl}${path}`);
        Object.entries(params).forEach(([k, v]) => url.searchParams.append(k, v));

        const options = {
            method: method,
            headers: this._getHeaders()
        };

        if (body && ["POST", "PUT", "PATCH"].includes(method)) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(url, options);

        if (!response.ok) {
            const errorBody = await response.text();
            let errorData;
            try { errorData = JSON.parse(errorBody); } catch { errorData = errorBody; }
            const error = new Error(`API Error: ${response.status} ${response.statusText}`);
            error.status = response.status;
            error.data = errorData;
            throw error;
        }

        // Handle 204 No Content
        if (response.status === 204) return null;

        return await response.json();
    }

    // Convenience methods
    get(path, params = {})           { return this._request("GET", path, null, params); }
    post(path, body)                  { return this._request("POST", path, body); }
    put(path, body)                   { return this._request("PUT", path, body); }
    patch(path, body)                 { return this._request("PATCH", path, body); }
    delete(path)                      { return this._request("DELETE", path); }
}


// ── Section 8: Dynamic DOM Rendering from API Data ─────────

async function renderUserCards() {
    /**
     * Fetch data from API and dynamically create DOM elements
     * to display it. Includes loading and error states.
     */
    const container = document.getElementById("users");
    if (!container) return;

    // Loading state
    container.innerHTML = '<div class="loading">Loading users...</div>';

    try {
        const users = await fetchUsers();

        container.innerHTML = "";

        if (users.length === 0) {
            container.innerHTML = '<div class="empty">No users found.</div>';
            return;
        }

        users.forEach(user => {
            const card = document.createElement("div");
            card.className = "user-card";
            card.innerHTML = `
                <h3>${user.name}</h3>
                <p class="email">${user.email}</p>
                <p class="company">${user.company.name}</p>
                <p class="location">${user.address.city}</p>
            `;
            card.addEventListener("click", () => {
                console.log(`Selected user: ${user.name}`);
            });
            container.appendChild(card);
        });

    } catch (error) {
        container.innerHTML = `
            <div class="error">
                <p>Failed to load users: ${error.message}</p>
                <button onclick="renderUserCards()">Retry</button>
            </div>
        `;
    }
}


// ── Section 9: Pagination Helper ───────────────────────────

async function fetchPaginated(page = 1, limit = 10) {
    /**
     * Fetch paginated data and return results with metadata.
     */
    const data = await fetchWithParams(
        "https://jsonplaceholder.typicode.com/posts",
        { _page: page, _limit: limit }
    );

    return {
        items: data,
        page: page,
        limit: limit,
        hasMore: data.length === limit
    };
}


// ── Initialize ─────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
    renderUserCards();
});
