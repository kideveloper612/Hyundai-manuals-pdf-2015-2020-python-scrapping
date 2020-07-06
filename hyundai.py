import os
import csv
import requests
import time
from bs4 import BeautifulSoup


def send_request(url, method, data):
    try:
        headers = {
            'Cookie': 'BIGipServerPOOL-192.237.132.213-80-owners.hyundaiusa.com=2818970796.20480.0000'
        }
        res = requests.request(method, url=url, headers=headers, data=data)
        print(res.status_code)
        if res.status_code == requests.codes.ok:
            return res
        return None
    except ConnectionError:
        time.sleep(5)
        return send_request(url=url)
    except Exception as e:
        print(e)
        time.sleep(5)
        return send_request(url=url)


def write_csv(lines, filename):
    with open(filename, 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)


def main():
    for year in range(2015, 2021):
        data = {
            'firstnode': year,
            'filepath': '/content/dam/hyundai/us/myhyundai/image',
            'secondnode': ''
        }
        mo = send_request(url='https://owners.hyundaiusa.com/bin/common/dropdownlist', method='POST', data=data)
        if model_list is not None:
            models = mo.json()
            for model in models:
                model_type = model.replace(' ', '-').upper()
                data = {
                    'resultType': 'manualandwarranties',
                    'tags': 'my-hyundai:Generic,my-hyundai:{}-HYUNDAI-{},my-hyundai:{}'.format(year, model_type, model_type),
                    'currenturl': 'https://owners.hyundaiusa.com/content/myhyundai/us/en/resources/manuals-warranties.html?intcmp=header%20nav;more%20flyout;text;owners%20manual'
                }
                response = send_request(url=post_url, data=data, method='POST')
                if response is not None:
                    for r in response.json():
                        title = r['dcTitle']
                        description = r['description']
                        pdf_url = 'https://owners.hyundaiusa.com' + r['href']
                        line = [year, 'HYUNDAI', model, 'PDF', title, description, pdf_url]
                        print(line)
                        write_csv(lines=[line], filename=filename)


if __name__ == '__main__':
    post_url = 'https://owners.hyundaiusa.com/bin/common/resourceResult'
    model_list = [
        'Accent',
        'Elantra',
        'Elantra GT',
        'Ioniq-Electric',
        'Ioniq-Hybrid',
        'Ioniq-Plug-In Hybrid',
        'Kona',
        'Kona-EV',
        'Nexo-Fuel-Cell',
        'Palisade',
        'Santa Fe',
        'Sonata',
        'Sonata-Hybrid',
        'Tucson',
        'Veloster',
        'Veloster-N',
        'Venue'
    ]
    filename = 'Hyundai_2015_2020_manuals_pdf.csv'
    csv_header = ['YEAR', 'MAKE', 'MODEL', 'SECTION', 'TITLE', 'DESCRIPTION', 'PDF_URL']
    write_csv(lines=[csv_header], filename=filename)
    main()
