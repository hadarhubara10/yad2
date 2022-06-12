import requests
from bs4 import BeautifulSoup


def get_yad2_content():
    url = "https://www.yad2.co.il/vehicles/cars"

    headers = {
        "cookie": '__uzma=9c48d5c1-6f2f-4a4b-9206-df6889d26754; __uzmb=1653295874; __uzme=9527; abTestKey=19; canary=never; _gid=GA1.3.1016085564.1653295877; __ssds=3; __ssuzjsr3=a9be0cd8e; __uzmbj3=1653295878; __uzmaj3=64f47a41-1687-4272-9f98-e584b225190c; server_env=production; y2018-2-cohort=94; leadSaleRentFree=31; use_elastic_search=1; __gads=ID=2b053cd13237d253:T=1653295660:S=ALNI_MY8DhDbn5O-uswj198-CkISwTgfdw; _fbp=fb.2.1653295883744.1667383413; bc.visitor_token=6934414757425733632; _gcl_au=1.1.177686135.1653297688; _hjSessionUser_266550=eyJpZCI6IjNmNjU1ZTMwLThjZTEtNTU5MS1iYmRlLWEzM2NhYTYyZTkxMiIsImNyZWF0ZWQiOjE2NTMyOTc3MTM2NDQsImV4aXN0aW5nIjp0cnVlfQ==; y2session=ba8eb1e4310777a6c0b2f98c96634714; _hjSessionUser_1413567=eyJpZCI6IjFmMjdlMTMxLTAwZTgtNWViNi05MmZmLTU2Yzg1YjViNDFmZCIsImNyZWF0ZWQiOjE2NTMyOTc5MDA4OTcsImV4aXN0aW5nIjpmYWxzZX0=; _hjSessionUser_2884988=eyJpZCI6IjcyM2EyY2I2LTkzM2UtNWY5Zi04NTA4LTBjYWYyODU2MDU0MSIsImNyZWF0ZWQiOjE2NTMyOTc5MDI0MjEsImV4aXN0aW5nIjpmYWxzZX0=; __uzmhj=d901640c84bb988b5184c49c0b99aa2e30b3667168e532fa5cf30d97ad764816; y2_cohort_2020=73; __gpi=UID=000006a630434566:T=1653295660:RT=1653383547:S=ALNI_MZ2ZSittYJJzqd4uwtcKKxfgPxUlA; _hjSession_266550=eyJpZCI6IjQxNWFmYmFkLWZlNTktNGRhMi1iMmM3LWQyM2ExNWYzNTBmZiIsImNyZWF0ZWQiOjE2NTMzODM1NTIxMzAsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; _hjIncludedInSessionSample=0; __uzmcj3=234573134990; __uzmdj3=1653384483; rdw_storereferer=https://www.yad2.co.il/; _gat_UA-708051-35=1; _ga_GQ385NHRG1=GS1.1.1653383549.3.1.1653384487.0; _ga=GA1.1.2088360494.1653295877; __uzmc=2875915487802; __uzmd=1653384485; __uzmf=7f600032044ae9-b931-401c-a14f-de204eab93d9165329587498388610549-c5e6218f4fa85ce2154; favorites_userid=gjg1899567822',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # modaa = soup.select_one('.feed_item_0_title')
    for i in range(1, 10):
        modaa = soup.find("span", {"id": 'feed_item_' + str(i) + '_title'})

        modaa_id = soup.find("div", {"id": 'feed_item_' + str(i)})['item-id']

        # # Link to item page
        # print('https://www.yad2.co.il/item/' + str(modaa_id))
        # # ID of car
        # print(modaa_id)
        # # Title of car
        # print(modaa.span.string)
        return f"""https://www.yad2.co.il/item/{str(modaa_id)}
modaa_id - {modaa_id}
modaa_tiitle - {modaa.span.string}
"""


if __name__ == '__main__':
    print(get_yad2_content())
