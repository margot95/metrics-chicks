import json
import regex as re

# File paths
json_file_path = '../create_embeddings/pdfs_new.json'

months_all_languages = [
    'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
    'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre',
    'januar', 'februar', 'märz', 'april', 'Mai', 'juni',
    'juli', 'august', 'september', 'oktober', 'november', 'dezember',
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
]

data = None
with open(json_file_path, 'r') as file:
    data = json.load(file)

def cleaning_law_text(data):
    for key1 in data.keys():
        for key2 in data[key1].keys():
            if key2 == 'content':
                data[key1][key2] = data[key1][key2].lower().strip()
                #delete special de characters
                data[key1][key2] = data[key1][key2].replace('\u00c4','ä').replace('\u00fc','ü').replace('\u00f6','ö')
                data[key1][key2] = data[key1][key2].replace('\u2013','-')
                data[key1][key2] = data[key1][key2].replace('_','')
                #delete special fr characters
                data[key1][key2] = data[key1][key2].replace('\u00c9','é').replace('\u00e9','é').replace('\u00e0','à').replace('\u00e8','è').replace('\u00c8','è').replace('\u00e2','â').replace('\u00e7','ç').replace('\u00ee','î').replace('\u00f4','ô').replace('\u00fb','û').replace('\u00ea','ê')
                #section sign
                data[key1][key2] = data[key1][key2].replace('\u00a7','')

                #delete addresses
                pattern = re.compile(r'\b(\d+\s+[A-Za-z/]{4,}\s+\d+)\b')
                matches = pattern.findall(data[key1][key2])
                for match in matches:
                    #if match is not a date
                    if not any(month in match for month in months_all_languages):
                        data[key1][key2] = data[key1][key2].replace(match,'')
    # Write the modified data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

cleaning_law_text(data)