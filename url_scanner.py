import requests
import time

API_KEY = 'e12e81636979414f0e10cf787195adcfca205062c460746db33dd0cffbce42ea'
BASE_URL = 'https://www.virustotal.com/api/v3'


def scan_url_and_get_scan_id(url):
    headers = {'x-apikey': API_KEY}
    response = requests.post(f'{BASE_URL}/urls', headers=headers, data={'url': url})
    if response.status_code == 200:
        return response.json()['data']['id']
    else:
        print("Error scanning URL:", response.text)
        return None


def get_url_report(scan_id):
    headers = {'x-apikey': API_KEY}
    for _ in range(10):  # Poll until ready
        response = requests.get(f'{BASE_URL}/analyses/{scan_id}', headers=headers)
        if response.status_code == 200:
            data = response.json()['data']['attributes']
            if data['status'] == 'completed':
                scan_report = data['results']
                detected_count = sum(1 for details in scan_report.values() if details['category'] == 'malicious')
                total_vendors = len(scan_report)
                return {
                    'scan_report': scan_report,
                    'detected': detected_count,
                    'total_vendors': total_vendors
                }
        time.sleep(3)
    return None


def scan_url_vt(url):
    scan_id = scan_url_and_get_scan_id(url)
    if scan_id:
        return get_url_report(scan_id)
    return None
