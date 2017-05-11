import os
import random
import requests
import sendgrid

from bs4 import BeautifulSoup
from sendgrid.helpers.mail import Email, Mail, Personalization, Substitution


BASE_URL = 'http://cinqminutesdepause.tumblr.com/page'
MIN_PAGE, MAX_PAGE = 0, 50 # First and last page to host content

def filter_articles(articles):
    articles = [a for a in articles if '»' in a]
    articles = [a for a in articles if 'In' in a]
    articles = [a for a in articles if '«' in a]
    articles = [a.split('«', maxsplit=1)[1].rsplit('»', maxsplit=1)[0] for a in articles]
    return articles

def get_articles_by_page(page):
    html_doc = requests.get(f'{BASE_URL}/{page}').text
    soup = BeautifulSoup(html_doc, 'html.parser')
    articles = soup.find_all('div', class_='body-text')
    articles = [a.get_text() for a in articles]
    articles = filter_articles(articles)
    return articles

def send_mail(recipient, subject, body):
    # Create a text/plain message
    me = 'no-reply@cinqminutesdepause.herokuapp.com'
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    # Creating mail
    mail = Mail()
    mail.from_email = Email(me, 'Cinq minutes de pause')
    mail.template_id = 'c871e900-fc06-45b5-b037-7ec58821ce27'
    # Substitutes
    personalization = Personalization()
    personalization.add_to(Email(recipient))
    mail.add_personalization(personalization)
    mail.personalizations[0].add_substitution(Substitution('-body-', body))
    mail.personalizations[0].add_substitution(Substitution('-subject-', subject))

    # Sending email
    try:
        sg.client.mail.send.post(request_body=mail.get())
    except Exception as error:
        print('Email not sent for {recipient}. Following error has occured:\n{error}')


is_valid = True
# While articles found are not nalid
while is_valid:
	rand_page = random.randint(MIN_PAGE, MAX_PAGE)
	articles = get_articles_by_page(rand_page)
	is_valid = len(articles) == 0

article = random.choice(articles)
send_mail('elmehdi.baha@gmail.com', 'Cinq minutes de pause', article)
