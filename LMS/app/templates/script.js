// Tab Switching Functions
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

// Page Navigation
function showPage(page) {
    const pages = ['loginPage', 'registerPage', 'dashboardPage'];
    pages.forEach(p => {
        document.getElementById(p).classList.add('hidden');
    });
    
    if (page === 'login') {
        document.getElementById('loginPage').classList.remove('hidden');
    } else if (page === 'register') {
        document.getElementById('registerPage').classList.remove('hidden');
    } else if (page === 'dashboard') {
        document.getElementById('dashboardPage').classList.remove('hidden');
    }
}

// Dashboard Section Navigation
function showDashboardSection(section) {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.page-section');
    
    navItems.forEach(item => item.classList.remove('active'));
    sections.forEach(sec => sec.classList.remove('active'));
    
    event.target.closest('.nav-item').classList.add('active');
    
    if (section === 'profile') {
        document.getElementById('profileSection').classList.add('active');
    } else if (section === 'apply') {
        document.getElementById('applySection').classList.add('active');
    } else if (section === 'status') {
        document.getElementById('statusSection').classList.add('active');
    } else if (section === 'history') {
        document.getElementById('historySection').classList.add('active');
    }
}

// Form Submissions
function loginEmployee(event) {
    event.preventDefault();
    // TODO: Implement backend login logic.
    // On success, populate user data and show dashboard.
    alert('Employee login successful!');
    showPage('dashboard');
}

function registerEmployee(event) {
    event.preventDefault();
    // TODO: Implement backend registration logic.
    alert('Employee registration successful! Please login.');
    showPage('login');
}

function registerHR(event) {
    event.preventDefault();
    // TODO: Implement backend registration logic.
    alert('HR registration successful! Please login.');
    showPage('login');
}

function submitLeave(event) {
    event.preventDefault();
    // TODO: Implement backend logic to submit leave.
    alert('Leave request submitted successfully!');
    event.target.reset();
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        // TODO: Add backend logout logic if necessary (e.g., invalidate session).
        showPage('login');
    }
}

function loginHR(event) {
    event.preventDefault();
    // TODO: Implement backend login logic before redirect.
    // On success, redirect to the HR dashboard.
    window.location.href = 'hr_dashboard.html';
}
