import json

import openpyxl



def get_ak_from_xlsx():
    data = []
    file_path = '/Users/momo/Downloads/ak.xlsx'
    xlsx = openpyxl.load_workbook(file_path)
    sheets = xlsx.sheetnames
    book_sheet = xlsx[sheets[0]]

    row = 0
    for _row in book_sheet.rows:
        row += 1
        if row == 1: continue
        _data = {
            "UserName"  :_row[0].value.strip(),
            "UserId"    :str(row),
            "CreateDate":_row[2].value.strftime("%Y-%m-%d"),  # "yyyy-mm-dd"
            "Keys"      :[_row[1].value.strip()],
            "From"      :"huawei",
        }
        data.append(_data)
    return data


def get_aks_from_txt(file='/Users/momo/Documents/ak.txt'):
    with open(file, mode='r') as f:
        ak_list = f.readlines()
        ak_list = [ak.strip() for ak in ak_list]
    return ak_list

