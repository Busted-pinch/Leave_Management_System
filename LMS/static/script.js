// ==========================
// 🔹 UI & Tab Switching
// ==========================
function switchLoginTab(type) {
    const tabs = document.querySelectorAll('#loginPage .tab-btn');
    const forms = document.querySelectorAll('#loginPage .form-content');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    forms.forEach(form => form.classList.remove('active'));
    
    if (type === 'employee') {
        tabs[0].classList.add('active');
        document.getElementById('employeeLoginForm').classList.add('active');
    } else {
        tabs[1].classList.add('active');
        document.getElementById('hrLoginForm').classList.add('active');
    }
}

function switchRegisterTab(type) {
    const tabs = document.querySelectorAll('#registerPage .tab-btn');
    const forms = document.querySelectorAll('#registerPage .form-content');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    forms.forEach(form => form.classList.remove('active'));
    
    if (type === 'employee') {
        tabs[0].classList.add('active');
        document.getElementById('employeeRegisterForm').classList.add('active');
    } else {
        tabs[1].classList.add('active');
        document.getElementById('hrRegisterForm').classList.add('active');
    }
}

// ==========================
// 🔹 Page Navigation
// ==========================
function showPage(page) {
    const pages = ['loginPage', 'registerPage', 'dashboardPage'];
    pages.forEach(p => document.getElementById(p).classList.add('hidden'));
    document.getElementById(`${page}Page`).classList.remove('hidden');
}

// ==========================
// 🔹 Dashboard Navigation
// ==========================
function showDashboardSection(section) {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.page-section');
    
    navItems.forEach(item => item.classList.remove('active'));
    sections.forEach(sec => sec.classList.remove('active'));
    
    event.target.closest('.nav-item').classList.add('active');
    document.getElementById(`${section}Section`).classList.add('active');
}

// ==========================
// 🔹 Backend API base
// ==========================
const API_BASE = "http://127.0.0.1:8000/api/v1/Emp_auth";

// ==========================
// 🔹 Helper function
// ==========================
async function apiRequest(url, method, body = null) {
    const options = {
        method,
        headers: { "Content-Type": "application/json" }
    };
    if (body) options.body = JSON.stringify(body);
    
    const res = await fetch(url, options);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Server Error");
    return data;
}

// ==========================
// 🔹 Employee Registration
// ==========================
async function registerEmployee(event) {
    event.preventDefault();
    const name = document.getElementById("empName").value;
    const email = document.getElementById("empEmail").value;
    const dept = document.getElementById("empDept").value;
    const password = document.getElementById("empPass").value;
    const confirmpass = document.getElementById("empConfirmPass").value;

    try {
        const data = await apiRequest(`${API_BASE}/Employee_signup`, "POST", {
            name, email, dept, password, confirmpass
        });
        alert(data.message || "Employee registration successful!");
        showPage("login");
    } catch (err) {
        alert("Registration failed: " + err.message);
    }
}

// ==========================
// 🔹 Employee Login
// ==========================
async function loginEmployee(event) {
    event.preventDefault();
    const email = document.getElementById("loginEmpEmail").value;
    const password = document.getElementById("loginEmpPass").value;

    try {
        const data = await apiRequest(`${API_BASE}/Employee_login`, "POST", { email, password });
        localStorage.setItem("token", data.access_token);
        alert("Login successful!");
        showPage("dashboard");
    } catch (err) {
        alert("Login failed: " + err.message);
    }
}

// ==========================
// 🔹 Leave Submission
// ==========================
async function submitLeave(event) {
    event.preventDefault();
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Please login first!");
        showPage("login");
        return;
    }

    const leaveData = {
        employee_id: document.getElementById("employeeId").value,
        leaveTitle: document.getElementById("leaveTitle").value,
        startDate: document.getElementById("startDate").value,
        endDate: document.getElementById("endDate").value,
        days: document.getElementById("leaveDays").value,
        description: document.getElementById("leaveDescription").value,
        status: "Pending",
        icon: "📝"
    };

    try {
        const res = await fetch("http://127.0.0.1:8000/api/v1/Emp_dash/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(leaveData)
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Failed to submit leave");
        alert(data.message);
        event.target.reset();
    } catch (err) {
        alert("Error submitting leave: " + err.message);
    }
}

// ==========================
// 🔹 Logout
// ==========================
function logout() {
    if (confirm("Are you sure you want to logout?")) {
        localStorage.removeItem("token");
        showPage("login");
    }
}

// ==========================
// 🔹 HR Functions (future)
// ==========================
async function registerHR(event) {
    event.preventDefault();
    alert("HR registration functionality coming soon!");
}

async function loginHR(event) {
    event.preventDefault();
    alert("HR login functionality coming soon!");
    // window.location.href = "hr_dashboard.html";
}
