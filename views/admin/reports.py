import streamlit as st
from utils.data_manager import DataManager
import pandas as pd
import altair as alt

def render_admin_reports(books_manager, user_manager):
    st.header("Reports & Analytics")
    
    history = DataManager.load_history()
    
    # Flatten history
    flat_history = []
    for email, records in history.items():
        for r in records:
            flat_history.append(r)
            
    if not flat_history:
        st.info("No sufficient data for reports.")
        return
        
    df = pd.DataFrame(flat_history)
    
    # 1. Most Borrowed Books
    st.subheader("Top Borrowed Books")
    if 'title' in df.columns:
        top_books = df['title'].value_counts().reset_index()
        top_books.columns = ['Book Title', 'Count']
        
        chart = alt.Chart(top_books.head(10)).mark_bar().encode(
            x='Count',
            y=alt.Y('Book Title', sort='-x')
        ).properties(title="Top 10 Most Borrowed Books")
        
        st.altair_chart(chart, use_container_width=True)
    
    st.divider()
    
    # 2. Fines Collected
    st.subheader("Financial Overview")
    if 'fine' in df.columns:
        total_fines = df['fine'].sum()
        st.metric("Total Fines Collected", f"{total_fines} LE")
        
    st.divider()

    # 3. Active Members (Most Returns)
    st.subheader("Most Active Members")
    # This comes from history keys
    activity_counts = {email: len(recs) for email, recs in history.items()}
    active_df = pd.DataFrame(list(activity_counts.items()), columns=['User Email', 'Returns Count'])
    active_df = active_df.sort_values(by='Returns Count', ascending=False).head(10)
    st.dataframe(active_df, use_container_width=True)
