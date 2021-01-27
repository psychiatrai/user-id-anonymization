import argparse
import base64
from decouple import config
from email.message import EmailMessage
import numpy as np
import smtplib
import random
import string


def get_source_email_credentials_from_environment_variables():
    '''
        Gets the source email address and password from a local
        .env file
    '''
    SOURCE_EMAIL = config('SOURCE_EMAIL')
    SOURCE_EMAIL_PASSWORD = config('SOURCE_EMAIL_PASSWORD')

    return SOURCE_EMAIL, SOURCE_EMAIL_PASSWORD


def get_email_addresses_from_file(email_list_file):
    '''
        Gets the email addresses stored in the email list file
    '''
    email_addresses = []
    with open(email_list_file, mode='r', encoding='utf-8') as email_list:
        for email in email_list:
            email_addresses.append(email)
    
    return email_addresses


def read_email_message_template(message_file):
    '''
        Reads the template of the email to be sent to the study participants
    '''
    with open(message_file, mode='r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    
    return string.Template(template_file_content)


def create_SMTP_instance():
    '''
        Creates an SMTP instance and logins into that
    '''
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()

    SOURCE_EMAIL, SOURCE_EMAIL_PASSWORD = get_source_email_credentials_from_environment_variables()

    s.login(SOURCE_EMAIL, SOURCE_EMAIL_PASSWORD)

    return s


def generate_random_participant_IDs(email_addresses):
    '''
        Generates six-digit alphanumeric IDs against a given list of email addresses
    '''
    random_participant_ids = set()        
    while len(email_addresses) != len(random_participant_ids):
        participant_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        random_participant_ids.add(participant_id)

    return random_participant_ids


def main():
    '''
        The main method which parses the arguments and calls
        the appropriate functions
    '''
    if __name__ == "__main__":
        
        parser = argparse.ArgumentParser(description='Generates six digit numerical \
            random IDs corresponding to a file containing email IDs and emails the \
            recipients their random ID, while storing a shuffled version of the \
            randomly generated IDs')
        parser.add_argument('--email_list', '-e', required=True, help=' The file \
            location of the list containing all the email IDs')
        parser.add_argument('--output_file', '-o', required=True,
            default="./shuffled_random_ID_list.txt", help='Output file location of the \
                list containing all the generated random IDs, but shuffled so that \
                there is no identifiable mapping between the email list and the \
                randomly generated IDs')
        parser.add_argument('--email_message', '-m', required=True, default='message.txt',
         help=' The file location of the email message to send to the study participants')

        args = parser.parse_args()

        SMTP_instance = create_SMTP_instance()

        email_addresses = get_email_addresses_from_file(args.email_list)
        email_message = read_email_message_template(args.email_message)

