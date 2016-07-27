# -*- coding: utf-8 -*-

import io
import random
import re
import requests
import sys
import time
import traceback

url1 = 'https://club.pokemon.com/uk/pokemon-trainer-club/sign-up/'
url2 = 'https://club.pokemon.com/uk/pokemon-trainer-club/parents/sign-up'

class PtcRegistrationError(Exception):
    pass

# emails = [email.strip() for email in open("emails.txt", "r").readlines()]
# birth_dates = [birth_date.strip() for birth_date in open("random_birth_dates.txt", "r").readlines()]
# countries = [country.strip() for country in open("random_countries.txt", "r").readlines()]
# print emails
# print birth_dates
# print countries
seconds_between_each_call = 2
seconds_between_each_registration = 10


def execute_first_call(logfile1, session):
    first_page = session.get(url1).text
    text_file = io.open(logfile1, "w", encoding='utf-8')
    text_file.write(first_page)
    text_file.close()
    first_csrf = re.search('name=\'csrfmiddlewaretoken\' value=\'(.+?)\'', first_page).group(1)
    return first_csrf


def execute_second_call(birth_date, country, first_csrf, logfile2, session):
    second_page = session.post(url1, data={'csrfmiddlewaretoken': first_csrf, 'country': country, 'dob': birth_date},
                               headers={'referer': url1}).text
    text_file = io.open(logfile2, "w", encoding='utf-8')
    text_file.write(second_page)
    text_file.close()
    return second_page


def execute_third_call_and_return_result(birth_date, country, email, logfile3, password, second_csrf, session,
                                         username):
    third_page = session.post(url2, data={'csrfmiddlewaretoken': second_csrf, 'country': country, 'dob': birth_date,
                                          'username': username, 'password': password, 'confirm_password': password,
                                          'email': email, 'confirm_email': email,
                                          'public_profile_opt_in': 'False', 'terms': 'on'},
                              headers={'referer': url2}).text
    text_file = io.open(logfile3, "w", encoding='utf-8')
    text_file.write(third_page)
    text_file.close()
    result = bool(re.search('Thank you for creating a Pokémon Trainer Club account.', third_page))


def register(birth_date, country, username, password, email):
    print "Registration of account %s:%s - Start" % (username, password)
    logfile1 = "logs/page1.%s.html" % username
    logfile2 = "logs/page2.%s.html" % username
    logfile3 = "logs/page3.%s.html" % username
    try:
        with requests.Session() as session:
            first_csrf = execute_first_call(logfile1, session)
            time.sleep(seconds_between_each_call)

            second_page = execute_second_call(birth_date, country, first_csrf, logfile2, session)
            time.sleep(seconds_between_each_call)

            second_csrf = re.search('name=\'csrfmiddlewaretoken\' value=\'(.+?)\'', second_page).group(1)
            execute_third_call_and_return_result(birth_date, country, email, logfile3, password, second_csrf, session,
                                                 username)
            result = False
            if result:
                print "Registration of account %s:%s - completed with success" % (username, password)
            else:
                raise PtcRegistrationError("The final page does not contain the expected content."
                                           " Check the log file '%s' for the content." % logfile3)
    except PtcRegistrationError, e:
        print "Registration of account %s:%s - failed" % (username, password)
        print str(e)
    except:
        print "Registration of account %s:%s - failed" % (username, password)
        traceback.print_exc(file=sys.stdout)


register("1990-07-03","US","PIPPOBAUDOBAU2","password123","pippomagic2@gmailg.com")
