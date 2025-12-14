# 🏛 Library Management System

A modern, full-featured Library Management System built with **Python** and **Streamlit**. This application provides a seamless experience for both Library Members and Managers, featuring a "Warm Academic Glassmorphism" UI design.

## 🌟 Features

### 👤 User Section (Members)
- **Dashboard**: View active loans, reading history, and favorite books.
- **Search & Borrow**: Advanced search (Trie-based) for books by title, author, or ISBN. Borrow available books instantly.
- **Reservations**: Reserve currently unavailable books. Automatic assignment when books are returned (FIFO queue).
- **Favorites**: Mark books as favorites and manage your personal reading wish-list.
- **History**: View complete borrowing history with return dates and fines paid.

### 🛡 Manager Section (Admins)
- **Admin Dashboard**: Real-time overview of system stats (Total Books, Members, Active Loans, Overdue Items).
- **Books Management**: Full CRUD (Create, Read, Update, Delete) capabilities for the library catalog.
- **Members Management**: View registered users and manage accounts.
- **Borrowings Management**: Track all active loans and process returns/fines.
- **Reservations Management**: View, Approve, or Cancel pending reservations.
- **Reports & Analytics**: Visual insights into borrowing trends, popular books, and most active members.

## 🛠 Tech Stack
- **Frontend & Backend**: [Streamlit](https://streamlit.io/) (Python)
- **Data Persistence**: JSON & CSV (File-based storage for portability)
- **Logic**: Object-Oriented Python (Custom Managers for Data, User, transactions)

## 🚀 How to Run Locally

### Prerequisites
- Python 3.8+ installed.

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/Mazzenmohamedd/Library-Management-System.git
   cd Library-Management-System
   ```

2. **Install Dependencies**
   ```bash
   pip install streamlit pandas altair
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Access the App**
   Open your browser and navigate to `http://localhost:8501`.

## 📁 Project Structure
```
Library-Management-System/
├── app.py                  # Main Application Entry Point (SPA Controller)
├── views/                  # UI Modules
│   ├── admin/              # Admin Portal Views (Dashboard, Books, etc.)
│   ├── dashboard.py        # User Dashboard
│   ├── search.py           # User Search & Borrow
│   └── ...
├── utils/                  # Helper Utilities
│   ├── data_manager.py     # JSON Data Persistence
│   ├── reservation_manager.py
│   └── style.py            # CSS & UI Styling
├── book.py                 # Book Class
├── member.py               # Member Class
├── ...
└── assets/                 # Images and Static Files
```

---
*Created by [Mazen Mohamed](https://github.com/Mazzenmohamedd)*
