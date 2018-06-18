

import logging
import os
import json

from pprint import  pprint
from datetime import datetime, timedelta

logger = logging.getLogger('bus-schedule')

BASE_DIR = os.path.dirname(
                os.path.abspath(__file__)
            )

class RawSchedule(object):
    
    schedule = {}

    def __init__(self,bus_no):
        self.bus_no = bus_no
        self.get_raw_schedule()
        self.convert_to_datetime()
        
    @property
    def schedule_path(self):
        return os.path.join( BASE_DIR, 'Schedules', 'Raw', self.bus_no)


        
    @property
    def ny_schedule(self, category='weekday'):
        """
        :param category: ( weekday | weekend )
        :return:
        """
        return self.raw_schedule['New York'][category]

    def get_raw_schedule(self):
        with open( self.schedule_path, 'r' ) as fh:
            self.raw_schedule = json.load(fh)

    def create_dt(self, str_time):
        (h,m) = str_time.split(':')
        (h,m) = (int(h), int(m))
        tday = datetime.today()
        return datetime( year=tday.year, month=tday.month, day=tday.day, hour=h, minute=m)
        
    def convert_to_datetime(self):
        for city in self.raw_schedule:
            if city not in self.schedule: self.schedule[city] = {}
            
            for category in self.raw_schedule[city]:
                if category not in self.schedule[city]: self.schedule[city][category] = []
                
                for schedule_time in self.raw_schedule[city][category]:
                    self.schedule[city][category].append( self.create_dt(schedule_time) )

class ProcessedSchedule(object):
    
    processed = {}

    def __init__(self, raw_schedule):
        self.raw = raw_schedule
        self.bus_no = self.raw.bus_no

    @property
    def schedule_path(self):
        return os.path.join( BASE_DIR, 'Schedules', 'Processed', self.bus_no)
    
    def generate_schedule(self):
        
        for city in self.raw.schedule:
            if city not in self.processed : self.processed[city] = {}

            for category in self.raw.schedule[city]:
                if category not in self.processed[city] : self.processed[city][category] = {}
                
                for stime in self.raw.schedule[city][category]:
                    
                    self.get_missing_schedule(stime=stime, city=city, category=category)
                    
                    
    def get_missing_schedule(self, stime, city, category):
        
        td = datetime.today()
        rdt = datetime( year=td.year, month=td.month, day=td.day, hour=00, minute=00 )
        
        while rdt <= stime:
            if rdt not in self.processed[city][category]:
                self.processed[city][category][rdt] = stime
                
            rdt = rdt + timedelta(minutes=1)

    def write_schedule(self):
        
        writable_schedule = {}
        
        # convert keys to string
        for city in self.processed:
            if city not in writable_schedule : writable_schedule[city] = {}

            for cat in self.processed[city]:
                if cat not in writable_schedule: writable_schedule[city][cat] = {}

                for dt, st in self.processed[city][cat].items():
                    #print( dt.strftime("%H:%M"), st.strftime("%I:%M"))
                    writable_schedule[city][cat][dt.strftime("%H:%M")] = st.strftime("%I:%M")
        
        processed_json = json.dumps( writable_schedule )
        with open( self.schedule_path , 'w') as fh:
            fh.write(processed_json)
