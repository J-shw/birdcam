import os, time
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

# Set up the Google Photos API client
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/photoslibrary'])
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = google.auth.OAuth2FlowFromClientSecrets('client_secret.json', ['https://www.googleapis.com/auth/photoslibrary'])
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('photoslibrary', 'v1', credentials=creds)

# Upload an image to Google Photos
def upload(image):
    try:
        upload_token = service.mediaItems().batchCreate(body={
            'albumId': 'your_album_id', # Replace with your album ID
            'newMediaItems': [{
                'description': 'your_image_description', # Replace with your image description
                'simpleMediaItem': {
                    'fileName': 'your_image_filename', # Replace with your image filename
                    'uploadToken': 'your_image_upload_token' # Replace with your image upload token
                }
            }]
        }).execute()
        print(f"Uploaded image: {upload_token['newMediaItemResults'][0]['mediaItem']['filename']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

while True:
    upload("image.jpg")
    time.sleep(1)