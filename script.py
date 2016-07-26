# -*- coding: utf-8 -*-

import io
import random
import re
import requests
import time

url1 = 'https://club.pokemon.com/uk/pokemon-trainer-club/sign-up/'
url2 = 'https://club.pokemon.com/uk/pokemon-trainer-club/parents/sign-up'

# emails = [email.strip() for email in open("emails.txt", "r").readlines()]
# birth_dates = [birth_date.strip() for birth_date in open("random_birth_dates.txt", "r").readlines()]
# countries = [country.strip() for country in open("random_countries.txt", "r").readlines()]
# print emails
# print birth_dates
# print countries


def register(birth_date, country, username, password, email):
    with requests.Session() as session:
        first_page = session.get(url1).text
        text_file = io.open("logs/Output1.out", "w", encoding='utf-8')
        text_file.write("TEXT %s" % first_page)
        text_file.close()
        first_csrf = re.search('name=\'csrfmiddlewaretoken\' value=\'(.+?)\'', first_page).group(1)
        second_page = session.post(url1, data={'csrfmiddlewaretoken': first_csrf, 'country': country, 'dob': birth_date},
                                       headers={'referer': url1}).text
        text_file = io.open("logs/Output2.out", "w", encoding='utf-8')
        text_file.write("First csrf %s\nTEXT= %s" % (first_csrf, second_page))
        text_file.close()
        second_csrf = re.search('name=\'csrfmiddlewaretoken\' value=\'(.+?)\'', second_page).group(1)
        third_page = session.post(url2, data={'csrfmiddlewaretoken': second_csrf, 'country': country, 'dob': birth_date,
                                         'username': username, 'password': password, 'confirm_password': password,
                                         'email': email, 'confirm_email': email,
                                         'public_profile_opt_in': 'False', 'terms': 'on'},
                                    headers={'referer': url2}).text
        text_file = io.open("logs/Output3.out", "w", encoding='utf-8')
        text_file.write("Second csrf %s\nTEXT= %s" % (second_csrf, third_page))
        text_file.close()

register("1990-07-03","US","PIPPOBAUDOBAU","password123","pippomagic@gmailg.com")
