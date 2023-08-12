import csv
from collections import defaultdict
from pprint import pprint
import json
import jsbeautifier

'''
to check whether current row in csv is the same video:
- variable to keep track of current identifier
- if identifier of the current row is different, create new list (filled with False) and change the prev variable

for each 1-min segment:
1. get transcript from 'text' column
2. set to True for current 1-min if includes at least one of the keywords
3. write the T/F value to the csv (prob not if using the clustering method)

after done with a whole video:
1. save the T/F list to... somewhere ? (maybe create)
    - this is suggesting that maybe a new row for each 1-minute segment is not a good idea...?
2. algorithm to determine the segment of the whole video that is about gun violence
3. 

keyword_check = {
    "insert identifier": ([True, False, False, True, True, True, False...], [3, 8])
}
^ each video is a tuple
- first item: list of T/F 
- second item: list where first item is start of segment and second item is end of segment

video_dict_list = {
    "identifier": {
        "minute_scores": [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0...],
        "relevant_segment": (start_index, end_index)
    },
    ...
}

JSON version of the CSV:
"video": {

}

'''

def max_density(parent_list, sl_length):
  sublists = []

  for i in range(0, len(parent_list)-sl_length+1):
    sl = parent_list[i:i+sl_length]
    indices = (i, i+sl_length)
    sublists.append((sl, indices))
  #print(sublists)
  max_sl = (sublists[0], sum(sublists[0][0]))
  i = 1
  while i < len(sublists):
    if sum(sublists[i][0]) > max_sl[1]:
      max_sl = (sublists[i], sum(sublists[i][0]))
    i += 1
  
  return max_sl[0]

def group_videos(file):
  grouped_videos = defaultdict(list)  # each entry of the dict is, by default, an empty list

  with open(file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for i, row in enumerate(csv_reader):
      grouped_videos[row["identifier"]].append(row)

  return grouped_videos

def score_minute(row, minute_scores, current_minute):
  keywords = ["gun", "guns", "firearm", "firearms", "assault rifle", "assault weapon", "shooting", "shootings", "shooter", "shooters", "gunman", "gunmen"]
  # TODO non-keywords
  irrelevant1 = ['blockbuster','movie','actor','actors','actress','director','game','novel','magic','spotify','netflix','concert','concerts','espn','nfl','mlb','album','earnings','hunters','dear','players']
  irrelevant2 = ["spray gun", "flood gun", "emission gun", "nerf gun", "radar gun", "anti-aircraft gun", "starting gun", "water gun", "video game", "machine gun kelly", "guns n roses", "guns n \' roses", "smoking gun", "big guns", "young gun", "under the gun", "jumping the gun", "james bond", "top gun"]
  non_keywords = irrelevant1 + irrelevant2

  # for this 1-min segment
  transcript = row["text"]
  minute_scores.append(0)
  for word in keywords: # TODO i should make all lowercase just in case there is uppercase
      if word in transcript.lower().split():
          minute_scores[current_minute] = 1
          break
  # TODO set to 0 if includes non-GV keywords
  for word in non_keywords:
      if word in transcript.lower().split():
        minute_scores[current_minute] = 0
        break
  return minute_scores

# TODO restructure this function
def get_segments(grouped_videos):
  all_video_dicts = {}

  # dict_keys = list(grouped_videos.keys())
  # print(len(dict_keys))
  # print(grouped_videos[dict_keys[-1]])

  '''
  all_video_dicts is a dictionary of lists
    key: identifier
    value: list of dictionaries
      each dictionary = a row for each minute of that video 

  algorithm: loop through all_video_dicts using the keys; so for each key 
    1. for each dict in the list: score the minute 
    2. add minute_scores to video_dict
    3. calculate the segment length
    4. apply max_density algorithm
    5. add relevant_segment to video_dict
    6. add video dict to all_video_dicts
  '''
  # print("starting to score minutes")

  for vid_count, id in enumerate(grouped_videos.keys()):
    video_dict = {}
    minute_scores = []
    for i, minute in enumerate(grouped_videos[id]):
      minute_scores = score_minute(minute, minute_scores, i)
    video_dict["minute_scores"] = minute_scores
    # apply algorithm to find highest concentration of True/1
    seg_length = round(sum(minute_scores) * 1.25)
    if seg_length > len(minute_scores):
      seg_length = len(minute_scores)
    indices = max_density(minute_scores, seg_length)[1]
    video_dict["relevant_segment"] = indices
    all_video_dicts[id] = video_dict
    print("done with {} videos: {}".format(vid_count, id))

  options = jsbeautifier.default_options()
  options.indent_size = 2
  json_object = jsbeautifier.beautify(json.dumps(all_video_dicts), options)
  
  # write to json file
  with open("segment_vids2.json", "w") as outfile:
    outfile.write(json_object)

  return grouped_videos


def slice_csv(grouped_videos, out_file, segments_file):
  '''
  iterate through grouped_videos dictionary with the keys -- for each key:
    1. subset the list with relevant segment
    2. append the subsetted list (of dictionaries) into out_dict_list
  '''
  out_dict_list = []
  # read segments_file json
  segments_dict = {}
  with open(segments_file) as json_file:
    segments_dict = json.load(json_file)

  for vid_count, id in enumerate(grouped_videos.keys()):
    [start, end] = segments_dict[id]["relevant_segment"]
    minute_list = grouped_videos[id]
    relevant_mins = minute_list[start:end]
    out_dict_list.extend(relevant_mins)
    print("done with {} videos: {}".format(vid_count+1, id))
    
  # copy into new csv 
  with open(out_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = out_dict_list[0].keys(), lineterminator = '\n')
    writer.writeheader()
    writer.writerows(out_dict_list)


# throw out irrelevant videos after slicing for relevant segments
def filter_videos(in_file):
  irrelevant1 = ['blockbuster','movie','film','actor','actors','actress','director','game','novel','magic','spotify','netflix','concert','concerts','espn','nfl','mlb','album','earnings','hunters','dear','players']
  irrelevant2 = ["spray gun", "flood gun", "emission gun", "nerf gun", "radar gun", "anti-aircraft gun", "starting gun", "water gun", "video game", "machine gun kelly", "guns n roses", "guns n \' roses", "smoking gun", "big guns", "young gun", "under the gun", "jumping the gun", "james bond", "top gun"]
  non_keywords = irrelevant1 + irrelevant2
  '''
  step 1: throw out videos that don't meet certain minimum for relevant segment length (# or percentage) TODO
  step 2: throw out videos that meet minimum density of exclusionary keywords 
  step 3: write to new csv

  step 2: for each id in grouped_videos
    1. for each minute, update keyword_count for the # of exclusionary keywords
    2. if keyword_count does NOT meet threshold, add to final_videos
  '''
  # TODO: maybe i don't need to write to csv in slice_csv if i'm just going to use it to create another new csv...?
  # TODO: videos with relevant segment [0:0] should be thrown out by default but check that the seth meyers video isn't there
  final_videos = []
  grouped_videos = group_videos(in_file)

  scrapped_list = []

  # throw out videos that meet minimum density of exclusionary keywords 
  # counts the number of minutes with exclusionary keywords
  for vid_count, id in enumerate(grouped_videos.keys()):
    keyword_count = 0
    keywords = []
    for i, minute in enumerate(grouped_videos[id]):
      for word in non_keywords:
        if word in minute["text"].lower().split():
          keyword_count += 1
          keywords.append(word)
          break
    # TODO: change threshold
    if (keyword_count/len(grouped_videos[id])) < 0.5:
      final_videos.extend(grouped_videos[id])
    else:
      scrapped_list.append(id)
      print(id)
      print(keywords, "\n\n")
    #print("done with {} videos: {}".format(vid_count+1, id))

  print("\n\n {} total videos".format(len(final_videos)))
  # for x in scrapped_list:
  #   print(x)
  print("{} scrapped".format(len(scrapped_list)))


      
   
#grouped_videos = group_videos('./data/june-2022-week.csv')
#get_segments(grouped_videos)        
#slice_csv(grouped_videos, "./data/june-2022-week-sliced.csv", "segment_vids.json")
filter_videos("./data/june22-sliced.csv")