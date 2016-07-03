import textwrap


_SECONDS_IN_MINUTE = 60


def seconds_to_minutes_and_seconds(seconds):
    string = ''
    
    if seconds is not None:
        negative = '-' if seconds < 0 else ''
    
        if seconds < 1:
            string = '<{}1s'.format(negative)
        else:
            seconds = round(abs(seconds))
            
            s = int(seconds % _SECONDS_IN_MINUTE)
            m = int((seconds - s) / _SECONDS_IN_MINUTE)
            
            string = '{}{}m {}s'.format(negative, m, s) if m > 0 else '{}{}s'.format(negative, s)
    
    return string


def wrap_str_array(str_array, width=70):
    return '\n'.join(['\n'.join(textwrap.wrap(line, width=width)) for line in str_array])
