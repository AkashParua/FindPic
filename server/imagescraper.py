import os
import requests
from bs4 import BeautifulSoup

def download_images(url, folder):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Fetch webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image tags
    images = soup.find_all('img')
    # Download each image
    for img in images :
        src = img.get('src')
        if src.endswith('jpg'):
            src = 'https:'+ src
            print(src)
            filename = os.path.join(folder, src.split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(src).content)
                
#download_images('https://imgflip.com/memetemplates','ScrapedImages')
for i in range(22,50):
    download_images(f'https://imgflip.com/memetemplates?page={i}', 'ScrapedImages')
