import csv
from pprint import pprint

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

  max_sl = (sublists[0], sum(sublists[0][0]))
  i = 1
  while i < len(sublists):
    if sum(sublists[i][0]) > max_sl[1]:
      max_sl = (sublists[i], sum(sublists[i][0]))
    i += 1
  
  return max_sl[0]

keywords = ["gun", "guns", "firearm", "firearms", "assault rifle", "assault weapon", "shooting", "shootings", "shooter", "shooters", "gunman", "gunmen"]
# TODO non-keywords

all_video_dicts = {}

with open('./data/june-2022-week.csv') as csv_file:
    #csv_reader = csv.reader(csv_file, delimiter=',').readlines()[1:141]
    #csv_reader = csv_file.readlines()[0:141]
    csv_reader = csv.DictReader(csv_file, delimiter=',')
   # csv_reader = [row for idx, row in enumerate(csv_reader) if idx in range(307,368)]

    video_dict = {}
    current_identifier = ""
    current_minute = 0
    minute_scores = []

    for i, row in enumerate(csv_reader):
        if i == 368:
           break
        # new full video
        if row["identifier"] != current_identifier:
            if i > 0: # done with full video
                video_dict["minute_scores"] = minute_scores

                # apply algorithm to find highest concentration of True/1
                seg_length = round(sum(minute_scores) * 1.25)
                indices = max_density(minute_scores, seg_length)[1]

                video_dict["relevant_segment"] = indices
                all_video_dicts[current_identifier] = video_dict

            # reset variables for new video
            current_identifier = row["identifier"]
            current_minute = 0
            minute_scores = []
        
        # for this 1-min segment
        transcript = row["text"]
        minute_scores.append(0)
        for word in keywords: # TODO i should make all lowercase just in case there is uppercase
            if word in transcript:
                minute_scores[current_minute] = 1
                break
        # TODO set to 0 if includes non-GV keywords


        current_minute += 1
            
#pprint(all_video_dicts)
print(all_video_dicts)