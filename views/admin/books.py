import streamlit as st
from book import Book

def render_admin_books(books_manager):
    st.header("Books Management")
    
    tab1, tab2 = st.tabs(["List & Edit", "Add New Book"])
    
    with tab1:
        st.subheader("Library Catalog")
        all_books = books_manager.list_books()
        
        # Convert to DataFrame for easier display
        data = []
        for b in all_books:
            data.append({
                "ISBN": b.isbn,
                "Title": b.title,
                "Author": b.author,
                "Year": b.year,
                "Qty": b.total_quantity,
                "Available": b.available_quantity
            })
        
        if not data:
            st.info("No books in library.")
        else:
            # We want actions. Streamlit dataframe editing is limited. 
            # Let's use expanders for editing each book or a selector.
            
            # Selector for editing
            book_titles = [f"{b['Title']} ({b['ISBN']})" for b in data]
            selected_option = st.selectbox("Select a book to edit/delete:", ["Select..."] + book_titles)
            
            if selected_option != "Select...":
                isbn_selected = selected_option.split("(")[-1].replace(")", "")
                book_obj = books_manager.get_book(isbn_selected)
                
                if book_obj:
                    with st.expander("Edit Book Details", expanded=True):
                        with st.form(key=f"edit_{book_obj.isbn}"):
                            new_title = st.text_input("Title", book_obj.title)
                            new_author = st.text_input("Author", book_obj.author)
                            new_year = st.text_input("Year", book_obj.year)
                            new_pub = st.text_input("Publisher", book_obj.publisher)
                            new_qty = st.number_input("Total Quantity", min_value=0, value=book_obj.total_quantity)
                            
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.form_submit_button("Update Book"):
                                    book_obj.title = new_title
                                    book_obj.author = new_author
                                    book_obj.year = new_year
                                    book_obj.publisher = new_pub
                                    # Adjusting quantity logic might be complex if available > total.
                                    # For simplicity, we update total, and adjust available by the diff.
                                    diff = new_qty - book_obj.total_quantity
                                    book_obj.total_quantity = new_qty
                                    book_obj.available_quantity += diff
                                    
                                    books_manager.save_books()
                                    st.success("Updated successfully!")
                                    st.rerun()
                            
                            with c2:
                                if st.form_submit_button("Delete Book", type="primary"):
                                    # Verify no active loans? 
                                    # For now, force delete.
                                    if book_obj.isbn in books_manager.books:
                                        del books_manager.books[book_obj.isbn]
                                        books_manager.save_books()
                                        st.warning("Book Deleted.")
                                        st.rerun()

            st.dataframe(data, use_container_width=True)

    with tab2:
        st.subheader("Add New Book")
        with st.form("add_book_admin"):
            isbn = st.text_input("ISBN")
            title = st.text_input("Title")
            author = st.text_input("Author")
            year = st.text_input("Year")
            publisher = st.text_input("Publisher")
            qty = st.number_input("Quantity", min_value=1, value=5)
            
            if st.form_submit_button("Add Book"):
                if isbn in books_manager.books:
                    st.error("Book with this ISBN already exists.")
                else:
                    new_book = Book(isbn, title, author, year, publisher, qty)
                    books_manager.add_book(new_book)
                    st.success(f"Book '{title}' added!")
