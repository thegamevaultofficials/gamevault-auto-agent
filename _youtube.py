import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

VIDEO_FILE = "final_video.mp4"
TITLE_FILE = "title.txt"
DESC_FILE = "description.txt"

def get_youtube_service():
    client_id = os.environ["YT_CLIENT_ID"]
    client_secret = os.environ["YT_CLIENT_SECRET"]
    refresh_token = os.environ["YT_REFRESH_TOKEN"]
    
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)

def upload_video():
    youtube = get_youtube_service()
    
    with open(TITLE_FILE, "r", encoding="utf-8") as f:
        title = f.read().strip()[:95]
    try:
        with open(DESC_FILE, "r", encoding="utf-8") as f:
            description = f.read().strip()[:4000]
    except:
        description = title

    privacy = os.getenv("YT_PRIVACY_STATUS", "private")

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "20",
                "tags": ["gaming", "gamevault", "mobile gaming"]
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=VIDEO_FILE
    )
    response = request.execute()
    print(f"Uploaded! Video ID: {response['id']} https://youtu.be/{response['id']}")

if __name__ == "__main__":
    upload_video()
