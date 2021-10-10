import requests
from bs4 import BeautifulSoup
import re

class WebUtils():
    @staticmethod
    def getHtmlByUrl(url):
        response = requests.get(url)
        return response.content

    @staticmethod
    def getEventsWithDeadlinesByUrl(url):
        eventToDeadline = dict()

        htmlDoc = WebUtils.getHtmlByUrl(url)

        event_tokens = WebUtils.__getEventTokensFromHtml(htmlDoc)
        event_tokens.pop()

        events = [event_tokens[i].contents[0].contents[0] for i in range(0, len(event_tokens), 2)]
        event_deadlines = [event_tokens[i].contents[0] for i in range(1, len(event_tokens), 2)]

        for i in range(0, len(events)):
            eventToDeadline[events[i]] = event_deadlines[i]

        return eventToDeadline

    @staticmethod
    def __getEventTokensFromHtml(html):
        soup = BeautifulSoup(html, 'html.parser')
        events = soup.findAll('a', attrs={'href': re.compile(r"/activity/.*/events/*")})
        return events

    @staticmethod
    def getRelatedOlympiadsByUrl(url):
        htmlDoc = WebUtils.getHtmlByUrl(url)

        olympiad_tokens = WebUtils.__getOlympiadsTokensFromHtml(htmlDoc)
        olympiad_tokens = olympiad_tokens[1:]

        try:
            olympiads = [(olympiad_token.contents[1].contents[0], olympiad_token['href']) for olympiad_token in olympiad_tokens]
        except AttributeError as err:
            print(f'Attribure Error: {err}')
            raise RuntimeError('Unknown format of webpage')

        nameToLink = dict(olympiads)

        return nameToLink


    @staticmethod
    def __getOlympiadsTokensFromHtml(html):
        soup = BeautifulSoup(html, 'html.parser')
        olympiads = soup.findAll('a', attrs={'href': re.compile(r"/activity/\d*$")})
        return olympiads

