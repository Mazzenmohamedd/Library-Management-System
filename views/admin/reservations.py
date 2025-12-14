import streamlit as st
from utils.reservation_manager import ReservationManager
from utils.data_manager import DataManager
from datetime import datetime, timedelta

def render_admin_reservations(books_manager):
    st.header("Reservations Management")
    
    # We need to peek into reservations.json directly or allow ReservationManager to list all.
    # ReservationManager.get_user_reservations(email) filters by user.
    # We need 'get_all_reservations'. Let's check if it exists or access file via DataManager.
    
    # Assuming DataManager has generic load:
    reservations_data = DataManager.load_json(DataManager.load_json("reservations.json") if hasattr(DataManager, "RESERVATIONS_FILE") else "reservations.json")
    # Actually DataManager.load_json takes filename. defined in utils/data_manager.py
    
    from utils.data_manager import RESERVATIONS_FILE
    data = DataManager.load_json(RESERVATIONS_FILE)
    
    # Data is a list of reservation objects
    all_res = data if isinstance(data, list) else []
            
    # Filter pending
    pending_res = [r for r in all_res if r['status'] == 'pending']
    
    if not pending_res:
        st.info("No pending reservations.")
    else:
        st.subheader("Pending Reservations")
        for res in pending_res:
            with st.expander(f"{res['book_title']} - {res['user_email']}"):
                st.write(f"ISBN: {res['isbn']}")
                st.write(f"Date: {res['date']}")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Approve (Convert to Loan)", key=f"app_{res['isbn']}_{res['user_email']}"):
                        # 1. Create Loan
                        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                        if DataManager.add_loan(res['user_email'], res['isbn'], due_date):
                            # 2. Update Status to Fulfilled
                             ReservationManager.update_status(res['user_email'], res['isbn'], 'fulfilled')
                             st.success("Reservation approved and converted to loan.")
                             st.rerun()
                        else:
                            st.error("Could not create loan (maybe already borrowed?).")
                
                with c2:
                    if st.button("Cancel Reservation", key=f"cncl_{res['isbn']}_{res['user_email']}"):
                        ReservationManager.cancel_reservation(res['user_email'], res['isbn'])
                        st.warning("Reservation cancelled.")
                        st.rerun()
