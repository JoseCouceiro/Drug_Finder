import streamlit as st

# Sample data: key is a number, value is a dictionary with details
data = {
    1: {"name": "Paracetamol", "dose": "500mg", "form": "Tablet", "info": "Used for pain and fever"},
    2: {"name": "Ibuprofen", "dose": "400mg", "form": "Capsule", "info": "Used for inflammation and pain"},
    3: {"name": "Aspirin", "dose": "325mg", "form": "Tablet", "info": "Used for blood thinning and pain relief"},
}

# Initialize session state for tracking selected button
if "selected_key" not in st.session_state:
    st.session_state.selected_key = None

st.title("Medicine Information")

# Create buttons for each key
for key in data:
    if st.button(f"Show details for {data[key]['name']}"):
        st.session_state.selected_key = key  # Store selected key in session state

# Display information when a button is clicked
if st.session_state.selected_key is not None:
    key = st.session_state.selected_key
    st.write(f"### {data[key]['name']}")
    st.write(f"**Dose:** {data[key]['dose']}")
    st.write(f"**Form:** {data[key]['form']}")
    st.write(f"**Info:** {data[key]['info']}")

    # Button to reset selection
    if st.button("Go back"):
        st.session_state.selected_key = None

