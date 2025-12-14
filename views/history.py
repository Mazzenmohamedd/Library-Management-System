import streamlit as st
from utils.data_manager import DataManager

def render_history(user, books_manager):
    st.header("Borrowing History")
    
    st.subheader("Active Loans")
    loans = DataManager.get_user_loans(user.email)
    
    if loans:
        for loan in loans:
            book = books_manager.get_book(loan['isbn'])
            if book:
                with st.expander(f"📘 {book.title}", expanded=True):
                    c1, c2 = st.columns([3,1])
                    with c1:
                        st.write(f"**Due Date:** {loan['due_date']}")
                    with c2:
                         if st.button("Return", key=f"ret_h_{loan['isbn']}"):
                             msg = user.return_book(book)
                             DataManager.remove_loan(user.email, loan['isbn'])
                             st.success(msg)
                             st.rerun()
    else:
        st.info("No active loans.")
        
    st.divider()
    st.subheader("Past Returns")
    history = user.get_history()
    if history:
        df = []
        for h in history:
            df.append({
                "Title": h['title'],
                "Author": h['author'],
                "Returned On": h['return_date'],
                "Fine": h['fine']
            })
        st.dataframe(df, use_container_width=True)
    else:
        st.caption("No history yet.")
