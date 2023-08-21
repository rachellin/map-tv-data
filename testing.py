import os
import csv 
import json

# check the number of files in directory
def count_files():
    count = 0
    dir_path = r'C:\Users\lynns\coding\corners\map-tv-data\data\meta-june22'
    #dir_path = r'{}'.format(path)
    for path in os.scandir(dir_path):
        if path.is_file():
            count += 1
    print('file count:', count)

count_files()


# with open('./data/archive-out.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     wrong_count = 0
#     for row in csv_reader:

#         line_count += 1

    #     if line_count > 0:
    #         if not row[0] == '4:3':
    #             print("not aspect ratio: ", line_count)
    #             wrong_count += 1
    #     line_count += 1
    # #print(f'Processed {line_count} lines.\n')
    # print("{} lines out of {} total lines are wrong".format(line_count, wrong_count))

# for row in csv.DictReader(open('./data/archive-out.csv')):
#   print(row)


# with open('./data/full-grab-check.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     wrong_count = 0
#     vid_count = -1
#     for row in csv_reader:
#         vid_count += 1
#     print("total videos for full grab: ", vid_count)


# full_file = open("./data/full-grab-check.csv", "r")
# full_data = list(csv.reader(full_file, delimiter=","))
# full_file.close()
# full_data = [x[0] for x in full_data[1:]]

# crawler_file = open("./tvscraper/one-month-check.csv", "r")
# crawler_data = list(csv.reader(crawler_file, delimiter=","))
# crawler_file.close()
# crawler_data = [x[0] for x in crawler_data[1:]]

# print("# of videos missing from full grab: ", len(list(set(crawler_data) - set(full_data))))

# print(len(full_data))
# print(len(set(full_data)))

# print(len(crawler_data))
# print(len(set(crawler_data)))

keywords = ["gun", "guns", "firearm", "firearms", "assault rifle", "assault weapon", "shooting", "shootings", "shooter", "gunman", "gunmen"]
minute_scores = []

# with open('./data/june-2022-week.csv') as csv_file:
#     #csv_reader = csv.reader(csv_file, delimiter=',').readlines()[1:141]
#     #csv_reader = csv_file.readlines()[0:141]
#     csv_reader = csv.DictReader(csv_file, delimiter=',')
#     for i, row in enumerate(csv_reader):
#         if i == 321:
#             transcript = row["text"]
#             minute_scores.append(0)
#             print(transcript)
#             for word in keywords: # TODO i should make all lowercase just in case there is uppercase
#                 if word in transcript:
#                     minute_scores[0] = 1
#                     break
#             print(minute_scores)


# with open('./data/june-2022-week.csv') as csv_file:
#     #csv_reader = csv.reader(csv_file, delimiter=',').readlines()[1:141]
#     #csv_reader = csv_file.readlines()[0:141]
#     csv_reader = csv.DictReader(csv_file, delimiter=',')
#     #csv_reader = csv.reader(csv_file, delimiter=',')
#     for i, row in enumerate(csv_reader):
#         # if i >= 4528 and i <= 4571:
#         #     print(row["text"], "\n")
#         if row["identifier"] != "b'CNNW_20220602_020000_Don_Lemon_Tonight'":
#         #for skip in range(61+42):
#             next(csv_reader)
#             print(i)


# validation check for segment_vids
def validate_segment_vids(segment_json):
    segments_dict = {}
    with open(segment_json) as json_file:
        segments_dict = json.load(json_file)

    print(segments_dict[list(segments_dict.keys())[-1]])
    minute_count = 0
    for i, id in enumerate(segments_dict.keys()):
        [start, end] = segments_dict[id]["relevant_segment"]
        minute_count += (end - start)

    print(minute_count)

    # TODO compare with length of csv instead of manual
            
#validate_segment_vids('segment_vids.json')