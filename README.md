# user-id-anonymization
Generates random IDs for people corresponding to their email addresses, and emails them to those, without us knowing the mapping

Takes a list (a .csv or a new-line (\n) separated .txt file of email addresses), generates a 6-digit numeric random ID against that email address, and emails the random ID to the specified email address.
We would not know which random ID corresponds to which email address. We would make sure that no two participants get the same randomly generated ID.
