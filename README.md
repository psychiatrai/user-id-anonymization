# user-id-anonymization
Generates random IDs for people corresponding to their email addresses, and emails them to those, without us knowing the mapping

Takes a list (a .csv or a new-line (\n) separated .txt file of email addresses), generates a 6-digit alphanumeric random ID against that email address, and emails the random ID to the specified email address.
We would not know which random ID corresponds to which email address. We would make sure that no two email addresses get the same randomly generated ID.

## Installation
```
pip install requirements.txt
```

## Usage
```
touch .env
```

In your `.env` file, specify your email address and password using your favorite text editor. Needless to say, do not publish this file.

A sample `.env` file would look like this:

```
SOURCE_EMAIL="your@email.com"
SOURCE_EMAIL_PASSWORD="your_password"
```

Finally, run the script as follows:

```
python -m generate_random_user_ids -e <path-to-email-list> -o <path-to-store-the-generated-and-shuffled-random-IDs> -m <path-to-the-email-message-content-file (.txt)>
```

Example usage:

```
python -m generate_random_user_ids -e sample_email_list.txt -o sample_generated_ids.txt -m sample_message.txt
```

