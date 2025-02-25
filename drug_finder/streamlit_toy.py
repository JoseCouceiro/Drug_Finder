import streamlit as st

# Initialize session state variables
if 'dynamic_buttons' not in st.session_state:
    st.session_state.dynamic_buttons = {}  # Dictionary to store button states

# Function to create dynamic buttons
def create_dynamic_button(button_key, label):
    if button_key not in st.session_state.dynamic_buttons:
        st.session_state.dynamic_buttons[button_key] = False  # Initialize button state
    
    # Create the button
    if st.button(label, key=button_key):
        st.session_state.dynamic_buttons[button_key] = True  # Update button state on click

# Initial button to trigger deployment of dynamic buttons
if st.button("Deploy Dynamic Buttons"):
    st.write("Dynamic buttons will now be deployed.")

# Deploy dynamic buttons conditionally
if st.session_state.get('dynamic_buttons_deployed', False):  # Check if deployment flag is set
    create_dynamic_button("button_1", "Button 1")
    create_dynamic_button("button_2", "Button 2")

    # Check if specific buttons were clicked
    if st.session_state.dynamic_buttons.get("button_1", False):
        st.write("Button 1 was clicked!")
        # Perform actions for Button 1
        # e.g., self.__searcher.search_motor_sing(__activep['nombre'])

    if st.session_state.dynamic_buttons.get("button_2", False):
        st.write("Button 2 was clicked!")
        # Perform actions for Button 2
        # e.g., self.__retrieve_compound_data(1)

# Set deployment flag
if st.button("Enable Dynamic Buttons"):
    st.session_state.dynamic_buttons_deployed = True
