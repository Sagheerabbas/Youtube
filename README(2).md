# YouTube Video Downloader

A simple Flask web application for previewing and downloading YouTube videos using `yt-dlp`. Users can paste a YouTube URL, preview the video details, choose an available format, start the download, and view recent download history from the browser.

> Important: This project is for educational and personal use only. Download only content you own, content in the public domain, or content you have permission to download. Always follow YouTube's terms and copyright rules.

## Features

- Paste a YouTube video URL and preview video details
- Show video title, thumbnail, duration, format, resolution, and file size
- Download videos in available formats supported by `yt-dlp`
- Audio-only download option
- Background download processing with task IDs
- Live download status using progress polling
- Download history saved in `history.json`
- Clean responsive UI using HTML, CSS, and Flask templates
- Local download storage inside the `downloads` folder

## Tech Stack

- Python
- Flask
- yt-dlp
- HTML5
- CSS3
- JavaScript
- JSON
- FFmpeg, recommended for video and audio merging

## Project Structure

```text
Youtube Downloader Final/
├── app.py
├── history.json
├── downloads/
├── static/
│   └── style.css
└── templates/
    ├── index.html
    ├── preview.html
    └── history.html
```

## Requirements

Make sure you have the following installed:

- Python 3.9 or higher
- pip
- FFmpeg, recommended because many YouTube formats need merging or audio processing

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/youtube-video-downloader.git
cd youtube-video-downloader
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

For Windows:

```bash
venv\Scripts\activate
```

For macOS or Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install flask yt-dlp
```

Or create a `requirements.txt` file with:

```text
Flask
yt-dlp
```

Then install using:

```bash
pip install -r requirements.txt
```

## FFmpeg Setup

FFmpeg is strongly recommended for proper video merging and audio handling.

Check if FFmpeg is installed:

```bash
ffmpeg -version
```

If the command is not found, install FFmpeg and add it to your system PATH.

## Run the App

Start the Flask development server:

```bash
python app.py
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

## How to Use

1. Open the home page.
2. Paste a YouTube video URL.
3. Click `Preview`.
4. Select the format or audio-only option.
5. Click `Download`.
6. Wait until the download is ready.
7. The file will download automatically.
8. Open the history page to view recent downloads.

## Main Routes

| Route | Method | Description |
|---|---:|---|
| `/` | GET | Shows the home page |
| `/preview` | POST | Fetches video information and available formats |
| `/start-download` | POST | Starts a background download task |
| `/progress/<task_id>` | GET | Checks download progress |
| `/download/<filename>` | GET | Downloads the completed file |
| `/history` | GET | Shows recent download history |

## Download History

The app stores recent downloads in `history.json`. It keeps the latest 100 records, including:

- Video title
- Downloaded filename
- Original URL
- Download timestamp

For public GitHub repositories, avoid committing personal download history. You can reset `history.json` to:

```json
[]
```

## Recommended `.gitignore`

Before pushing to GitHub, add this `.gitignore` file:

```gitignore
venv/
__pycache__/
*.pyc
.env
.DS_Store
Thumbs.db
downloads/*
!downloads/.gitkeep
history.json
```

If you want to keep the `downloads` folder in GitHub, create an empty file:

```bash
touch downloads/.gitkeep
```

## Notes

- The app runs locally by default.
- Files are saved in the `downloads` folder.
- Some YouTube formats may require FFmpeg to merge video and audio.
- Audio-only downloads depend on the available source format and local FFmpeg setup.
- Do not use Flask debug mode in production.

## Possible Improvements

- Add a real progress percentage using `yt-dlp` progress hooks
- Add URL validation for YouTube links only
- Add error handling when no downloadable formats are available
- Add automatic cleanup for old downloaded files
- Add user authentication before exposing downloads publicly
- Add proper MP3 conversion using `yt-dlp` postprocessors
- Add Docker support
- Add tests for route validation and utility functions

## Production Reminder

This app is currently built for local development. If you deploy it online, make sure to:

- Disable debug mode
- Add authentication
- Limit download size and request frequency
- Protect the downloads directory
- Clean old files automatically
- Follow copyright and platform rules


