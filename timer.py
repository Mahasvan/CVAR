import threading

# initialize timer_done to False
timer_done = False
lock = threading.Lock()

def get_time(time):
    if time is not None:
        if time[-1] == 'd':
            time_final = int(time[-1]) * 3600 * 24
        elif time[-1] == 'h':
            time_final = int(time[:-1]) * 3600
        elif time[-1] == 'm':
            time_final = int(time[:-1]) * 60
        elif time[-1] == 's':
            time_final = int(time[:-1])
        else:
            time_final = int(time)
        return time_final

def set_timer_done():
    global timer_done
    
    lock.acquire()
    timer_done = True
    lock.release()

def timer(seconds):
    global timer_done
    # create a timer thread that sets timer_done to True after `seconds` seconds
    timer_thread = threading.Timer(seconds, lambda: set_timer_done())
    timer_thread.start()
