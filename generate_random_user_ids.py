import argparse
from decouple import config
from email.message import EmailMessage
import smtplib
import random
import string


def get_source_email_credentials_from_environment_variables():
    '''
        Gets the source email address and password from a local
        .env file
    '''
    global SOURCE_EMAIL
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


def generate_random_participant_IDs(email_addresses):
    '''
        Generates six-digit alphanumeric IDs against a given list of email addresses
    '''
    random_participant_ids = set()        
    while len(email_addresses) != len(random_participant_ids):
        participant_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        random_participant_ids.add(participant_id)

    return random_participant_ids


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


def compose_and_send_emails(SMTP_instance, email_message_content, email_addresses, participant_ids):
    '''
        Composes and sends emails to each participant
    '''
    for email_address, participant_id in zip(email_addresses, participant_ids):
        msg = EmailMessage()
        
        message = email_message_content.substitute(PARTICIPANT_ID=participant_id)
        msg.set_content(message)
        
        msg['Subject'] = '[Confidential] Your random participant ID for the psychiatr.ai pilot study'
        msg['From'] = SOURCE_EMAIL
        msg['To'] = email_address
    
        SMTP_instance.send_message(msg)


def save_shuffled_generated_participant_ids(participant_ids, output_file_location):
    '''
        Saves a shuffled version of the generated participant IDs for 
        future reference. No mapping between email addresses and the 
        participant IDs can be obtained in this way
    '''
    random.shuffle(participant_ids)
    with open(output_file_location, mode='w', encoding='utf-8') as output_file:
        for participant_id in participant_ids:
            output_file.write(participant_id+'\n')


def main():
    '''
        The main method which parses the arguments and calls
        the appropriate functions
    '''
    parser = argparse.ArgumentParser(description='Generates six digit alphanumeric \
            random IDs corresponding to a file containing email IDs and emails the \
            recipients their random ID, while storing a shuffled version of the \
            randomly generated IDs')
    parser.add_argument('--email_list', '-e', required=True, help=' The file \
        location of the list containing all the email IDs')
    parser.add_argument('--output_file', '-o', default="shuffled_random_ID_list.txt", 
        help='Output file location of the list containing all the generated random IDs, \
            but shuffled so that there is no identifiable mapping between the email list \
            and the randomly generated IDs')
    parser.add_argument('--email_message', '-m', required=True, default='message.txt',
        help=' The file location of the email message to send to the study participants')

    args = parser.parse_args()

    SMTP_instance = create_SMTP_instance()

    email_addresses = get_email_addresses_from_file(args.email_list)
    participant_ids = list(generate_random_participant_IDs(email_addresses))
    email_message_content = read_email_message_template(args.email_message)
    
    compose_and_send_emails(SMTP_instance, email_message_content, email_addresses, participant_ids)

    del email_addresses

    SMTP_instance.quit()

    save_shuffled_generated_participant_ids(participant_ids, args.output_file)


if __name__ == "__main__":
    main()

