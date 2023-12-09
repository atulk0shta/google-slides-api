import logging
import time
from time import sleep
from src.constants.main import Presentation, Properties
from src.services.google_slides_api_service import GoogleSlidesApiService

logger = logging.getLogger()
google_service = GoogleSlidesApiService.get_service()

# presentation = GoogleSlidesApiService.get_or_create_presentation(google_service, title="TRGT DIGITAL")
presentation_id = '1VeNAHWYvoouKi16A5lIw-smoJ4w1vBoIThILdOJAZ50'

# Create Slide
page_id = Presentation.SLIDE_ID_PREFIX + str(int(time.time()))
create_slide_response = GoogleSlidesApiService.create_slide(google_service, presentation_id, page_id)
logger.info(create_slide_response)

# Create Title Textbox in Slide
title_element_id = Presentation.ELEMENT_ID_PREFIX + str(int(time.time()))
create_title_response = GoogleSlidesApiService.create_textbox_with_text(google_service, presentation_id, page_id,
                                                                        title_element_id,
                                                                        Properties.TITLE_PROPERTIES, title=True)
logger.info(create_title_response)

# Sample data - bullet points
bullet_points = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do',
                 'eiusmod tempor incididunt ut labore et dolore magna aliqua',
                 'enim ad minim veniam, quis nostrud exercitation ullamco laboris']

# Create Body Textbox in Slide
body_textbox_properties = Properties.BODY_PROPERTIES
body_textbox_properties['text'] = '\n'.join([f'\u2022 {point}' for point in bullet_points])
body_element_id = Presentation.ELEMENT_ID_PREFIX + str(int(time.time()))
create_body_response = GoogleSlidesApiService.create_textbox_with_text(google_service, presentation_id, page_id,
                                                                       body_element_id,
                                                                       body_textbox_properties)
logger.info(create_body_response)
