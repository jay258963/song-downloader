import streamlit as st
import yt_dlp
import os
from PIL import Image
import base64

# Set page title and icon
st.set_page_config(page_title="YouTube to MP3 Converter", page_icon=":musical_note:")

# Load background image (if available)
try:
    with open("img.jpg", "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded_image}");
                background-size: cover;
            }}
        </style>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    pass  # Skip background image if not found

# Custom CSS to style the page
st.markdown("""
    <style>
        .container {
            background-color: rgba(255, 255, 255, 0); /* Fully transparent background */
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 50px;
        }
        .title {
            font-size: 40px;
            font-weight: bold;
            color: white; /* Set text color to white */
            text-align: center;
            margin-bottom: 20px;
        }
        .description {
            font-size: 18px;
            color: white; /* Set text color to white */
            text-align: center;
            margin-bottom: 30px;
        }
        .input-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .input-field {
            padding: 12px;
            border-radius: 5px;
            border: 1px solid #ccc;
            width: 400px;
            font-size: 18px;
            background-color: rgba(255, 255, 255, 0.8); /* Add background to input field */
            border: 2px solid #ccc; /* Add border to input field */
        }
        .convert-button {
            background-color: #FF9800; /* Initial button color: Orange */
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Display the title and description
st.markdown(f"""
    <div class="container">
        <h1 class="title">YouTube to MP3 Converter</h1>
        <p class="description">Convert your favorite YouTube videos to high-quality MP3 audio files in just a few clicks!</p>
    </div>
""", unsafe_allow_html=True)

# User input for YouTube URL
youtube_url = st.text_input("Enter YouTube video link:")

def download_audio(youtube_url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': r"C:\Users\mogud\OneDrive\Desktop\yt download\ffmpeg-7.1-essentials_build\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe",  # Set the ffmpeg path
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        return file_path, info_dict.get('title', 'Unknown Title')
    except Exception as e:
        return None, str(e)

if st.button("Convert & Download", key="convert", use_container_width=True):
    if youtube_url:
        with st.spinner("Downloading and converting..."):
            mp3_file, title = download_audio(youtube_url)
            if mp3_file:
                st.success(f"Conversion successful: {title}", icon="✅")
                with open(mp3_file, "rb") as file:
                    st.download_button(label="Download MP3", data=file, file_name=f"{title}.mp3", mime="audio/mpeg", key="download-btn", use_container_width=True)
                os.remove(mp3_file)  # Clean up after download
            else:
                st.error(f"Error: {title}", icon="❌")
    else:
        st.warning("Please enter a valid YouTube link.", icon="⚠️")

# Add some visual flair (optional)
st.balloons()  # Display balloons on successful conversion

# End of the app