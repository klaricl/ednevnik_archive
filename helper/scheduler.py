import datetime

def get_time_of_teaching(order, start):
    PAUSE = datetime.time(0,5)
    CLASS_DURATION = datetime.time(0,45)
    time = datetime.datetime(1,1,1,start.hour, start.minute)

    order -= 1

    time += datetime.timedelta(minutes = 5) * order
    time += datetime.timedelta(minutes = 45) * order
    
    return time.time()
