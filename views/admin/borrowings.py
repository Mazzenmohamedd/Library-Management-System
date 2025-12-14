import streamlit as st
from utils.data_manager import DataManager
from datetime import datetime

def render_admin_borrowings(books_manager):
    st.header("Borrowings Management")
    
    loans = DataManager.load_loans()
    
    # Flatten loans
    all_loans = []
    for email, user_loans in loans.items():
        for loan in user_loans:
            all_loans.append({
                "User": email,
                "ISBN": loan['isbn'],
                "Due Date": loan['due_date'],
                "Borrowed Date": loan.get('borrowed_date', 'N/A')
            })
            
    if not all_loans:
        st.info("No active borrowings.")
    else:
        st.subheader("Active Loans List")
        st.dataframe(all_loans, use_container_width=True)
        
        st.divider()
        st.subheader("Process Return")
        
        # Admin Return Interface
        loan_options = [f"{l['User']} - {l['ISBN']}" for l in all_loans]
        selected_loan_str = st.selectbox("Select Loan to Return:", ["Select..."] + loan_options)
        
        if selected_loan_str != "Select...":
            user_email = selected_loan_str.split(" - ")[0]
            isbn = selected_loan_str.split(" - ")[1]
            
            book = books_manager.get_book(isbn)
            
            if st.button("Mark as Returned"):
                # We need to simulate the return process.
                # Ideally we call the user.return_book logic, but we don't have the user object instantiated as a RegularUser here easily without login.
                # So we manually do the steps: 
                # 1. Update Inventory (increment avail)
                # 2. Add to History
                # 3. Remove from Loans
                
                # 1. Inventory
                if book:
                    book.return_book() # This increments available_quantity
                    books_manager.save_books()
                
                # 2. History (Calculate fine if needed)
                # Find loan data
                loan_data = next((l for l in loans[user_email] if l['isbn'] == isbn), None)
                if loan_data:
                    due_date = datetime.strptime(loan_data['due_date'], "%Y-%m-%d")
                    return_date = datetime.now()
                    fine = 0.0
                    if return_date > due_date:
                        days = (return_date - due_date).days
                        fine = days * 10.0 # Standard fine
                    
                    history_record = {
                        'title': book.title if book else "Unknown",
                        'author': book.author if book else "Unknown",
                        'return_date': return_date.strftime("%Y-%m-%d"),
                        'fine': fine
                    }
                    DataManager.add_history(user_email, history_record)
                
                # 3. Remove Loan
                DataManager.remove_loan(user_email, isbn)
                
                st.success(f"Book {isbn} returned for user {user_email}. Fine: {fine} LE")
                st.rerun()
