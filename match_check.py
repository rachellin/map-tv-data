import csv 
import json
import re 

with open('june22-matches.txt') as f:
    lines = f.readlines()

# print([x.strip() for x in lines[2].split(None, 1)])

def create_eval_csv():
    out_data = []

    for i, match in enumerate(lines):
        split_line = [x.strip() for x in match.split(None, 1)]
        out_data.append({
            "identifier": split_line[0],
            "matched incident(s)": split_line[1]
        })
        print("done with {} videos".format(i))

    with open("june22-matches.csv", 'w') as csv_file:
        fieldnames = ["identifier", "matched incident(s)"]
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames, lineterminator = '\n')
        writer.writeheader()
        writer.writerows(out_data)


def get_matches():
    matches = []
    for i, match in enumerate(lines):
        split_line = [x.strip() for x in match.split(None, 1)]
        id = split_line[0]
        matches.append(id)
    return matches


def get_all(segments_file):
    all_videos = []
    segments_dict = {}
    with open(segments_file) as json_file:
        segments_dict = json.load(json_file)

    for id in segments_dict.keys():
        pattern = r"b'"
        replacement = ''
        cleaned_id = re.sub(pattern, replacement, id)
        cleaned_id = cleaned_id.replace("'", "")
        all_videos.append(cleaned_id)

    return all_videos



all_videos = get_all("./data/june22-segments.json")
matched = get_matches()
unmatched = list(set(all_videos) - set(matched))
#print(len(unmatched))

out_data = []
for video in unmatched:
    out_data.append({
            "identifier": video
        })
    
with open("june22-unmatched.csv", 'w') as csv_file:
    fieldnames = ["identifier"]
    writer = csv.DictWriter(csv_file, fieldnames = fieldnames, lineterminator = '\n')
    writer.writeheader()
    writer.writerows(out_data)