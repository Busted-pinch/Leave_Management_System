# 🏢 Employee Leave Management System (ELMS)

![GitHub repo size](https://img.shields.io/github/repo-size/Busted-pinch/Leave_Management_System)
![GitHub contributors](https://img.shields.io/github/contributors/Busted-pinch/Leave_Management_System)
![GitHub issues](https://img.shields.io/github/issues/Busted-pinch/Leave_Management_System)
![GitHub license](https://img.shields.io/github/license/Busted-pinch/Leave_Management_System)

✨ **Streamline employee leave management, approvals, and analytics with ELMS!**

---

## ⚙️ Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/Busted-pinch/Leave_Management_System.git
cd Leave_Management_System
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure Environment Variables**
   Create a `.env` file and add your configuration:

```
MONGO_URI=<your_mongodb_connection_string>
SECRET_KEY=<your_jwt_secret_key>
```

4. **Run the Application**

```bash
python main.py
```

Access the system at: [http://localhost:8000](http://localhost:8000) 🌐

---

## 📝 Features & Usage

### Employee

* Sign up / login 👨‍💼
* Apply for leave 🏖️ (single/multiple days)
* View leave history 📜
* Check remaining leave balance 📋
* Receive approval/rejection notifications ✅❌

### Manager

* Sign up / login 👩‍💼
* View all pending leave requests 🕒
* Approve or reject leaves ✅❌
* See department-wise leave reports 📊
* Monitor employee attendance and leave patterns

### HR/Admin

* Monitor overall leave balance of all employees 📋
* Generate analytics and reports for management 📈
* Fix leave entries for frontend compatibility 🛠️

### Backend Features

* **Python / FastAPI** 🐍
* **JWT authentication** 🔐
* Role-based access control (Employee / Manager / HR)
* MongoDB database 🍃 for flexible storage
* Data validation via Pydantic models ✅

### Frontend Features

* HTML, CSS, JavaScript for responsive UI ⚛️
* Dynamic dashboards for Managers & Employees
* Real-time leave request updates

---

## 🛠️ Tech Stack

| Layer          | Technology                     |
| -------------- | ------------------------------ |
| Backend        | Python, FastAPI                |
| Database       | MongoDB                        |
| Frontend       | HTML, CSS, JavaScript / React  |
| Authentication | JWT                            |
| Deployment     | Local / Optional cloud hosting |

---

## 🚀 Project Highlights (Work Done So Far)

* Complete Employee & Manager signup/login flow
* Leave apply, approve, reject functionalities implemented
* Fixed data compatibility issues for frontend (e.g., date formats, leave IDs)
* Role-based dashboard views (Manager / Employee)
* Integrated JWT authentication for secure API access
* Added RESTful APIs for CRUD operations on leaves and users
* Setup CORS and environment configuration
* Implemented leave reporting and analytics endpoints

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repository 🍴
2. Create a new branch:

```bash
git checkout -b feature-name
```

3. Make your changes and commit:

```bash
git commit -m "Add feature"
```

4. Push to your branch:

```bash
git push origin feature-name
```

5. Create a Pull Request 🔃

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 📬 Contact

* **Backend Dev**: Prathamesh Mete
* **GitHub**: [Busted-pinch](https://github.com/Busted-pinch)
* **Email**: [metepratham04@gmail.com](mailto:metepratham04@gmail.com)
