import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://replicate.com'
TARGET_URL = BASE_URL + '/explore'


def fetch_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Ensure correct character encoding
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_github_link(url):
    soup = fetch_soup(url)
    github_link_elem = soup.select_one('body > main > header > hgroup > ul > li:nth-child(3) > a')
    if github_link_elem:
        return github_link_elem['href']
    return None  # Return None if the GitHub link is not found


def main():
    soup = fetch_soup(TARGET_URL)
    collections = soup.select('#collections > div > div')

    # Create empty lists to store data
    titles = []
    title_descriptions = []
    links = []
    inner_models = []
    inner_model_descriptions = []
    github_links = []

    for collection in collections:
        title = collection.select_one('div.overflow-hidden > h4 > a').text.strip()
        title_description = collection.select_one('div.overflow-hidden > p:nth-child(2)').text.strip()
        link = BASE_URL + collection.select_one('div.overflow-hidden > h4 > a')['href']

        inner_soup = fetch_soup(link)
        models = inner_soup.select('body > main > div > div > a')

        for model in models:
            inner_model = model['href']
            inner_model_description = model.select_one('div:nth-child(2) > p').text.strip()

            # Fetch the GitHub link
            github_link = get_github_link(BASE_URL + inner_model)

            # Append the data to the lists
            titles.append(title)
            title_descriptions.append(title_description)
            links.append(link)
            inner_models.append(inner_model)
            inner_model_descriptions.append(inner_model_description)
            github_links.append(github_link)

    # Create a pandas DataFrame
    df = pd.DataFrame({
        'Title': titles,
        'Title Description': title_descriptions,
        'Link': links,
        'Inner Model': inner_models,
        'Inner Model Description': inner_model_descriptions,
        'GitHub Link': github_links
    })

    return df


if __name__ == '__main__':
    dataframe = main()
    # display(dataframe)  # This will display the DataFrame in Jupyter notebook

    dataframe.to_csv('output_df.csv')
