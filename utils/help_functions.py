import re


def get_number(string):
    pattern = re.compile(r'\d')
    arr = re.findall(pattern, string)
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


# def check_edit_params(name, phone_last, phone_now, address, password):
#     if len(name) > 3:
