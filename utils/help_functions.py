import io
import re


def get_number(string):
    pattern = re.compile(r'\d')
    arr = re.findall(pattern, string)
    if len(arr) < 10:
        return False
    if (arr[0] in '78' and len(arr) == 11) or (arr[0] == '9' and len(arr) == 10):
        if len(arr) == 10:
            arr.insert(0, '7')
        elif len(arr) == 11:
            arr[0] = '7'
    else:
        return False
    arr = ''.join(arr)
    arr = f'+7{arr[1:11]}'

    return arr
