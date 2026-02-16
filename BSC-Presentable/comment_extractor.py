from googleapiclient.discovery import build

API_KEY="AIzaSyDRVrWzAUh1ZnSyme344Dvwib8UB50YkEU"

from googleapiclient.discovery import build

youtube = build("youtube", "v3", developerKey=API_KEY)

request = youtube.commentThreads().list(
    part="snippet",
    videoId="yta_B6tq2VQ",
    maxResults=10,
    textFormat="plainText"
)

response = request.execute()

for item in response["items"]:
    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
    print(comment)
