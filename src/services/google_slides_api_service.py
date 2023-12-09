# ref: https://developers.google.com/slides/api/reference/rest/v1/presentations/request#LayoutReference
import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.constants.en import LogMessage
from src.constants.main import ROOT_DIR, Google

logger = logging.getLogger()


class GoogleSlidesApiService:
    @staticmethod
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

    @staticmethod
    def get_or_create_presentation(service, pid=None, title=None, subtitle=None):
        # Retrieve a list of presentations
        if not pid:
            if not (title and subtitle):
                logger.warning(LogMessage.TITLE_AND_SUBTITLE_REQUIRED)
                return

            logger.debug(LogMessage.SHEET_CREATION_ATTEMPT.format(title))
            presentation_body = {'title': title}

            presentation = service.presentations().create(body=presentation_body).execute()
            logger.info(LogMessage.SHEET_CREATED.format(presentation['presentationId']))

            add_title_and_subtitle_response = GoogleSlidesApiService.add_title_and_subtitle(service, presentation,
                                                                                            title,
                                                                                            subtitle)
            logger.info(add_title_and_subtitle_response)
        else:
            try:
                presentation = service.presentations().get(
                    presentationId=pid
                ).execute()

                logger.debug(LogMessage.SHEET_ALREADY_EXISTS.format(pid))
            except HttpError as e:
                if e.resp.status == 404:
                    logger.error(LogMessage.SHEET_NOT_FOUND.format(pid))
                    return
                else:
                    raise

        return presentation

    @staticmethod
    def add_title_and_subtitle(service, presentation, title, subtitle):
        pid = presentation['presentationId']
        slide_0 = presentation['slides'][0]
        slide_0_id = slide_0['objectId']
        title_id = slide_0['pageElements'][0]['objectId']
        subtitle_id = slide_0['pageElements'][1]['objectId']

        logger.debug(f'Slide 0 ID: {slide_0_id}')
        logger.debug(f'Title ID: {title_id}')
        logger.debug(f'Subtitle ID: {subtitle_id}')

        try:
            requests = [
                {
                    "insertText": {
                        "objectId": title_id,
                        "text": title,
                    }
                },
                {
                    "insertText": {
                        "objectId": subtitle_id,
                        "text": subtitle,
                    }
                }
            ]

            body = {"requests": requests}
            response = (
                service.presentations()
                .batchUpdate(presentationId=pid, body=body)
                .execute()
            )

            return response
        except HttpError as error:
            logger.error(f"An error occurred: {error}")

            return error

    @staticmethod
    def create_slide(service, pid, page_id):
        try:
            requests = [
                {
                    "createSlide": {
                        "objectId": page_id,
                        "insertionIndex": "1",
                        "slideLayoutReference": {
                            "predefinedLayout": "BLANK"
                        },
                    }
                }
            ]

            # If you wish to populate the slide with elements,
            # add element create requests here, using the page_id.

            # Execute the request.
            body = {"requests": requests}
            response = (
                service.presentations()
                .batchUpdate(presentationId=pid, body=body)
                .execute()
            )
            create_slide_response = response.get("replies")[0].get("createSlide")
            logger.info(f"Created slide with ID:{(create_slide_response.get('objectId'))}")
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            logger.error("Slides not created")
            return error

        return response

    @staticmethod
    def create_textbox_with_text(service, pid, page_id, element_id, properties, title=False):
        height = {'magnitude': properties['height_magnitude'], 'unit': 'PT'}
        width = {'magnitude': properties['width_magnitude'], 'unit': 'PT'}
        translateX = properties['translateX']
        translateY = properties['translateY']
        text = properties['text']

        requests = [
            {
                "createShape": {
                    "objectId": element_id,
                    "shapeType": "TEXT_BOX",
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {"height": height, "width": width},
                        "transform": {
                            "scaleX": 1,
                            "scaleY": 1,
                            "translateX": translateX,
                            "translateY": translateY,
                            "unit": "PT",
                        },
                    },
                }
            },
            # Insert text into the box, using the supplied element ID.
            {
                "insertText": {
                    "objectId": element_id,
                    # "insertionIndex": 0,
                    "text": text,
                }
            },
        ]

        if title:
            requests.append({
                "updateParagraphStyle": {
                    "objectId": element_id,
                    "style": {
                        "alignment": 'CENTER',
                        "direction": 'LEFT_TO_RIGHT',
                        "spaceAbove": {
                            "magnitude": 5,
                            "unit": 'PT'
                        }
                    },
                    "fields": "*"
                }
            })

        try:
            # Execute the request.
            body = {"requests": requests}
            response = (
                service.presentations()
                .batchUpdate(presentationId=pid, body=body)
                .execute()
            )
            create_shape_response = response.get("replies")[0].get("createShape")
        except HttpError as error:
            logger.error(f"An error occurred: {error}")

            return error

        return response
