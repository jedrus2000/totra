# -*- coding: utf-8 -*-
import sys
from requests import Session, codes
from requests.exceptions import HTTPError
import maya
import logging
import json
from totra.exceptions import UnknownFormat

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger(__name__)

TTRACKER_API_BASE_URL = 'https://tracker-api.toptal.com/'


def report_activities(username, password, workers, projects, start_date, end_date):
    """gets activities"""
    tt = TTrackerSession()
    tt.login(username, password)
    return tt.report_activities(workers, projects, start_date, end_date)


def how_much_hours(username, password, workers, projects, start_date, end_date):
    """gets hours counts based on parameters"""
    tt = TTrackerSession()
    tt.login(username, password)
    return tt.how_much_hours(workers, projects, start_date, end_date)


def get_today_date_str():
    return maya.now().datetime().strftime('%Y-%m-%d')


class TTrackerSession(object):
    """implementing TopTracker API calls"""
    def __init__(self):
        self.session = Session()
        #self.session.proxies.update({
        #    'http': 'http://localhost:8888',
        #    'https': 'http://localhost:8888'
        #})
        #self.session.verify = False # prevent proxy SSL complain about certificate

        self.access_token = None
        self.user_json = None
        self.tzname = None
        #
        self._projects_cache = None
        self._reports_filters_cache = None

    def _convert_names_to_ids(self, names_list, subject):
        mapping = self.report_filters().get(subject, {})
        if not names_list:
            return [map['id'] for map in mapping]
        ids = []
        for map in mapping:
            if map['label'] in names_list:
                ids.append(map['id'])
        return ids

    def _convert_human_moment_to_date(self, human_moment):
        return maya.when(human_moment, self.tzname).datetime(to_timezone=self.tzname).strftime('%Y-%m-%d')

    def login(self, username, password, tzname=maya.now().local_timezone):
        try:
            self.tzname=tzname
            url = TTRACKER_API_BASE_URL + 'sessions'
            login_payload = {
                'email': username,
                'remember_me': True,
                'password': password,
                'time_zone': self.tzname
            }
            r = self.session.post(url, data=login_payload)
            r.raise_for_status()
            json_content = r.json()
            self.access_token = json_content['access_token']
            self.user_json = json_content['user']
        except (KeyError, HTTPError) as e:
            logger.error('login: {}, Content: {}'.format(
                e, r.text))
            sys.exit(1)

    def projects(self, archived=True):
        try:
            url = TTRACKER_API_BASE_URL + 'projects'
            params = {
                'access_token': self.access_token,
                'archived': archived,
                'time_zone': self.tzname
            }
            r = self.session.get(url, params=params)
            if r.status_code == codes.not_modified:
                json_content = self._projects_cache
            else:
                json_content = r.json()
                self._projects_cache = json_content
            return json_content['projects']
        except KeyError as e:
            logger.error('projects error. Status code: {}, Reason: {}'.format(r.status_code, r.reason))

    def report_filters(self):
        try:
            url = TTRACKER_API_BASE_URL + 'reports/filters'
            params = {
                'access_token': self.access_token,
                'time_zone': self.tzname
            }
            r = self.session.get(url, params=params)
            if r.status_code == codes.not_modified:
                json_content = self._reports_filters_cache
            else:
                json_content = r.json()
                self._reports_filters_cache = json_content
            return json_content['filters']
        except KeyError as e:
            logger.error('reports_filters error. Status code: {}, Reason: {}'.format(r.status_code, r.reason))

    def report_activities(self, workers, projects, start_date, end_date):
        output = {}
        try:
            url = TTRACKER_API_BASE_URL + 'reports/activities'
            params = {
                'access_token': self.access_token,
                'time_zone': self.tzname,
                'start_date': self._convert_human_moment_to_date(start_date),
                'end_date': self._convert_human_moment_to_date(end_date),
                'worker_ids[]': self._convert_names_to_ids(workers, 'workers'),
                'project_ids[]': self._convert_names_to_ids(projects, 'projects')
            }
            r = self.session.get(url, params=params)
            r.raise_for_status()
            output = r.json()['activities']
        except (KeyError, json.JSONDecodeError, HTTPError) as e:
            logger.error('report_activities error.  {}, Content: {}'.format(
                e, r.text))

        return output

    def how_much_hours(self, workers, projects, start_date, end_date):
        activities = self.report_activities(workers, projects, start_date, end_date)
        seconds = 0
        for activity in activities:
            seconds += activity.get('seconds', 0)
        return round(seconds/3600, 1)
