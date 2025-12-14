import streamlit as st
from utils.data_manager import DataManager
from utils.reservation_manager import ReservationManager
from datetime import datetime, timedelta

def render_search(user, books_manager):
    st.header("Search & Borrow")
    st.markdown("Search for books by title, author, or ISBN.")
    
    query = st.text_input("Search", placeholder="e.g. Harry Potter", label_visibility="collapsed")
    st.divider()

    if query:
        results = books_manager.search_books(query)
        st.write(f"Found {len(results)} books.")
        
        for book in results:
            with st.container():
                # Card Styling - High Contrast
                st.markdown("""
                <div style="background-color: rgba(255, 255, 255, 0.85); backdrop-filter: blur(15px); padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid rgba(141, 110, 99, 0.3); box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 4, 3])
                
                with col1:
                     st.markdown("<div style='font-size: 40px; text-align: center;'>📖</div>", unsafe_allow_html=True) 
                
                with col2:
                    st.subheader(book.title)
                    st.markdown(f"<span style='color: #6D4C41; font-size: 0.9em;'>Author: {book.title} | ISBN: {book.isbn} | Year: {book.year}</span>", unsafe_allow_html=True)
                    
                    # Status Badge
                    if book.available_quantity > 0:
                        st.markdown(f"<span style='color:#2E7D32; font-weight:bold; background-color: rgba(46, 125, 50, 0.1); padding: 4px 8px; border-radius: 4px;'>Available: {book.available_quantity}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='color:#C62828; font-weight:bold; background-color: rgba(198, 40, 40, 0.1); padding: 4px 8px; border-radius: 4px;'>Unavailable</span>", unsafe_allow_html=True)
                        
                with col3:
                    # Borrow / Reserve Actions
                    if book.available_quantity > 0:
                         if st.button("Borrow", key=f"btn_bor_{book.isbn}", type="primary"):
                             success, msg = user.borrow_book(book)
                             if success:
                                 due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                                 DataManager.add_loan(user.email, book.isbn, due_date)
                                 st.toast(msg, icon="✅")
                                 st.rerun()
                             else:
                                 st.error(msg)
                    else:
                         user_res = ReservationManager.get_user_reservations(user.email, status='pending')
                         already_reserved = any(r['isbn'] == book.isbn for r in user_res)
                         
                         if already_reserved:
                             st.info("Reserved")
                         else:
                             if st.button("Reserve", key=f"btn_res_{book.isbn}"):
                                 success, msg = ReservationManager.create_reservation(user.email, book.isbn, book.title)
                                 if success:
                                     st.success("Reserved!")
                                     st.rerun()
                                 else:
                                     st.warning(msg)
                    
                    # Favorites Action
                    st.divider()
                    likes = DataManager.get_book_likes_count(book.isbn)
                    fav_list = user.get_favorites()
                    is_fav = book.isbn in fav_list
                    
                    c_h1, c_h2 = st.columns([1, 2])
                    with c_h1:
                        st.markdown(f"<div style='color:#C62828; font-weight:bold; padding-top:8px;'>❤ {likes}</div>", unsafe_allow_html=True)
                    with c_h2:
                        if is_fav:
                            if st.button("Unfavorite", key=f"unfav_{book.isbn}"):
                                user.remove_from_favorites(book)
                                st.rerun()
                        else:
                            if st.button("❤ Favorite", key=f"fav_{book.isbn}"):
                                user.add_to_favorites(book)
                                st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Start typing search terms above...")
