import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
PRIVACY = os.getenv("YT_PRIVACY_STATUS", "private") # change to public later

creds = Credentials(None, refresh_token=REFRESH_TOKEN, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
youtube = build("youtube", "v3", credentials=creds)

with open("title.txt","r", encoding="utf-8") as f:
    title = f.read().strip()[:95]

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {"title": title, "description": f"{title}\n\n#gaming #gta5 #bgmi", "categoryId": "20"},
        "status": {"privacyStatus": PRIVACY, "selfDeclaredMadeForKids": False}
    },
    media_body=MediaFileUpload("final_video.mp4", chunksize=-1, resumable=True)
)
res = request.execute()
print(f"Uploaded video ID: {res['id']}")

# thumbnail
if os.path.exists("thumbnail.png"):
    youtube.thumbnails().set(videoId=res['id'], media_body=MediaFileUpload("thumbnail.png", mimetype="image/png")).execute()
    print("Thumbnail uploaded")
