import pickle
import os.path
from apiclient import errors
import email
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']


def search_message(service, user_id, search_string):
    """
    take the services from get_service()
    user_id : your gmail
    search_string : the search keyword
    returns a list containing email IDs of search query
    """
    try:
        # initiate the list for returning
        list_ids = []

        # get the id of all messages that are in the search string
        search_ids = service.users().messages().list(userId=user_id, q=search_string).execute()

        # if there were no results, print warning and return empty string
        try:
            ids = search_ids['messages']

        except KeyError:
            return ["Nothing found"]

        if len(ids)>1:
            for msg_id in ids:
                list_ids.append(msg_id['id'])
            return(list_ids)

        else:
            list_ids.append(ids['id'])
            return list_ids

    except Exception as error:
        print(error)


def get_message(service, user_id, msg_id):
    """
    take the services from get_service()
    user_id : your gmail
    msg_id : id of the message, get from search_message()
    returns gmail's messages after encoded
    """
    try:
        # grab the message instance
        message = service.users().messages().get(userId=user_id, id=msg_id,format='raw').execute()

        # decode the raw string, ASCII works pretty well here
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        # grab the string from the byte object
        mime_msg = email.message_from_bytes(msg_str)

        # check if the content is multipart (it usually is)
        content_type = mime_msg.get_content_maintype()
        if content_type == 'multipart':
            # there will usually be 2 parts the first will be the body in text
            # the second will be the text in html
            parts = mime_msg.get_payload()

            # return the encoded text
            final_content = parts[0].get_payload()
            return final_content

        elif content_type == 'text':
            return mime_msg.get_payload()

        else:
            return "Message is not text"

    # unsure why the usual exception doesn't work in this case, but
    # having a standard Exception seems to do the trick
    except Exception as error:
        print(error)


def get_service():
    """
    Authenticate the google api client and return the service object
    to make further calls
    return service api
    """
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)


    service = build('gmail', 'v1', credentials=creds)

    return service

def delete_message(service, user_id, msg_id):
  #delete the msg
  try:
    service.users().messages().delete(userId=user_id, id=msg_id).execute()
    print('Message with id: %s deleted successfully.' % msg_id)
  except Exception as error:
    print(error)
