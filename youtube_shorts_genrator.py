import streamlit as st
from pytube import YouTube
import ffmpeg
import os

# Function to download YouTube video temporarily
def download_video(youtube_url, download_path="downloads"):
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    file_path = stream.download(output_path=download_path)
    return file_path

# Function to create short videos using ffmpeg
def create_shorts(video_path, timestamps, add_caption, caption_texts):
    output_paths = []
    for i, (start, end) in enumerate(timestamps):
        output_file = f"output_short_{i + 1}.mp4"
        # Trim video using ffmpeg
        trim_cmd = (
            ffmpeg.input(video_path, ss=start, to=end)
            .filter("crop", "ih*9/16", "ih")  # Crop to 9:16 aspect ratio
        )
        
        if add_caption:
            caption_text = caption_texts[i] if i < len(caption_texts) else "Highlight"
            trim_cmd = trim_cmd.filter("drawtext", text=caption_text, fontsize=24, fontcolor="white", x="(w-text_w)/2", y="h-text_h-10")
        
        # Running the ffmpeg command to create the short video
        (
            trim_cmd
            .output(output_file, vcodec="libx264", acodec="aac", strict="-2")
            .run(overwrite_output=True)
        )
        output_paths.append(output_file)
    
    return output_paths

# Streamlit UI
st.title("Video Shorts Generator")
st.sidebar.header("Input Options")

# Input for YouTube URL
youtube_url = st.sidebar.text_input("Paste YouTube Video URL")
clip_length = st.sidebar.number_input("Length of each short video (seconds)", min_value=5, max_value=30, value=10)
add_caption = st.sidebar.checkbox("Add captions to shorts", value=True)

if add_caption:
    st.sidebar.text("Caption Examples")
    captions = st.sidebar.text_area("Enter captions (comma-separated for each short)", "Exciting Scene, Must Watch, Fun Moment, Highlight!")
else:
    captions = ""

# Preview the YouTube video before generating shorts
if youtube_url:
    yt = YouTube(youtube_url)
    st.video(youtube_url)  # Display the YouTube video preview

# Button to trigger short video generation
if st.sidebar.button("Generate Shorts"):
    if youtube_url.strip() == "":
        st.error("Please provide a valid YouTube URL!")
    else:
        st.info("Downloading video...")

        try:
            # Download video temporarily
            video_path = download_video(youtube_url)
            st.success("Video downloaded successfully!")

            # Process the video and create shorts
            timestamps = [(i, i + clip_length) for i in range(0, clip_length * 4, clip_length)]
            caption_texts = captions.split(",") if add_caption else []
            output_paths = create_shorts(video_path, timestamps, add_caption, caption_texts)
            
            st.success("Short videos generated successfully!")

            # Display generated short videos
            st.info("Generated Short Videos:")
            for i, path in enumerate(output_paths):
                st.video(path)
                
            st.success("Short videos are ready to share!")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Reset button to clear any generated files
if st.sidebar.button("Reset"):
    if os.path.exists("downloads"):
        for file in os.listdir("downloads"):
            os.remove(os.path.join("downloads", file))
        st.info("Reset complete. All files cleared!")

# Footer message for instructions
st.text("By Daksh")
