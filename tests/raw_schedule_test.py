import pytest

import sys, os
sys.path.append('..')

from pprint import  pprint
from process_schedule import RawSchedule, ProcessedSchedule

bus_no = '321'

def test_raw_scheudle():
    raw = RawSchedule(bus_no)
    assert raw.raw_schedule is not None

def test_ny_weekday_schedule():
    raw = RawSchedule(bus_no)
    assert  raw.ny_schedule is not None
    assert  isinstance( raw.ny_schedule , (list, tuple))
    
def test_convert_to_timestamp():
    raw = RawSchedule(bus_no)
    
    
def test_processed_schedule():
    raw = RawSchedule(bus_no)
    p = ProcessedSchedule(raw)
    p.generate_schedule()
    #pprint( p.processed )
    
    p.write_schedule()