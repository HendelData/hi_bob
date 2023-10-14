import httplib2
import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import re

# CREATE BLANK DATAFRAME
df = pd.DataFrame(columns=['Episode Title', 'Bob Count', 'Hi Bob Count', 'Drinks'])

# GET DATA FROM SCRIPTMOCHI
http = httplib2.Http()
mochi = "https://scriptmochi.com/tv-series/the-bob-newhart-show"

status, response = http.request(mochi)

r = requests.get(mochi)
r_html = r.text

# RUN THROUGH BEAUTIFUL SOUP
soup = BeautifulSoup(r_html, features="html.parser")

for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
    # GET LIST OF URLs FOR EACH EPISODE
    if link.has_attr('href'):
        if len(link['href']) > 41:
            url = "https://scriptmochi.com" + link['href']

            # GET THE TITLE OF THE EPISODE
            r2 = requests.get(url)
            r2_html = r2.text
            soup2 = BeautifulSoup(r2_html, features="html.parser")

            title = soup2.findAll('h1')
            for row in title:
                episode = row.text[5:]
                ep_number = row.text[0:2]

            # READ TEXT FROM THE SCRIPT
            response = requests.get(url)
            text = BeautifulSoup(response.text, features="html.parser")
            result = text.text

            # GET SEASON NUMBER
            html = requests.get(url).text
            season_number = re.findall(r'#session\d+', html)[0][-1:]

            # FIND START POSITION OF THE SCRIPT
            script_start_location = len(episode) + 1
            script = result[script_start_location:].upper()

            # COUNT THE NUMBER  OF 'BOB' AND 'HI, BOB'
            Bob_count = script.count('BOB')
            Hi_Bob_count = script.count('HI, BOB')
            Bob = Bob_count - Hi_Bob_count
            total_drinks = Bob_count + Hi_Bob_count
            episode = "S0" + season_number + "E" + ep_number + " " + episode

            # WRITE TO DATAFRAME
            df.loc[len(df.index)] = [episode, Bob, Hi_Bob_count, total_drinks]


# REPLACE INCORRECT LINKS
def get_scripts(url, episode_title, index_num):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', {'class': 'content'}).text.strip().upper()

    Bob_count = content.count('BOB')
    Hi_Bob_count = content.count('HI, BOB')
    Bob = Bob_count - Hi_Bob_count
    total_drinks = Bob_count + Hi_Bob_count

    df.loc[index_num] = [episode_title, Bob, Hi_Bob_count, total_drinks]


get_scripts('https://transcripts.foreverdreaming.org/viewtopic.php?p=197222',
            "S01E15 Let's Get Away from It Almost", 14)
get_scripts('https://transcripts.foreverdreaming.org/viewtopic.php?t=83476',
            "S02E14 T.S. Elliot", 37)
get_scripts('https://transcripts.foreverdreaming.org/viewtopic.php?t=83479',
            "S02E17 The Modernization of Emily", 40)
get_scripts('https://transcripts.foreverdreaming.org/viewtopic.php?t=83364',
            "S03E18 The Way We Weren't", 65)
get_scripts('https://transcripts.foreverdreaming.org/viewtopic.php?t=83810',
            "S04E10 Seemed Like a Good Idea at the Time", 81)
get_scripts('https://transcripts.foreverdreaming.org/viewtopic.php?t=83070',
            "S05E02 Caged Fury", 97)
get_scripts('https://transcripts.foreverdreaming.org/viewtopic.php?t=83076',
            "S05E08 A Crime Most Foul", 103)
get_scripts('https://transcripts.foreverdreaming.org/viewtopic.php?t=83280',
            "S05E24 You're Having My Hartley", 119)
get_scripts('https://transcripts.foreverdreaming.org/viewtopic.php?t=83395',
            "S06E22 Happy Trails to You", 140)

# SORT THE DATA
df.sort_values(by=['Drinks', 'Bob Count'], inplace=True, ascending=False)
df.reset_index(drop=True, inplace=True)

# WRITE THE DATA TO A CSV FILE
df.to_csv('C:/Users/marce/Documents/Python/SWD/Bob/bob.csv')
