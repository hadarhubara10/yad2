import json


def get_manufacturer_json():
    with open('manufacturer.json', 'r', encoding="utf8") as f:
        data = json.load(f)
        return data['manufacturer']
def get_owners_json():
    with open('owners.json', 'r', encoding="utf8") as f:
        data = json.load(f)
        return data['ownerID']

json_manufacturer = get_manufacturer_json()
json_owners=get_owners_json()
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
def get_code_of_owner(owners):
    for item in json_owners:
        if item["text"] == owners:
            return item["value"]

print(get_code_of_manufacturer('שברולט'))
