from flask import Flask, request, jsonify, send_from_directory
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

# Read API key from environment variable
API_KEY = "AIzaSyDRVrWzAUh1ZnSyme344Dvwib8UB50YkEU"
if not API_KEY:
    raise RuntimeError("Set the YOUTUBE_API_KEY environment variable to your YouTube Data API key")

# Create YouTube API client once (reuse it)
youtube = build("youtube", "v3", developerKey=API_KEY)

app = Flask(__name__, static_folder='.')

@app.route("/")
def index():
    # Serve index.html from this directory
    return send_from_directory(app.static_folder, "index.html")

@app.get("/comments")
def comments():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify(error="Missing videoId"), 400

    comments = []
    next_page_token = None
    
    while True:
        try:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                pageToken=next_page_token,
                maxResults=50,  
                textFormat='plainText'
            ).execute()
        except HttpError as e:
            return jsonify(error="YouTube API error", details=str(e)), 500

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'like_count': comment['likeCount'],
                'published_at': comment['publishedAt']
            })
            print(f"Added comment from {comment['authorDisplayName']}")
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return jsonify(
        videoId = video_id,
        commentCount=len(comments),
        comments=comments
    )

if __name__ == "__main__":
    app.run(debug=True)