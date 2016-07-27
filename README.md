ptc-registration
============
Script for quick registration of "disposable" PTC (Pokèmon Trainer Club) accounts. For "disposable" I mean unconfirmed accounts, that will be rendered inactive after 48 hours from the registration.

The accounts are registered with a random generated email, if you want a confirmed account with a valid email, you can provide your emails through an external configuration file.

**Pull requests are very welcome**, since this is a project of a couple of hours, it served its scope but it could be more powerful and configurable.

Requirements
============
* Python 2.7 (not sure about different versions, if you use it with different versions, please let me know and I'll update the README.md)
* **[Requests](https://github.com/kennethreitz/requests)** >= 2.0

Use
============
* `python script.py`will generate one random account
* `python script.py -random N` will generate N random accounts
* `python script.py -mails` will generate N random accounts, using each of the line of emails.txt in the script folder as email address.
