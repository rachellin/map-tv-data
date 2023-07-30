def get_segments_old():
  
  keywords = ["gun", "guns", "firearm", "firearms", "assault rifle", "assault weapon", "shooting", "shootings", "shooter", "shooters", "gunman", "gunmen"]
  # TODO non-keywords
  irrelevant1 = ['blockbuster','movie','actor','actors','actress','director','game','novel','magic','spotify','netflix','concert','concerts','espn','nfl','mlb','album','earnings','hunters','dear','players']
  irrelevant2 = ["spray gun", "flood gun", "emission gun", "nerf gun", "radar gun", "anti-aircraft gun", "starting gun", "water gun", "video game", "machine gun kelly", "guns n roses", "guns n \' roses", "smoking gun", "big guns", "young gun", "under the gun", "jumping the gun", "james bond"]
  non_keywords = irrelevant1 + irrelevant2

  all_video_dicts = {}
  reset_count = 0

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
          # if i == 1092:
          #    break
          # new full video
          print(next(csv_reader) == None)
          if (row["identifier"] != current_identifier):
              if i > 0: # done with full video
                  video_dict["minute_scores"] = minute_scores

                  # apply algorithm to find highest concentration of True/1
                  seg_length = round(sum(minute_scores) * 1.25)
                  if seg_length > len(minute_scores):
                    seg_length = len(minute_scores)

                  # if current_identifier == "b'CSPAN_20220604_052300_Politics_and_Public_Policy_Today'":
                  #    print("len of minute scores: ", len(minute_scores))
                  #    print("seg_length: ", seg_length)
                  #    print(minute_scores)
                  
                  indices = max_density(minute_scores, seg_length)[1]
                  #print(current_identifier, ": ", len(minute_scores))

                  video_dict["relevant_segment"] = indices
                  all_video_dicts[current_identifier] = video_dict
                  #print("done with {} videos: {}".format(i, current_identifier))

              # reset variables for new video
              current_identifier = row["identifier"]
              current_minute = 0
              minute_scores = []
              video_dict = {}
          
          # for this 1-min segment
          transcript = row["text"]
          minute_scores.append(0)
          for word in keywords: # TODO i should make all lowercase just in case there is uppercase
              if word in transcript.lower():
                  minute_scores[current_minute] = 1
                  break
          # TODO set to 0 if includes non-GV keywords
          for word in non_keywords:
             if word in transcript:
                minute_scores[current_minute] = 0
                break

          current_minute += 1
              
  #pprint(all_video_dicts)
  #print(all_video_dicts)

  options = jsbeautifier.default_options()
  options.indent_size = 2
  json_object = jsbeautifier.beautify(json.dumps(all_video_dicts), options)

  # serialize json
  #json_object = json.dumps(all_video_dicts, indent=2)
  
  # write to json file
  with open("segment_vids.json", "w") as outfile:
      outfile.write(json_object)

def get_segments():
  keywords = ["gun", "guns", "firearm", "firearms", "assault rifle", "assault weapon", "shooting", "shootings", "shooter", "shooters", "gunman", "gunmen"]
  # TODO non-keywords
  irrelevant1 = ['blockbuster','movie','actor','actors','actress','director','game','novel','magic','spotify','netflix','concert','concerts','espn','nfl','mlb','album','earnings','hunters','dear','players']
  irrelevant2 = ["spray gun", "flood gun", "emission gun", "nerf gun", "radar gun", "anti-aircraft gun", "starting gun", "water gun", "video game", "machine gun kelly", "guns n roses", "guns n \' roses", "smoking gun", "big guns", "young gun", "under the gun", "jumping the gun", "james bond"]
  non_keywords = irrelevant1 + irrelevant2

  all_video_dicts = {}
  reset_count = 0

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
          # if i == 1092:
          #    break
          # new full video
          if row["identifier"] != current_identifier:
              if i > 0: # done with full video
                  video_dict["minute_scores"] = minute_scores

                  # apply algorithm to find highest concentration of True/1
                  seg_length = round(sum(minute_scores) * 1.25)
                  if seg_length > len(minute_scores):
                    seg_length = len(minute_scores)

                  # if current_identifier == "b'CSPAN_20220604_052300_Politics_and_Public_Policy_Today'":
                  #    print("len of minute scores: ", len(minute_scores))
                  #    print("seg_length: ", seg_length)
                  #    print(minute_scores)
                  
                  indices = max_density(minute_scores, seg_length)[1]
                  #print(current_identifier, ": ", len(minute_scores))

                  video_dict["relevant_segment"] = indices
                  all_video_dicts[current_identifier] = video_dict
                  print("done with {} videos: {}".format(i, current_identifier))

              # reset variables for new video
              current_identifier = row["identifier"]
              current_minute = 0
              minute_scores = []
              video_dict = {}
          
          # for this 1-min segment
          transcript = row["text"]
          minute_scores.append(0)
          for word in keywords: # TODO i should make all lowercase just in case there is uppercase
              if word in transcript:
                  minute_scores[current_minute] = 1
                  break
          # TODO set to 0 if includes non-GV keywords
          for word in non_keywords:
             if word in transcript:
                minute_scores[current_minute] = 0
                break

          current_minute += 1
              
  #pprint(all_video_dicts)
  #print(all_video_dicts)

  options = jsbeautifier.default_options()
  options.indent_size = 2
  json_object = jsbeautifier.beautify(json.dumps(all_video_dicts), options)

  # serialize json
  #json_object = json.dumps(all_video_dicts, indent=2)
  
  # write to json file
  with open("segment_vids.json", "w") as outfile:
      outfile.write(json_object)


def slice_csv(in_file, out_file, segments_file):
  '''
  iterate through segments_file with the keys:
    1. read all rows from in_file that match current video id into a list
    2. subset the list with relevant_segment
    3. append the subsetted list (of dictionaries) into out_dict_list
  '''
  out_dict_list = []

  # read segments_file json
  segments_dict = {}
  with open(segments_file) as json_file:
    segments_dict = json.load(json_file)
  
  videos_list = list(segments_dict.keys())
  #print(len(videos_list)) len = 1763
  #print(videos_list[-1])

  with open(in_file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')

    i = 0
    current_id = videos_list[i]
    current_vid = segments_dict[current_id]
    minute_list = []

    #print(videos_list[1762])
    
    for row_count, row in enumerate(csv_reader):
       # read rows from in_file that match current video id into a list
       if row["identifier"] == current_id:
          #print(i)
          minute_list.append(row)
      
       # done with full video --> subset relevant segment
       #if next(csv_reader) and next(csv_reader)["identifier"] != current_id:
       if row["identifier"] != current_id:
          # if i == 708:
          #    print(row["identifier"])
          #    print(current_id)
          [start, end] = current_vid["relevant_segment"]
          relevant_mins = minute_list[start:end]
          #print("start, end: [", start, ",", end, "]      id: ", current_id)
          out_dict_list.extend(relevant_mins)
          # print("done with {}".format(videos_list[i]))
          # print(i)
          #print("out_dict_list: ", len(out_dict_list), "      id: ", current_id)
          print("minute_list: ", len(minute_list), "    i: ", i, "  id: ", current_id)

          # shouldn't need this because it's supposed to get to the end of the csv...?
          # if i+1 == len(videos_list):
          #    break

          # reset 
          if i+1 < len(videos_list):
            i += 1
          #current_id = videos_list[i]
          current_id = row["identifier"]
          current_vid = segments_dict[current_id] 
          minute_list = []
          relevant_mins = []
          # add first minunte
          minute_list.append(row)

  # copy into new csv 
  with open(out_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = out_dict_list[0].keys(), lineterminator = '\n')
    writer.writeheader()
    writer.writerows(out_dict_list)
    

# TODO: for now, just copying over as single minutes, but maybe want to change the full relevant segment(?)
def slice_csv_ew(in_file, out_file, segments_file):
  out_dict_list = []
  segments_dict = {}

  # read segments_file json
  with open(segments_file) as json_file:
    segments_dict = json.load(json_file)

  with open(in_file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')

    #current_identifier = csv_reader[0]["identifier"]
    current_identifier = next(csv_reader)["identifier"]
    current_video = segments_dict[current_identifier] # video dict from get_segements output
    
    current_minute = 0 
    next_video = False # true if we want to skip until new video

    for i, row in enumerate(csv_reader):
      if i == 108:
         break
      
      if current_minute == 0:
        # skip to the start of the relevant segment
        if current_minute != current_video["relevant_segment"][0]:
          current_minute += 1
          continue

      if current_minute == current_video["relevant_segment"][1]:
        # finished with a video's relevant segment
        print("done with {}".format(current_identifier))
        # temp = [x["identifier"] for x in out_dict_list if x["identifier"] == "b'CSPAN2_20220608_051500_Washington_Journal_Steve_Gutowski'"]
        # print(temp)
        # print(len(temp))
        next_video = True

      # copy over for new csv
      if not next_video:
        out_dict_list.append(row)
        current_minute += 1

      # skip until next video
      # if i == 59:
      #   print(row["identifier"])
      #   print(next(csv_reader)["identifier"])
      #   break
      elif current_identifier != next(csv_reader)["identifier"]:
          next_video = False
          # reset variables
          current_identifier = next(csv_reader)["identifier"]
          current_video = segments_dict[current_identifier]
          current_minute = 0

    with open(out_file, 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames = out_dict_list[0].keys())
      writer.writeheader()
      writer.writerows(out_dict_list)