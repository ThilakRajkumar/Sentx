import requests
import time

API_KEY = 'e12e81636979414f0e10cf787195adcfca205062c460746db33dd0cffbce42ea'
BASE_URL = 'https://www.virustotal.com/api/v3'


def upload_file_and_get_scan_id(file):
    headers = {'x-apikey': API_KEY}
    response = requests.post(f'{BASE_URL}/files', headers=headers, files={'file': (file.filename, file.stream.read())})
    if response.status_code == 200:
        return response.json()['data']['id']
    else:
        print("Error uploading file:", response.text)
        return None


def get_file_report(scan_id):
    headers = {'x-apikey': API_KEY}
    for _ in range(10):  # Poll up to 10 times until ready
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
                    'total_vendors': total_vendors,
                    'filename': scan_id
                }
        time.sleep(3)
    return None


def scan_file_vt(file):
    scan_id = upload_file_and_get_scan_id(file)
    if scan_id:
        return get_file_report(scan_id)
    return None
