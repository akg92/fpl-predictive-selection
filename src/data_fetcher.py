import json 
import requests
import unicodecsv as csv
def add_additionl_to_all(extra_key,extra_values,original):
    result = []
    for ele in original:
        for key in extra_key:
            ele[key] =  extra_values[key]
        result.append(ele)

    return result


def get_for_id(id):
    base_url = 'https://fantasy.premierleague.com/drf/element-summary/'
    player_url = base_url+id
    data = requests.get(player_url)
    j_data = json.loads(data.text)
    h_data = j_data['history_past']
    return h_data

def get_additional_details():
    details_url = 'https://fantasy.premierleague.com/drf/bootstrap-static'
    data = requests.get(details_url).text
    j_data = json.loads(data)
    result = []
    for ele in j_data['elements']:
        player = {}
        player['first_name'] = ele['first_name']
        player['second_name'] = ele['second_name']
        player['team'] = ele['team_code']
        player['element_type'] = ele['element_type']
        player['id'] = str(ele['id'])
        result.append(player)
    return result


def write_to_csv(file_name,history):
    
    keys = history[0].keys()
    with open(file_name,'w') as f:
        dict_wrtiter =  csv.DictWriter(f,keys)
        dict_wrtiter.writeheader()
        dict_wrtiter.writerows(history)
    
    
def get_all_players(out_file='../fpl_data/data/player_history.csv'):
    result = []
    extra_keys = ['id','first_name','second_name','team','element_type']
    players = get_additional_details()
    for player in players:
        p_hist = get_for_id(player['id'])
        result += add_additionl_to_all(extra_keys,player,p_hist)
    write_to_csv(out_file,result)
    return result

if __name__=='__main__':
    get_all_players()


