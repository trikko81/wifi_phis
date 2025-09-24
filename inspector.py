
import requests
from bs4 import BeautifulSoup

url = 'https://studentvue.vbcps.com/PXP2_Login_Student.aspx?regenerateSessionId=True'

try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    inputs = soup.find_all('input')
    
    for input_tag in inputs:
        print(f"Name: {input_tag.get('name')}, Type: {input_tag.get('type')}, Value: {input_tag.get('value')}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching page: {e}")
