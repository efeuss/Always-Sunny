# IT'S ALWAYS SUNNY RANDOM EPISODE GENERATOR


def main():
    import pandas as pd
    
    #### PRETTY BORDER ####
    topBorder = ""
    bottomBorder = ""
    
    for i in range(60):
        topBorder += "*"
        
    bottomBorder = topBorder
    
    print(topBorder)
    print("*" + f"{'IT' +chr(39)+'S ALWAYS SUNNY IN PHILADELPHIA':^58}" + "*")
    print("*" + f"{'random unique episode generator':^58}" + "*")
    print(bottomBorder)
    print()
    
    #### BUILDING TABLE OF ALL SEASONS AND EPISODES ####
    #num_seasons of it's always sunny, added this to easily change it per new show
    num_seasons = 16

    seasons = list(range(1,num_seasons+1))
    episodes = [7,10,15,13,12,14,13,10,10,10,10,10,10,10,8,8]
    total = sum(episodes)
    
    all_always = pd.DataFrame(
        {'Season': seasons, 'Episodes': episodes}) 
    #print(all_always)
    # don't really need this, but nice to validate you got it all right
    
    episode_title_list = title_scrape()
    
    #### RETURNING FIRST RANDOM UNIQUE CHOICE EPISODE ####
    #### AND SEEING IF THE USER WANTS IT, IF NOT, SELECTING ANOTHER ####
    random_choice_1 = random_episode_generator(seasons,episodes)
    #pick = random_choice_1
    #print(random_choice_1)
    print(f'SEASON: {random_choice_1[0]}')
    print(f'EPISODE: {random_choice_1 [1]}')
    
    #### CALCULATING RANDOM EPISODE OVERALL EPISODE NUMBER
    #### THEN SENDING THAT INTO THE EPISODE TITLE FUNCTION
    #### THAT WILL RETURN THE EPISODE TITLE
    overall_no = sum(episodes[0:(random_choice_1[0]-1)]) + random_choice_1[1]
    #print(overall_no)
    episode_title = title_search(overall_no, episode_title_list)
    print(f'TITLE: {episode_title}')
    
    wanna_watch = input('Do you want to watch this episode? Y/N: ')
    print()
    
    while wanna_watch != "Y":
        random_choice_n = random_episode_generator(seasons,episodes)
        pick = random_choice_n
        #print(random_choice_n)
        print(f'SEASON: {random_choice_n[0]}')
        print(f'EPISODE: {random_choice_n [1]}')
        overall_no = sum(episodes[0:(random_choice_n[0]-1)]) + random_choice_n[1]
        episode_title = title_search(overall_no, episode_title_list)
        print(f'TITLE: {episode_title}')
        wanna_watch = input('Do you want to watch this episode? Y/N: ')
        print()


    ##### WRITING THE FINAL CHOSEN EPISODE TO THE WATCHED LIST ####
    watched_txt = open('always_watched.txt','a')
    watched_txt.write(str(pick) + '\n')
    watched_txt.close()
    
    ##### GETTING WATCHED LIST EPISODE TOTALS ####
    watched_txt = open('always_watched.txt','r')
    watched = pd.Series(watched_txt)
    watched = watched.replace(r'\n','',regex=True)
    watch_list = list(watched)
    watched_txt.close()

    watch_total = len(watch_list)
    print(f'TOTAL EPISODES IN SERIES: {total}')
    print(f'NUMBER WATCHED: {watch_total}')
    print(f'NUMBER REMAINING: {total - watch_total}')


    #### FUTURE PLAN: ADD WATCHED DATE TO THE WATCHED LIST ####
    
    
def random_episode_generator(s,e):
    # randomly selects an episode from series with seasons & episodes
    # validates against watched list
    # returns unique random selection
    import random
    import pandas as pd
    
    # using random selection to pick out of initial available episodes
    choice_season = random.choice(s)
    #print(f'SEASON: {choice_season}')
    
    choice_episode = random.choice(range(1,e[choice_season-1]+1))
    #print(f'EPISODE: {choice_episode}')
    
    choice = choice_season, choice_episode
    
    # importing watch list into the program so we can later validate
    watched_txt = open('always_watched.txt','r')
    watched = pd.Series(watched_txt)
    watched = watched.replace(r'\n','',regex=True)
    watch_list = list(watched)
    watched_txt.close()
    
    if choice in watch_list:
        choice_n = random_episode_generator(seasons,episodes)
        random_choice = choice_n
    else:
        random_choice = choice
    
    return random_choice

def title_scrape():
    import requests
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    import time
    import numpy as np

    url='https://en.wikipedia.org/wiki/List_of_It%27s_Always_Sunny_in_Philadelphia_episodes'
    response = requests.get(url)
    page = response.text
    soup = bs(page, "html.parser")
    
    epies = soup.find_all(class_='wikitable plainrowheaders wikiepisodetable')
    
    e_list = []

    for season in epies:
        for rows in season.find_all(class_="vevent"):
            overall = rows.find("th").text
            no_season = rows.find("td").text
            title = rows.find(class_="summary").text
            e_list.append([overall, no_season, title])
            
    episode_list = pd.DataFrame(e_list)
    episode_list.columns = ['Overall', 'Season', 'Title']
            
    return episode_list

    # this is a little messed up, ep 70 and 71 bundled so overall 71 is missing


def title_search(overall_number, epi_list):
    import pandas as pd
    
    #print(episode_list)

    random_episode = str(overall_number)
    episode_list = epi_list
    #print(random_episode_overall) - this part is correct
    
    title = episode_list[episode_list.Overall==random_episode].Title.item()
    #print(title)
    
    return title
    
main()
 


