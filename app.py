import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from pathlib import Path
import importlib
import os
from utils.helpers import load_json, save_json

# Page config
st.set_page_config(
    page_title="Brain4 Enterprise",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication
def init_auth():
    if not os.path.exists('data/users.json'):
        # Create default admin user if no users exist
        default_config = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'email': 'admin@brain4.ai',
                        'name': 'Admin User',
                        'password': stauth.Hasher(['admin']).generate()[0]
                    }
                }
            },
            'cookie': {
                'name': 'brain4_auth',
                'key': 'brain4_auth_key',
                'expiry_days': 30
            }
        }
        save_json('data/users.json', default_config)
    
    with open('data/users.json') as file:
        config = load_json('data/users.json')
    
    authenticator = stauth.Authenticator(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    return authenticator

def main():
    try:
        # Initialize required directories
        for dir_path in ['data/uploads', 'data/legal', 'data/ocr']:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
        authenticator = init_auth()
        
        # Place authentication in a container for better styling
        with st.container():
            name, authentication_status, username = authenticator.login("Login", "main")

            if authentication_status == False:
                st.error("Invalid credentials")
                return
            elif authentication_status == None:
                st.warning("Please enter your credentials")
                return

        # User is authenticated
        with st.sidebar:
            authenticator.logout("Logout", "sidebar")
            st.write(f"Welcome {name}")

            # Navigation
            selected = st.radio(
                "Navigation",
                ["Dashboard", "Car Insurance", "Legal", "OCR", "Alerts"]
            )

        # Route to appropriate module
        try:
            if selected == "Dashboard":
                from pages.car.dashboard import show_dashboard
                show_dashboard()
            elif selected == "Car Insurance":
                from pages.car.ai import show as show_car
                show_car()
            elif selected == "Legal":
                from pages.legal.ai import show as show_legal
                show_legal()
            elif selected == "OCR":
                from pages.ocr.ocr_ai import show as show_ocr
                show_ocr()
            elif selected == "Alerts":
                from pages.alerts.live import show as show_alerts
                show_alerts()
        except Exception as e:
            st.error(f"Error loading module: {str(e)}")
            st.error("Please check if all required packages are installed")

    except Exception as e:
        st.error(f"System error: {str(e)}")
        if os.environ.get('DEBUG'):
            import traceback
            st.error(traceback.format_exc())

if __name__ == "__main__":
    main()
