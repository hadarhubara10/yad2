import json


def get_manufacturer_json():
    with open('manufacturer.json', 'r', encoding="utf8") as f:
        data = json.load(f)
        return data['manufacturer']


json_manufacturer = get_manufacturer_json()

# Get array of manufacturers code #

# def get_code_of_manufacturer(manufacturers):
#     list_of_code = []
#     for manufacturer in manufacturers:
#         for item in json_manufacturer:
#             if item["text"] == manufacturer:
#                 list_of_code.append(item["value"])
#     return list_of_code

# print(get_code_of_manufacturer(['שברולט', 'מאזדה']))


#  Get code of manufacturer #


def get_code_of_manufacturer(manufacturer):
    for item in json_manufacturer:
        if item["text"] == manufacturer:
            return item["value"]


print(get_code_of_manufacturer('שברולט'))
