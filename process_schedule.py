

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
    def ny_schedule(self):
        """
        :return:
        """
        return self.raw_schedule['New York']

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

            if city not in self.schedule: self.schedule[city] = []

            for schedule_time in self.raw_schedule[city]:
                self.schedule[city].append( self.create_dt(schedule_time) )


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
            for stime in self.raw.schedule[city]: self.get_missing_schedule(stime=stime, city=city)
                    
                    
    def get_missing_schedule(self, stime, city):
        
        td = datetime.today()
        rdt = datetime( year=td.year, month=td.month, day=td.day, hour=00, minute=00 )
        
        while rdt <= stime:
            if rdt not in self.processed[city]: self.processed[city][rdt] = stime
            rdt = rdt + timedelta(minutes=1)


    def write_schedule(self):
        
        writable_schedule = {}
        
        # convert keys to string
        for city in self.processed:
            if city not in writable_schedule : writable_schedule[city] = {}

            for dt, st in self.processed[city].items():
                dt_str = dt.strftime("%H:%M")
                st_str = st.strftime("%I:%M")

                with open( os.path.join(self.schedule_path, dt_str )  , 'w') as fh:
                    line = {}
                    line[dt_str] = st_str
                    fh.writelines( json.dumps( line ) )
                    print( "{} | {}  -- {} ".format(dt_str, st_str, line))
                    del line
                #writable_schedule[city][dt.strftime("%H:%M")] = st.strftime("%I:%M")
        
        # processed_json = json.dumps( writable_schedule )
        # with open( self.schedule_path , 'w') as fh:
        #     fh.write(processed_json)


if __name__ == '__main__':
    
    BUS_NO = '321'

    raw = RawSchedule(BUS_NO)
    processed = ProcessedSchedule(raw)
    processed.generate_schedule()
    processed.write_schedule()