import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def login(url, username, password):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)

        # Wait and locate login elements
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$MainContent$username')))
        password_field = driver.find_element(By.NAME, 'ctl00$MainContent$password')
        login_button = driver.find_element(By.NAME, 'ctl00$MainContent$Submit1')

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        print("Login button clicked. Assuming login is successful.")
        return driver

    except Exception as e:
        print(f"Login failed. Exception type: {type(e)}")
        print(f"Exception details: {e}")
        driver.quit()
        return None

if __name__ == '__main__':
    login_url = 'https://studentvue.vbcps.com/PXP2_Login_Student.aspx?regenerateSessionId=True'

    with open('logins.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            username = row[0]
            password = row[1]
            
            logged_in_driver = login(login_url, username, password)

            if logged_in_driver:
                try:
                    # Navigate to student info page
                    student_info_link = logged_in_driver.find_element(By.LINK_TEXT, 'Student Info')
                    student_info_link.click()

                    WebDriverWait(logged_in_driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'info_tbl'))
                    )

                    from bs4 import BeautifulSoup
                    page_source = logged_in_driver.page_source
                    soup = BeautifulSoup(page_source, 'html.parser')

                    data = {}

                    # Extract data from info tables
                    info_tables = soup.find_all('table', class_='info_tbl')
                    for table in info_tables:
                        rows = table.find_all('tr')
                        for row in rows:
                            cells = row.find_all('td')
                            for cell in cells:
                                label_span = cell.find('span', class_='tbl_label')
                                if label_span:
                                    label = label_span.text.strip()
                                    value = cell.text.replace(label, '').strip()
                                    if label:
                                        data[label] = value
                    
                    data['Password'] = password

                    # Save data to CSV
                    output_dir = 'student_data'
                    os.makedirs(output_dir, exist_ok=True)

                    student_name = data.get('Student Name', 'student')
                    filename = os.path.join(output_dir, f"{student_name.replace(' ', '_').lower()}.csv")

                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Field', 'Value'])
                        for key, value in data.items():
                            writer.writerow([key, value])

                    print(f"Successfully scraped student information and saved it to {filename}")

                finally:
                    logged_in_driver.quit()
