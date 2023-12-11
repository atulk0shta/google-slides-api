Instructions:

1. Store google oauth2 client_secret inside src/configs
2. Configure your project root directory path and 'client secret JSON file name(in Google class)' in
   src/constants/main.py
3. Pass either 'existing presentation id' or 'title and subtitle of new presentation to be created' while calling
   get_or_create_presentation method in src/main.py
4. To add slide with specific layout, add specific method in src/services/google_slides_api_service.py

References:  
[Google Requests](https://developers.google.com/slides/api/reference/rest/v1/presentations/request)  
[Create and manage presentations](https://developers.google.com/slides/api/guides/presentations)