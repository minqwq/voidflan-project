import datetime
import pytz

def getCurtimeFmt():
    print(datetime.datetime.now().strftime("%c %z%Z"))

def getCurtimeFmt_pytz():
    utc = pytz.utc
    locdt = utc.localize(datetime.datetime.now())
    print(locdt.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

if __name__ == "__main__":
    getCurtimeFmt()
    getCurtimeFmt_pytz()
