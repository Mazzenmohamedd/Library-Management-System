import streamlit as st
from utils.reservation_manager import ReservationManager

def render_reservations(user):
    st.header("My Reservations")
    
    res_list = ReservationManager.get_user_reservations(user.email)
    
    if not res_list:
        st.info("You have no reservations.")
        return

    for res in res_list:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{res.get('book_title', 'Book')}** (ISBN: {res['isbn']})")
                st.caption(f"Status: {res['status']} | Date: {res['date']}")
            with col2:
                if res['status'] == 'pending':
                    if st.button("Cancel", key=f"can_res_{res['isbn']}_{res['date']}"):
                        ReservationManager.cancel_reservation(user.email, res['isbn'])
                        st.rerun()
            st.divider()
