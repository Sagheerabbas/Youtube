
from flask import Flask, render_template, request, send_file, jsonify
from yt_dlp import YoutubeDL
import os, uuid, threading, re, json
from datetime import datetime

app = Flask(__name__)
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(os.getcwd(), "history.json")
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

progress_status = {}
lock = threading.Lock()

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T"]:
        if abs(num) < 1024.0:
            return f"{num:.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}P{suffix}"

def sanitize_title(title):
    return re.sub(r'[\\/*?:"<>|]', "_", title)

def log_download(info):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    history.insert(0, info)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[:100], f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preview", methods=["POST"])
def preview():
    url = request.form["url"]
    if not url.startswith("http"):
        return "Invalid URL", 400

    ydl_opts = {'quiet': True, 'skip_download': True}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        return f"Error retrieving video: {str(e)}", 400

    formats = []
    for f in info['formats']:
        if f.get("filesize"):
            formats.append({
                "format_id": f["format_id"],
                "ext": f["ext"],
                "resolution": f.get("format_note") or f.get("height", "") or "audio",
                "filesize": sizeof_fmt(f["filesize"])
            })

    # Add audio-only manually
    formats.append({"format_id": "bestaudio", "ext": "mp3", "resolution": "Audio Only", "filesize": "Varies"})

    return render_template("preview.html", url=url, title=info.get("title"),
                           thumbnail_url=info.get("thumbnail"),
                           duration=info.get("duration_string", ""), formats=formats)

def download_video(task_id, url, format_id, title):
    safe_title = sanitize_title(title)
    out_file = os.path.join(DOWNLOAD_DIR, f"{safe_title}_{task_id}.%(ext)s")
    with lock:
        progress_status[task_id] = "Downloading..."

    is_audio = format_id == "bestaudio"

    ydl_opts = {
        'format': format_id if is_audio else f"{format_id}+bestaudio/best",
        'outtmpl': out_file,
        'merge_output_format': 'mp3' if is_audio else 'mp4',
        'quiet': True,
        'noplaylist': True
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            filename = ydl.prepare_filename(info)
        with lock:
            progress_status[task_id] = "done"
        log_download({
            "title": title,
            "filename": os.path.basename(filename),
            "url": url,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        with lock:
            progress_status[task_id] = f"error: {e}"

@app.route("/start-download", methods=["POST"])
def start_download():
    url = request.form.get("url")
    title = request.form.get("title")
    format_id = request.form.get("format_id")
    if not format_id or not url or not title:
        return "Missing parameters", 400

    task_id = str(uuid.uuid4())
    threading.Thread(target=download_video, args=(task_id, url, format_id, title)).start()
    return jsonify({"task_id": task_id})

@app.route("/progress/<task_id>")
def progress(task_id):
    with lock:
        status = progress_status.get(task_id, "starting")
    if status == "done":
        filename = [f for f in os.listdir(DOWNLOAD_DIR) if task_id in f][0]
        return jsonify({"status": "done", "url": f"/download/{filename}"})
    elif status.startswith("error"):
        return jsonify({"status": "error", "message": status})
    else:
        return jsonify({"status": status})

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(DOWNLOAD_DIR, filename), as_attachment=True)

@app.route("/history")
def history():
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
    return render_template("history.html", history=data)

if __name__ == '__main__':
    app.run(debug=True)
