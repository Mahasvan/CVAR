import threading

# initialize timer_done to False
timer_done = 0
lock = threading.Lock()

timer_thread = None

def set_timer_done():
    global timer_done

    if timer_done == 2:
        return

    lock.acquire()
    timer_done = 1
    lock.release()

def set_timer_interrupted():
    global timer_done
    
    lock.acquire()
    timer_done = 2
    lock.release()

def timer(seconds):
    global timer_thread
    # create a timer thread that sets timer_done to True after `seconds` seconds
    timer_thread = threading.Timer(seconds, lambda: set_timer_done())
    timer_thread.start()

def stop_timer():
    global timer_thread
    timer_thread.cancel()


def get_seconds_from_input(input_time_str: str):
    """Thanks to CorpNewt for helping out with this function"""
    accepted_chars = {
        "w": 604_800,
        "d": 86_400,
        "h": 3_600,
        "m": 60,
        "s": 1
    }
    time_seconds = 0
    last_number = ""
    for char in input_time_str:
        if char.isdigit():  # Check if we have a number
            last_number += char
        elif char in accepted_chars:  # Check if it's a valid suffix, and we have a time so far
            if last_number == "":
                continue
            time_seconds += int(last_number) * accepted_chars[char]
            last_number = ""
        else:
            last_number = ""
    if last_number:  # Check if we have any left - and add it
        time_seconds += int(last_number)
    return time_seconds

def pretty_time_from_seconds(time_remaining: int):
    if time_remaining < 0:
        return "0 seconds"
    minutes, seconds = divmod(time_remaining, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    final_string_to_join = []
    if weeks > 0:
        final_string_to_join.append(f"{weeks} {'weeks' if weeks != 1 else 'week'}")
    if days > 0:
        final_string_to_join.append(f"{days} {'days' if days != 1 else 'day'}")
    if hours > 0:
        final_string_to_join.append(f"{hours} {'hours' if hours != 1 else 'hour'}")
    if minutes > 0:
        final_string_to_join.append(f"{minutes} {'minutes' if minutes != 1 else 'minute'}")
    if seconds > 0:
        final_string_to_join.append(f"{seconds} {'seconds' if seconds != 1 else 'second'}")

    if len(final_string_to_join) > 1:
        final_string = ", ".join(final_string_to_join[:-1]) + f", and {final_string_to_join[-1]}"
    else:
        final_string = ", ".join(final_string_to_join)
    return final_string
