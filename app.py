import streamlit as st
from datetime import datetime
import os

# Deployment instructions:
# Save this file as streamlit_app.py and run:
#   streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 80
# Ensure your server's firewall allows incoming traffic on port 80 or your chosen port.

# Limit uploads to 10 MB
# st.set_option('server.maxUploadSize', 10)

st.title("Photo Upload App")

# Input fields
name = st.text_input("Name")
uploaded_file = st.file_uploader(
    "Photo", type=["jpg", "jpeg", "png", "gif"], help="Max file size 10 MB"
)

if st.button("Upload"):
    if not name:
        st.error("Please enter your name.")
    elif not uploaded_file:
        st.error("Please select an image to upload.")
    else:
        # Check file size
        uploaded_file.seek(0, os.SEEK_END)
        file_size = uploaded_file.tell()
        uploaded_file.seek(0)
        if file_size > 10 * 1024 * 1024:
            st.error("File size exceeds 10 MB limit.")
        else:
            # Create directory for today's date
            date_str = datetime.now().strftime("%Y-%m-%d")
            save_dir = os.path.join("uploads", date_str)
            os.makedirs(save_dir, exist_ok=True)

            # Construct filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            _, ext = os.path.splitext(uploaded_file.name)
            filename = f"{name}_{timestamp}{ext}"
            save_path = os.path.join(save_dir, filename)

            # Write file to disk
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"Image saved as `{filename}` in `{save_dir}`.")
