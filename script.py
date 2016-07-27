# -*- coding: utf-8 -*-

import io
import random
import re
import requests
import sys
import time
import traceback
import uuid

url1 = 'https://club.pokemon.com/uk/pokemon-trainer-club/sign-up/'
url2 = 'https://club.pokemon.com/uk/pokemon-trainer-club/parents/sign-up'

class PtcRegistrationError(Exception):
    pass

#delay configuration in seconds
seconds_between_each_call = 2
seconds_between_each_registration = 10

#preset data
birth_dates = [birth_date.strip() for birth_date in open("random_birth_dates.txt", "r").readlines()]
countries = [country.strip() for country in open("random_countries.txt", "r").readlines()]

class PtcRegistration:
    def __init__(self, birth_date, country, username, password, email):
        self.birth_date = birth_date
        self.country = country
        self.username = username
        self.password = password
        self.email = email
        self.logfile1 = "logs/page1.%s.html" % username
        self.logfile2 = "logs/page2.%s.html" % username
        self.logfile3 = "logs/page3.%s.html" % username
        self.first_csrf = None
        self.second_csrf = None

    def execute(self):
        print "Registration of account %s:%s - Start" % (self.username, self.password)

        try:
            with requests.Session() as session:
                self.execute_first_call(session)
                time.sleep(seconds_between_each_call)

                self.execute_second_call(session)
                time.sleep(seconds_between_each_call)

                content = self.execute_third_call_and_return_body(session)

                result = self.is_registration_completed_successfully(content)

                if result:
                    print "Registration of account %s:%s - completed with success" % (self.username, self.password)
                else:
                    raise PtcRegistrationError("The final page does not contain the expected content."
                                               " Check the log file '%s' for the content." % self.logfile3)
        except PtcRegistrationError, e:
            print "Registration of account %s:%s - failed" % (self.username, self.password)
            print str(e)
        except:
            print "Registration of account %s:%s - failed" % (self.username, self.password)
            traceback.print_exc(file=sys.stdout)

    def execute_first_call(self, session):
        first_page = session.get(url1).text
        text_file = io.open(self.logfile1, "w", encoding='utf-8')
        text_file.write(first_page)
        text_file.close()
        self.first_csrf = re.search('name=\'csrfmiddlewaretoken\' value=\'(.+?)\'', first_page).group(1)

    def execute_second_call(self, session):
        second_page = session.post(url1,
                                   data={'csrfmiddlewaretoken': self.first_csrf,
                                               'country': self.country,
                                               'dob': self.birth_date},
                                   headers={'referer': url1}).text
        text_file = io.open(self.logfile2, "w", encoding='utf-8')
        text_file.write(second_page)
        text_file.close()
        self.second_csrf = re.search('name=\'csrfmiddlewaretoken\' value=\'(.+?)\'', second_page).group(1)


    def execute_third_call_and_return_body(self, session):
        third_page = session.post(url2,
                                  data={'csrfmiddlewaretoken': self.second_csrf,
                                              'country': self.country,
                                              'dob': self.birth_date,
                                              'username': self.username,
                                              'password': self.password,
                                              'confirm_password': self.password,
                                              'email': self.email,
                                              'confirm_email': self.email,
                                              'public_profile_opt_in': 'False',
                                              'terms': 'on'},
                                  headers={'referer': url2}).text
        text_file = io.open(self.logfile3, "w", encoding='utf-8')
        text_file.write(third_page)
        text_file.close()
        return third_page

    def is_registration_completed_successfully(self, third_page_body):
        return bool(re.search('Hello! Thank you for creating an account!', third_page_body))


def get_random_alphanumeric_string(size):
    return str(uuid.uuid4().get_hex().upper()[0:size])


def generate_random_user():
    random_10_char_string = get_random_alphanumeric_string(10)
    random_12_char_string = get_random_alphanumeric_string(12)

    registration = PtcRegistration(random.choice(birth_dates),
                                   random.choice(countries),
                                   random_12_char_string,  # username
                                   random_10_char_string,  # password
                                   '%s@hotmail.com' % random_12_char_string)
    registration.execute()

def generate_from_email_list():
    emails = [email.strip() for email in open("emails.txt", "r").readlines()]
    for email in emails:
        registration = PtcRegistration(random.choice(birth_dates),
                                       random.choice(countries),
                                       get_random_alphanumeric_string(12),
                                       get_random_alphanumeric_string(10),
                                       email)
        registration.execute()
        time.sleep(seconds_between_each_registration)


def generate_n_random_accounts(number_of_accounts):
    for i in range(0, number_of_accounts):
        generate_random_user()
        time.sleep(seconds_between_each_registration)


def main(argv):
    if len(argv) == 0:
        generate_random_user()
        sys.exit(0)

    if argv[0] == '-mails':
        generate_from_email_list()
        sys.exit(0)

    if argv[0] == '-random':
        accounts = int(argv[1])
        generate_n_random_accounts(accounts)
        sys.exit(0)

    raise Exception('invalid arguments %s' % argv)


if __name__ == "__main__":
   main(sys.argv[1:])


