import streamlit as st
from utils.style import apply_style
from BooksManager import BooksManager
from UserManager import UserManager
from transaction import TransactionManager
from views.dashboard import render_dashboard
from views.search import render_search
from views.history import render_history
from views.reservations import render_reservations
from views.admin.dashboard import render_admin_dashboard
from views.admin.books import render_admin_books
from views.admin.members import render_admin_members
from views.admin.borrowings import render_admin_borrowings
from views.admin.reservations import render_admin_reservations
from views.admin.reports import render_admin_reports

# Page 
st.set_page_config(page_title="Library System", page_icon="🏛", layout="wide")

apply_style()

# Initialize State
if 'books_manager' not in st.session_state:
    st.session_state['books_manager'] = BooksManager("books.csv")
if 'user_manager' not in st.session_state:
    st.session_state['user_manager'] = UserManager("MembersData.csv")
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'active_page' not in st.session_state:
    st.session_state['active_page'] = 'Dashboard' # Default

def login_register_page():
    st.title("🏛 Library Management System")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login"):
            email = st.text_input("Email")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                user = st.session_state['user_manager'].login(email, pwd)
                if user:
                    st.session_state['user'] = user
                    # Set default page based on role
                    if user.role == 'librarian':
                        st.session_state['active_page'] = 'AdminDashboard'
                    else:
                        st.session_state['active_page'] = 'Dashboard'
                    st.rerun()
                else:
                    st.error("Invalid Credentials")

    with tab2:
        st.subheader("Create Account")
        role_choice = st.radio("Are you registering as:", ["User", "Manager"])
        
        with st.form("register"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", 5, 100)
            email = st.text_input("Email")
            pwd = st.text_input("Password", type="password")
            
            if st.form_submit_button("Register"):
                role_key = "librarian" if role_choice == "Manager" else "user"
                success, msg = st.session_state['user_manager'].register_user(name, age, email, pwd, role=role_key)
                if success:
                    st.success("Account created! Please login.")
                else:
                     st.error(msg)

def render_sidebar():
    user = st.session_state['user']
    st.sidebar.title(f"👤 {user.name}")
    st.sidebar.caption(f"Role: {user.role.upper()}")
    st.sidebar.divider()
    
    # --- MANAGER MENU ---
    if user.role == 'librarian':
        st.sidebar.subheader("Admin Portal")
        
        menu_map = {
            "AdminDashboard": "📊 Dashboard",
            "AdminBooks": "📚 Books",
            "AdminMembers": "👥 Members",
            "AdminBorrowings": "📆 Borrowings",
            "AdminReservations": "🔔 Reservations",
            "AdminReports": "📈 Reports"
        }
        
        for key, label in menu_map.items():
            t_type = "primary" if st.session_state.get('active_page') == key else "secondary"
            if st.sidebar.button(label, key=f"nav_{key}", use_container_width=True, type=t_type):
                st.session_state['active_page'] = key
                st.rerun()

    # --- USER MENU ---
    else:
        st.sidebar.subheader("Library Menu")
        
        menu_map = {
            "Dashboard": "🏠 Dashboard",
            "Search": "🔍 Search & Borrow",
            "Reservations": "🔖 Reservations",
            "History": "📜 History"
        }
        
        for key, label in menu_map.items():
            t_type = "primary" if st.session_state.get('active_page') == key else "secondary"
            if st.sidebar.button(label, key=f"nav_{key}", use_container_width=True, type=t_type):
                st.session_state['active_page'] = key
                st.rerun()

    # Logout (Bottom)
    st.sidebar.divider()
    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        st.session_state['user'] = None
        st.session_state['active_page'] = 'Dashboard'
        st.rerun()

def main():
    if not st.session_state['user']:
        login_register_page()
        return

    # Render Sidebar
    render_sidebar()
    
    # Routing
    page = st.session_state['active_page']
    user = st.session_state['user']
    bm = st.session_state['books_manager']
    um = st.session_state['user_manager']
    
    # User Pages
    if page == 'Dashboard':
        render_dashboard(user, bm, um)
    elif page == 'Search':
        render_search(user, bm)
    elif page == 'Reservations':
        render_reservations(user)
    elif page == 'History':
        render_history(user, bm)
        
    # Admin Pages
    elif page == 'AdminDashboard':
        if user.role != 'librarian': st.error("Unauthorized"); return
        render_admin_dashboard(bm, um)
    elif page == 'AdminBooks':
        if user.role != 'librarian': st.error("Unauthorized"); return
        render_admin_books(bm)
    elif page == 'AdminMembers':
        if user.role != 'librarian': st.error("Unauthorized"); return
        render_admin_members(um)
    elif page == 'AdminBorrowings':
        if user.role != 'librarian': st.error("Unauthorized"); return
        render_admin_borrowings(bm)
    elif page == 'AdminReservations':
        if user.role != 'librarian': st.error("Unauthorized"); return
        render_admin_reservations(bm)
    elif page == 'AdminReports':
        if user.role != 'librarian': st.error("Unauthorized"); return
        render_admin_reports(bm, um)
    
    # Fallback
    else:
        # If page state is weird or old 'Manager' key exists
        if user.role == 'librarian':
             render_admin_dashboard(bm, um)
        else:
             render_dashboard(user, bm, um)

if __name__ == "__main__":
    main()
