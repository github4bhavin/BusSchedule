
import time
from datetime import datetime, timedelta

def test_represent_time():
    tstr = '08:15'
    (h,m) = tstr.split(':')
    tday = datetime.today()
    tobj = datetime(year=tday.year, month=tday.month, day=tday.day, hour=int(h), minute=int(m))
    # (tobj.hour, tobj.minute) = tstr.split(':')

    # assert isinstance( tobj, (time.struct_time) )
    
    print(tobj)
    print(tobj + timedelta(hours=2))
    