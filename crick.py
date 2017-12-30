import requests
import pynotify
from time import sleep
from pycricbuzz import Cricbuzz
import json
import time

c = Cricbuzz()

def allmatches():
    m_data = c.matches()
    matches = []
    for match in m_data:
        matches.append(match['mchdesc'])
    return matches

def id_matches(match_description):
    m_data = c.matches()
    for match in m_data:
        if (match['mchdesc'].title() == match_description):
            return match['id']
    else:
        return None

def full_score(match_description):
    match_id = id_matches(match_description)
    match_full_score = c.scorecard(match_id)
    fullscore = {}
    fullscore['minfo'] = "{}, {}".format(match_full_score['matchinfo']['mchdesc'],match_full_score['matchinfo']['mnum'])
    fullscore['status'] = "{}, {}".format(match_full_score['matchinfo']['mchstate'].title(), match_full_score['matchinfo']['status'])
    fullscore['series'] = "{}".format(match_score['matchinfo']['srs'])
    
    fullscore['score'] = match_full_score['scorecard']

    data = ''
    data += fullscore['minfo'] + score['series'] + '\n' + fullscore['status'] + '\n\n'

    for score in reversed(fullscore['score']):
        data+= "{} {}\n{}/{} in {} overs\n".format(score['inngdesc'],score['batteam'],score['runs'],score['wickets'],score['overs']              )

        data+= "\nBatting\n"
        data+= "{:<20} {:<5} {:<5} {:<5} {}\n\n".format('Name','R','B','4s','6s')

        for batting in score['batcard']:
            data+= "{:<20} {:<5} {:<5} {:<5} {}\n\n".format(batting['name'],batting['runs'],batting['balls'],batting['fours'],batting['six'],batting['dismissal'])


        data+= '\nBowling\n'
        data += "{:<20} {:<5} {:<5} {:<5} {}\n\n".format('Name', 'O', 'M', 'R', 'W')
        for bowling in score['bowlcard']:
            data+= "{:<20} {:<5} {:<5} {:<5} {}\n\n".format(bowling['name'],bowling['overs'],bowling['maidens'],bowling['runs'],bowling['wickets']                                           )

    return data

def live_score(match_description):
    match_id = id_matches(match_description)
    match_score = c.livescore(match_id)
    score = {}
    score['minfo'] = "{}, {}".format(match_score['matchinfo']['mchdesc'],match_score['matchinfo']['mnum'])
    score['status'] = "{}, {}".format(match_score['matchinfo']['mchstate'].title(),match_score['matchinfo']['status'])
    score['series'] = "{}".format(match_score['matchinfo']['srs'])

    score['batting'] = match_score['batting']
    score['bowling'] = match_score['bowling']

    data = ''
    data+= score['minfo'] + score['series'] + '\n' + score['status']+'\n\n'
    data+= score['batting']['team'] + '\n'

    # print data

    for runs in reversed(score['batting']['score']):
            data+= "{} :- {}/{} in {} overs\n".format(runs['desc'],runs['runs'],runs['wickets'],runs['overs'])

    for batsman in reversed(score['batting']['batsman']):
        data += "{} : {}({}) \n".format(batsman['name'], batsman['runs'], batsman['balls'])

    for bowler in reversed(score['bowling']['bowler']):
        data+= "{} : {}/{} \n".format(bowler['name'],bowler['wickets'],bowler['runs'])

    return data


def commentary(match_description):
    match_id = id_matches(match_description)
    match_ct = c.commentary(match_id)
    ct = {}
    ct['minfo'] = "{}, {}".format(match_ct['matchinfo']['mchdesc'], match_ct['matchinfo']['mnum'])
    ct['status'] = "{}, {}".format(match_ct['matchinfo']['mchstate'].title(), match_ct['matchinfo']['status'])
    ct['series'] = "{}".format(match_ct['matchinfo']['srs'])
    ct['commentary'] = match_ct['commentary']

    data = ''
    data += ct['minfo'] + ct['series'] + '\n' + ct['status'] + '\n\n'
    for cty in ct['commentary']:
        data+= "{}\n".format(cty)

    return data

def main():
    print('\nMatch List')
    matches = allmatches()
    m=1
    for i in matches:
        print("{}. {}".format(m,i))
        m+=1

    choice = int(input('\nEnter the choice of your match: '))
    while (choice < 1 or choice > len(matches)):
        print('\nWrong choice')
        choice = int(input('\nEnter the choice of your match again: '))

    match_description = matches[choice-1].title()#indexing from 0

    print ('1. Live Score 2. Full Score Card 3. Commentary')

    choice = int(input('\nEnter your choice: '))

    while (choice < 1 or choice > len(matches)):
        print('\nWrong choice')
        choice = int(input('\nEnter the your choice again: '))

    print('\n')
    if choice == 1:
        value = 'yes'
        while value == 'yes':
            print(live_score(match_description))
            a = live_score(match_description)
            pynotify.init('Cricket Score')
            n=pynotify.Notification('Cricket Score',a)
            n.show()
            time.sleep(30)

    elif choice == 2:
        value = 'yes'
        while value == 'yes':
            print(full_score(match_description))
            fs = full_score(match_description)
            value = 'no'
    else:
        value = 'yes'
        while value == 'yes':
            print(commentary(match_description))  # getting the score of particular match
            cm = commentary(match_description)
            value = 'no'


if __name__ == '__main__':
    main()