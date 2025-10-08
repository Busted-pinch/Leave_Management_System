// ==========================
// 🔹 API Base URLs
// ==========================
const EMP_AUTH_BASE = "http://127.0.0.1:8000/api/v1/Emp_auth";
const EMP_DASH_BASE = "http://127.0.0.1:8000/api/v1/Emp_Dash";
const MAN_AUTH_BASE = "http://127.0.0.1:8000/api/v1/Man_auth";
const MAN_DASH_BASE = "http://127.0.0.1:8000/api/v1/Man_Dash";

// ==========================
// 🔹 Generic API Request
// ==========================
async function apiRequest(url, method, body = null, token = null) {
    const options = { method, headers: { "Content-Type": "application/json" } };
    if (body) options.body = JSON.stringify(body);
    if (token) options.headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(url, options);
    const text = await res.text();
    try {
        const data = JSON.parse(text);
        if (!res.ok) throw new Error(data.detail || data.message || "Server Error");
        return data;
    } catch {
        if (!res.ok) throw new Error(text || "Server returned invalid response");
        return text;
    }
}

// ==========================
// 🔹 Helpers
// ==========================
function formatDate(dateStr) {
    if (!dateStr) return "-";
    const date = new Date(dateStr);
    if (isNaN(date)) return dateStr;
    return date.toLocaleDateString("en-US", { day: "numeric", month: "short", year: "numeric" });
}

function calculateDays(start, end) {
    const startDate = new Date(start);
    const endDate = new Date(end);
    return Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
}

function getToken() {
    return localStorage.getItem("token");
}

// ==========================
// 🔹 Page & Tab Switchers
// ==========================
function showPage(page) {
    document.getElementById("loginPage").classList.toggle("hidden", page !== "login");
    document.getElementById("registerPage").classList.toggle("hidden", page === "login");
}

function switchTab(pageId, type) {
    const tabs = document.querySelectorAll(`#${pageId} .tab-btn`);
    const forms = document.querySelectorAll(`#${pageId} .form-content`);
    tabs.forEach((tab, i) => tab.classList.toggle('active', i === (type === 'employee' ? 0 : 1)));
    forms.forEach((form, i) => form.classList.toggle('active', i === (type === 'employee' ? 0 : 1)));
}

function switchLoginTab(type) { switchTab('loginPage', type); }
function switchRegisterTab(type) { switchTab('registerPage', type); }

// ==========================
// 🔹 Employee Auth
// ==========================
async function registerEmployee(event) {
    event.preventDefault();
    const name = document.getElementById("empName")?.value.trim();
    const email = document.getElementById("empEmail")?.value.trim();
    const department = document.getElementById("empDept")?.value;
    const password = document.getElementById("empPass")?.value;
    const confirmpass = document.getElementById("empConfirmPass")?.value;

    if (!name || !email || !department || !password || !confirmpass) return alert("All fields are required!");
    if (password !== confirmpass) return alert("Passwords do not match!");

    try {
        await apiRequest(`${EMP_AUTH_BASE}/Employee_signup`, "POST", { name, email, department, password });
        alert("Employee registered successfully!");
        window.location.href = "/";
    } catch (err) { alert("Registration failed: " + err.message); }
}

async function loginEmployee(event) {
    event.preventDefault();
    const email = document.getElementById("loginEmpEmail")?.value.trim();
    const password = document.getElementById("loginEmpPass")?.value;

    try {
        const data = await apiRequest(`${EMP_AUTH_BASE}/Employee_login`, "POST", { email, password });
        localStorage.setItem("token", data.access_token);
        alert("Login successful!");
        window.location.href = "/employee_dashboard";
    } catch (err) { alert("Login failed: " + err.message); }
}

// ==========================
// 🔹 HR Auth
// ==========================
async function registerHR(event) {
    event.preventDefault();
    const name = document.getElementById("hrName")?.value.trim();
    const email = document.getElementById("hrEmail")?.value.trim();
    const department = document.getElementById("hrDept")?.value;
    const password = document.getElementById("hrPass")?.value;
    const confirmpass = document.getElementById("hrConfirmPass")?.value;

    if (!name || !email || !department || !password || !confirmpass) return alert("All fields are required!");
    if (password !== confirmpass) return alert("Passwords do not match!");

    try {
        await apiRequest(`${MAN_AUTH_BASE}/Manager_signup`, "POST", { name, email, department, password });
        alert("HR registered successfully!");
        window.location.href = "/";
    } catch (err) { alert("HR registration failed: " + err.message); }
}

async function loginHR(event) {
    event.preventDefault();
    const email = document.getElementById("loginHrEmail")?.value.trim();
    const password = document.getElementById("loginHrPass")?.value;

    try {
        const data = await apiRequest(`${MAN_AUTH_BASE}/Manager_login`, "POST", { email, password });
        localStorage.setItem("token", data.access_token);
        alert("HR login successful!");
        window.location.href = "/hr_dashboard";
    } catch (err) { alert("HR login failed: " + err.message); }
}

// ==========================
// 🔹 Employee Leave
// ==========================
async function submitLeave(event) {
    event.preventDefault();
    const token = getToken();
    if (!token) return alert("Please login first!");

    // Grab values from inputs
    const leaveTitleInput = document.getElementById("leaveTitle")?.value.trim();
    const leaveTitle = leaveTitleInput || "Untitled Application"; // fallback if empty
    const startDate = document.getElementById("startDate")?.value;
    const endDate = document.getElementById("endDate")?.value;
    const description = document.getElementById("leaveDescription")?.value.trim();

    // Validate required fields
    if (!startDate || !endDate) return alert("Please provide start and end dates!");

    const leaveData = {
        leaveTitle,
        startDate,
        endDate,
        days: calculateDays(startDate, endDate),
        description
    };

    try {
        const res = await apiRequest(`${EMP_DASH_BASE}/submit`, "POST", leaveData, token);
        alert("Leave submitted successfully!");
        event.target.reset();
        loadLeaveStatus();
        loadLeaveHistory();
    } catch (err) {
        alert("Error submitting leave: " + err.message);
    }
}
async function loadEmployeeProfile() {
    const token = getToken();
    if (!token) return;
    try {
        const user = await apiRequest(`${EMP_AUTH_BASE}/me`, "GET", null, token);
        ["employeeName", "employeeEmail", "employeeDepartment", "employeeId"].forEach(id => {
            document.getElementById(id).innerText = user[id.replace("employee","").toLowerCase()] || "-";
        });
    } catch (err) { alert("Failed to load profile: " + err.message); }
}

async function loadLeaveStatus() {
    const token = getToken();
    const container = document.getElementById("leaveStatusCards");
    if (!token || !container) return;

    try {
        const leaves = await apiRequest(`${EMP_DASH_BASE}/my_leaves`, "GET", null, token);
        container.innerHTML = leaves?.length
            ? leaves.map(lv => {
                const leaveTitle = lv.leaveTitle?.trim() || lv.title?.trim() || "Untitled Application";
                const start = lv.startDate ? formatDate(lv.startDate) : "-";
                const end = lv.endDate ? formatDate(lv.endDate) : "-";
                const status = lv.status || "Pending";

                return `<div class="leave-card">
                    <h4>${leaveTitle}</h4>
                    <p>${start} - ${end}</p>
                    <p>Status: ${status}</p>
                </div>`;
            }).join("")
            : "<p>No leaves found</p>";
    } catch (err) {
        container.innerHTML = `<p>Error loading leaves: ${err.message}</p>`;
    }
}

async function loadLeaveHistory() {
    const token = getToken();
    const tbody = document.getElementById("leaveHistoryTableBody");
    if (!token || !tbody) return;

    try {
        const leaves = await apiRequest(`${EMP_DASH_BASE}/my_leaves`, "GET", null, token);
        tbody.innerHTML = leaves?.length
            ? leaves.map(lv => {
                const leaveTitle = lv.leaveTitle?.trim() || lv.title?.trim() || "Untitled Application";
                const start = lv.startDate ? formatDate(lv.startDate) : "-";
                const end = lv.endDate ? formatDate(lv.endDate) : "-";
                const days = lv.days ?? "-";
                const status = lv.status || "-";

                return `<tr>
                    <td>${leaveTitle}</td>
                    <td>${start}</td>
                    <td>${end}</td>
                    <td>${days}</td>
                    <td>${status}</td>
                </tr>`;
            }).join("")
            : `<tr><td colspan="5">No leave history found</td></tr>`;
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="5">Error loading history: ${err.message}</td></tr>`;
    }
}


// ==========================
// 🔹 HR Dashboard
// ==========================
async function loadHRProfile() {
    const token = getToken();
    if (!token) return;

    try {
        const user = await apiRequest(`${MAN_AUTH_BASE}/me`, "GET", null, token);
        ["hrName","hrEmail","hrDepartment","hrId","hrRole"].forEach(id => {
            document.getElementById(id).innerText = user[id.replace("hr","").toLowerCase()] || "-";
        });
    } catch (err) { alert("Failed to load profile: " + err.message); }
}

// ==========================
// 🔹 Load Pending Leaves (HR)
// ==========================
async function loadPendingLeaves() {
    const token = getToken();
    const container = document.getElementById("hrLeaveRequests");
    if (!token || !container) return;

    try {
        const leaves = await apiRequest(`${MAN_DASH_BASE}/leave_requests`, "GET", null, token);
        container.innerHTML = "";
        if (!leaves?.length) return container.innerHTML = "<p>No pending leave requests.</p>";

        leaves.forEach(lv => {
            const leaveId = lv._id || lv.id || lv.leave_id;
            if (!leaveId) return;

            const leaveTitle = lv.leaveTitle?.trim() || lv.title?.trim() || "Untitled Application";
            const employeeName = lv.employee?.name || lv.employee_name || lv.name || "Unknown";
            const start = lv.startDate ? formatDate(lv.startDate) : "-";
            const end = lv.endDate ? formatDate(lv.endDate) : "-";

            const card = document.createElement("div");
            card.className = "leave-card";
            card.dataset.leaveId = leaveId;
            card.innerHTML = `
                <h4>${leaveTitle}</h4>
                <p>Employee: ${employeeName}</p>
                <p>${start} - ${end}</p>
                <button class="approve-btn">Approve</button>
                <button class="reject-btn">Reject</button>
            `;
            container.appendChild(card);
        });

        container.onclick = e => {
            const card = e.target.closest(".leave-card");
            if (!card) return;
            const leaveId = card.dataset.leaveId;
            if (e.target.classList.contains("approve-btn")) decideLeave(leaveId, "approve");
            if (e.target.classList.contains("reject-btn")) decideLeave(leaveId, "reject");
        };
    } catch (err) {
        container.innerHTML = `<p>Error loading pending leaves: ${err.message}</p>`;
    }
}


async function decideLeave(leaveId, action) {
    const token = getToken();
    if (!token) return alert("Please login first!");
    try {
        const data = await apiRequest(`${MAN_DASH_BASE}/${action}_leave/${leaveId}`, "POST", null, token);
        alert(data.message || `Leave ${action}d successfully!`);
        loadPendingLeaves();
    } catch (err) { alert(`Error: ${err.message}`); }
}

async function loadEmployees() {
    const token = getToken();
    const tbody = document.getElementById("hrEmployeeTableBody");
    if (!token || !tbody) return;
    tbody.innerHTML = leaves?.length
    ? leaves.map(lv => {
        const employeeName = lv.employee?.name || lv.employee_name || lv.name || "";
        const leaveTitle = lv.leaveTitle?.trim() || "";
        return `<tr>
            <td>${leaveTitle}</td>
            <td>${employeeName}</td>
            <td>${lv.startDate ? formatDate(lv.startDate) : ""}</td>
            <td>${lv.endDate ? formatDate(lv.endDate) : ""}</td>
            <td>${lv.days ?? ""}</td>
            <td>${lv.status || ""}</td>
        </tr>`;
    }).join("")
    : `<tr><td colspan="6">No leave history found</td></tr>`;

    try {
        const employees = await apiRequest(`${MAN_DASH_BASE}/employees`, "GET", null, token);
        tbody.innerHTML = "";
        if (!employees?.length) return tbody.innerHTML = `<tr><td colspan="5">No employees found</td></tr>`;

        employees.forEach(emp => {
            tbody.innerHTML += `<tr>
                <td>${emp.employee_id || "-"}</td>
                <td>${emp.name || "-"}</td>
                <td>${emp.email || "-"}</td>
                <td>${emp.department || "-"}</td>
                <td>${emp.status || "Active"}</td>
            </tr>`;
        });
    } catch (err) { tbody.innerHTML = `<tr><td colspan="5">Error: ${err.message}</td></tr>`; }
}

// Auto-refresh employee list
setInterval(() => {
    if(document.getElementById("employeeListSection")?.classList.contains("active")) loadEmployees();
}, 5000);

// Logout
function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}

// Auto-load dashboards
window.addEventListener("DOMContentLoaded", () => {
    if (window.location.pathname.includes("employee_dashboard")) {
        loadEmployeeProfile();
        loadLeaveStatus();
        loadLeaveHistory();
    } else if (window.location.pathname.includes("hr_dashboard")) {
        loadHRProfile();
        loadPendingLeaves();
        if(document.getElementById("employeeListSection")) loadEmployees();
    }
});
