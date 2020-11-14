async def unaware_timezone(time_now):
    sec = time_now.second
    minute = time_now.minute
    hour = time_now.hour
    day = time_now.day
    month = time_now.month
    year = time_now.year
    #print ("======================")
    #print (time_now)
    #print (year,month,day,hour,minute,sec)
    return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=sec)

async def time_future(duration):
    time_now = datetime.datetime.now(datetime.timezone.utc)
    duration = int(duration)
    minute = hour = day = 0
    sec = int(duration)
    day = sec // (24 * 3600)
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minutes = sec // 60
    sec %= 60
    future_time = time_now + \
        datetime.timedelta(minutes=minute, days=day,
                           seconds=duration, hours=hour)
    from datetime import timezone
    timestamp = future_time.replace(tzinfo=timezone.utc)
    return future_time



async def convert_possible_time_to_sec(possible_time):
    seconds = ["s", "sec", "secs", "seconds", "second"]
    minutes = ["m", "min", "mins", "minute", "minutes"]
    hours = ["h", "hour", "hours"]
    days = ["d", "day", "days"]
    weeks = ["w", "week", "weeks"]
    sec: int = 0
    counter = 0
    time_trial_counter = 0
    time_data_started: bool = False
    for item in possible_time:
        item = str(item)
        if time_data_started == True:
            time_trial_counter += 1
            print("heres the counters: ", counter, time_trial_counter)
            if int(counter) != time_trial_counter:
                data = [sec, int(possible_time.index(item))-1]
                return data
        for i in seconds:
            print(i, item)
            if str(item).endswith(str(i)):
                second = item[:-int(len(i))]
                try:
                    second = int(second)
                except:
                    print("can't convert string to int")
                else:
                    sec += second
                    time_data_started = True
                    counter += 1
        for i in minutes:
            print(i, item)
            if str(item).endswith(str(i)):
                second = item[:-int(len(i))]
                try:
                    second = int(second)
                except:
                    print("can't convert string to int")
                second = second*60
                sec += second
                time_data_started = True
                counter += 1
        for i in hours:
            print(i, item)
            if str(item).endswith(str(i)):
                second = item[:-int(len(i))]
                try:
                    second = int(second)
                except:
                    print("can't convert string to int")
                else:
                    sec += second*3600
                    time_data_started = True
                    counter += 1
        for i in days:
            print(i, item)
            if str(item).endswith(str(i)):
                second = item[:-int(len(i))]
                try:
                    second = int(second)
                except:
                    print("can't convert string to int")
                else:
                    sec += second*86400
                    time_data_started = True
                    counter += 1
        for i in weeks:
            print(i, item)
            if str(item).endswith(str(i)):
                second = item[:-int(len(i))]
                try:
                    second = int(second)
                except:
                    print("can't convert string to int")
                else:
                    sec += second*604800
                    time_data_started = True
                    counter += 1
    data = [sec, int(len(possible_time)-1)]
    return data


async def sec_to_time(sec):
    sec = int(sec)
    day = sec // (24 * 3600)
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minutes = sec // 60
    sec %= 60
    seconds = sec
    time_human: str = ""
    if day > 0:
        time_human = time_human+f"{day} days"
    if hour > 0:
        time_human = time_human+f"{hour} hours"
    if minutes > 0:
        time_human = time_human+f"{minutes} mins"
    if seconds > 0:
        time_human = time_human+f"{seconds} seconds"
    return time_human
