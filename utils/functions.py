from datetime import time, timedelta


def generate_time_choices(start_hour=6, end_hour=22, interval_minutes=30):
    times = []
    current_time = time(start_hour, 0)
    end_time = time(end_hour, 0)
    
    while current_time <= end_time:
        time_label = current_time.strftime('%H:%M')
        times.append((current_time, time_label))
        
        current_datetime = (timedelta(hours=current_time.hour, minutes=current_time.minute) 
                            + timedelta(minutes=interval_minutes))
        current_time = (time(current_datetime.seconds // 3600, 
                             (current_datetime.seconds // 60) % 60))
        
    return times

def convert_hours_units_to_time(unit):
    if unit < 0 or unit > 32:
        raise ValueError("O número deve ser um inteiro positivo.")
    
    total_minutes = unit * 30
    hours, minutes = divmod(total_minutes, 60)

    return time(hours, minutes)
    