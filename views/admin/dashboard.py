import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

def render_admin_dashboard(books_manager, user_manager):
    st.header("Admin Dashboard")
    
    # 1. Key Metrics
    total_books = len(books_manager.books)
    total_users = len(user_manager.users)
    
    loans = DataManager.load_loans()
    active_loans_count = sum(len(user_loans) for user_loans in loans.values())
    
    # Calculate Overdue
    overdue_count = 0
    from datetime import datetime
    now = datetime.now()
    for user_loans in loans.values():
        for loan in user_loans:
            try:
                due = datetime.strptime(loan['due_date'], "%Y-%m-%d")
                if now > due:
                    overdue_count += 1
            except:
                pass
                
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Books", total_books)
    col2.metric("Total Members", total_users)
    col3.metric("Active Loans", active_loans_count)
    col4.metric("Overdue Books", overdue_count, delta_color="inverse")
    
    st.divider()
    
    # 2. Quick Activity Overview (Mockup or real if transaction log exists)
    # We have TransactionManager but it logs to file. Let's read it if possible or just show placeholder.
    # We will implement a simple recent activity view if transaction manager gives access. 
    # TransactionManager log_transaction appends to transactions.csv.
    
    st.subheader("Recent System Activity")
    try:
        df = pd.read_csv("transactions.csv")
        st.dataframe(df.tail(10).iloc[::-1], use_container_width=True) # Show last 10 reversed
    except:
        st.info("No recent activity found.")
