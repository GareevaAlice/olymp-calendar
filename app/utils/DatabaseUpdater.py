from app.utils.WebUtils import WebUtils
from app.models import Olympiad, Event
from datetime import date
import re


# Класс заполнения базы данных информацией об олимпиадах
class DatabaseUpdater():

    def __init__(self):
        # класс обработки web страниц
        self.webutils = WebUtils()

    def update_database(self):
        """
        Обновление базы данных информацией об олимпиадах
        :return: None
        """
        # получаем информацию об олимпиадах
        olympiads_info_list = self._get_olympiads_info_list()
        # сохраняем олимпиады и их события в базу данных
        self._save_olympiads_info(olympiads_info_list)

    def _get_olympiads_info_list(self):
        """
        Получение информацию об олимпиадах
        :return: list({'olympiad_name': string,
                    'olympiad_url': string,
                    'events': list({'event_name': string,
                                    'date_start': string,
                                    'date_end': string
                                    }, ...),
                    }, ...)
        """
        # данный список будет браться с помощью других функци
        # сейчас он заполнен вручную ради проверки корректности
        olympiads_url_lists = ['https://olimpiada.ru/activity/5277',
                               'https://olimpiada.ru/activity/180',
                               'https://olimpiada.ru/activity/5149',
                               'https://olimpiada.ru/activity/5668',
                               'https://olimpiada.ru/activity/157',
                               'https://olimpiada.ru/activity/5319',
                               'https://olimpiada.ru/activity/232',
                               'https://olimpiada.ru/activity/177',
                               'https://olimpiada.ru/activity/5761',
                               'https://olimpiada.ru/activity/251']

        olympiads_info_list = list()
        for i, olympiad_url in enumerate(olympiads_url_lists):
            # получение информацию о расписании событий олимпиады по url
            events_dict = \
                self.webutils.getEventsWithDeadlinesByUrl(olympiad_url)
            events_list = list()
            # обработка событий в расписании олимпиады
            for name, date in events_dict.items():
                date_start_end = self._get_date_start_end(date)
                events_list.append({'event_name': name,
                                    'date_start': date_start_end['date_start'],
                                    'date_end': date_start_end['date_end']})
            olympiads_info_list.append({'olympiad_name': str(i),
                                        'olympiad_url': olympiad_url,
                                        'events': events_list})
            print(olympiads_info_list[-1])
        return olympiads_info_list

    def _save_olympiads_info(self, olympiads_info_list):
        """
        Сохранение олимпиад и их событий в базу данных
        :param olympiads_info_list: информация об олимпиадах
        list({'olympiad_name': string,
            'olympiad_url': string,
            'events': list({'event_name': string,
                            'date_start': string,
                            'date_end': string
                            }, ...),
            }, ...)
        :return: None
        """
        for olympiad_info in olympiads_info_list:
            olympiad_id = \
                self._create_olympiad(name=olympiad_info['olympiad_name'],
                                      url=olympiad_info['olympiad_url'])
            for event in olympiad_info['events']:
                self._create_event(olympiad_id=olympiad_id,
                                   name=event['event_name'],
                                   date_start=event['date_start'],
                                   date_end=event['date_end'])

    @staticmethod
    def _create_olympiad(name, url=None):
        """
        Сохранение олимпиады в базу данных
        :param name: название олимпиады
        :param url: url олимпиады
        :return: id сохраненной олимпиады
        """
        olympiad = Olympiad(name=name, url=url)
        id = olympiad.save()
        print(olympiad)
        return id

    @staticmethod
    def _create_event(olympiad_id, name, date_start=None, date_end=None):
        """
        Сохранение события в базу данных
        :param olympiad_id: id оимпиады в базе данных,
                            которой пренадлежит событие
        :param name: название события
        :param date_start: дата начала проведения события
        :param date_end: дата конца проведения события
        :return: id сохраненного события
        """
        event = Event(olympiad_id=olympiad_id, name=name,
                      date_start=date_start, date_end=date_end)
        id = event.save()
        print(event)
        return id

    def _get_date_start_end(self, date):
        dates = re.sub('[...]', ' ', date).split()
        date_start = None
        date_end = None
        if dates[0] == 'До':
            date_start = self._transform_date(int(dates[1]), dates[2])
        elif len(dates) == 4:
            date_start = self._transform_date(int(dates[0]), dates[1])
            date_end = self._transform_date(int(dates[2]), dates[3])
        else:
            date_start = self._transform_date(int(dates[0]), dates[2])
            date_end = self._transform_date(int(dates[1]), dates[2])
        return {'date_start': date_start,
                'date_end': date_end}

    @staticmethod
    def _transform_date(day, month):
        months_dict = dict(zip(['янв', 'фев', 'мар',
                                'апр', 'май', 'июн',
                                'июл', 'авг', 'сен',
                                'окт', 'ноя', 'дек'], range(1, 13)))
        month_number = months_dict[month]
        year = 2021
        if month_number < 9:
            year = 2022
        return date(year, month_number, day)