import streamlit as st
import pandas as pd

def render_dashboard(user, books_manager, user_manager):
    st.header("Dashboard")
    st.markdown(f"Welcome back, **{user.name}**!")
    st.divider()

    if user.role == 'librarian':
        # Manager Stats
        col1, col2, col3 = st.columns(3)
        with col1:
             st.metric("Total Books", len(books_manager.books))
        with col2:
             st.metric("Total Members", len(user_manager.users))
        with col3:
             # Basic pie chart replacement
             st.metric("System Health", "100%")
             
    else:
        # User Stats
        from utils.data_manager import DataManager
        active_loans = len(DataManager.get_user_loans(user.email))
        history_count = len(DataManager.get_user_history(user.email))
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.85); backdrop-filter: blur(15px); padding: 25px; border-radius: 12px; border: 1px solid rgba(141, 110, 99, 0.3); box-shadow: 0 6px 15px rgba(62, 39, 35, 0.1);">
                <h4 style="color: #6D4C41; margin:0; font-family:'Poppins', sans-serif; font-weight: 500;">Books Borrowed</h4>
                <h1 style="color: #3E2723; margin:10px 0 0 0; font-family:'Playfair Display', serif; font-size: 3rem;">{}</h1>
            </div>
            """.format(active_loans), unsafe_allow_html=True)
            
        with col2:
             st.markdown("""
            <div style="background-color: rgba(255, 255, 255, 0.85); backdrop-filter: blur(15px); padding: 25px; border-radius: 12px; border: 1px solid rgba(141, 110, 99, 0.3); box-shadow: 0 6px 15px rgba(62, 39, 35, 0.1);">
                <h4 style="color: #6D4C41; margin:0; font-family:'Poppins', sans-serif; font-weight: 500;">Reading History</h4>
                <h1 style="color: #3E2723; margin:10px 0 0 0; font-family:'Playfair Display', serif; font-size: 3rem;">{}</h1>
            </div>
            """.format(history_count), unsafe_allow_html=True)

        st.divider()
        st.subheader("❤ My Favorite Books")
        
        fav_isbns = user.get_favorites()
        if fav_isbns:
            from utils.data_manager import DataManager
            
            for isbn in fav_isbns:
                book = books_manager.get_book(isbn)
                if book:
                    with st.expander(f"{book.title} ({book.author})"):
                        likes = DataManager.get_book_likes_count(isbn)
                        st.caption(f"Total Likes: {likes}")
                        if st.button("Remove from Favorites", key=f"rm_fav_{isbn}"):
                            user.remove_from_favorites(book)
                            st.success(f"Removed '{book.title}'")
                            st.rerun()
        else:
            st.info("You haven't favorited any books yet.")
