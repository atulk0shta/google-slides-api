import logging
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from src.constants.en import LogMessage
from src.constants.main import ROOT_DIR
from src.constants.main import Google
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger()


def get_service():
    creds = None
    token_file = os.path.join(ROOT_DIR, Google.TOKEN)
    credentials_path = os.path.join(ROOT_DIR, 'src', 'configs', Google.OAUTH_CLIENT_SECRET)
    scopes = ['https://www.googleapis.com/auth/presentations']

    if token_file and os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, scopes=scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    service = build('slides', 'v1', credentials=creds)

    logger.debug("Service object created")

    return service


def get_or_create_presentation(service, presentation_id=None, title=None):
    # Retrieve a list of presentations
    if not presentation_id:
        if not title:
            return

        logger.debug(LogMessage.SHEET_CREATION_ATTEMPT.format(title))
        presentation_body = {'title': title}

        presentation = service.presentations().create(body=presentation_body).execute()
        logger.info(LogMessage.SHEET_CREATED.format(presentation['presentationId']))
    else:
        try:
            presentation = service.presentations().get(
                presentationId=presentation_id
            ).execute()

            logger.debug(LogMessage.SHEET_ALREADY_EXISTS.format(presentation_id))
        except HttpError as e:
            if e.resp.status == 404:
                logger.error(LogMessage.SHEET_NOT_FOUND.format(presentation_id))
                return
            else:
                raise

    return presentation


google_service = get_service()
prs = get_or_create_presentation(google_service, presentation_id='')

print(dir(prs))
