import streamlit as st

def render_admin_members(user_manager):
    st.header("Members Management")
    
    st.subheader("All Members")
    
    members_data = []
    for u in user_manager.users:
        members_data.append({
            "ID": u.user_id,
            "Name": u.name,
            "Email": u.email,
            "Role": u.role,
            "Age": u.age
        })
        
    st.dataframe(members_data, use_container_width=True)
    
    st.divider()
    st.subheader("Manage Member")
    
    member_emails = [u.email for u in user_manager.users]
    selected_email = st.selectbox("Select Member to Manage:", ["Select..."] + member_emails)
    
    if selected_email != "Select...":
        user = next((u for u in user_manager.users if u.email == selected_email), None)
        if user:
            st.write(f"**Selected:** {user.name} ({user.role})")
            
            if st.button("Remove Member", type="primary"):
                # Safety check
                if user.role == "librarian" and len([u for u in user_manager.users if u.role == 'librarian']) <= 1:
                     st.error("Cannot remove the last manager.")
                else:
                    user_manager.users.remove(user)
                    user_manager.save_users()
                    st.success(f"User {user.email} removed.")
                    st.rerun()
