import os
import csv 

# check the number of files in directory
def count_files():
    count = 0
    dir_path = r'C:\Users\lynns\coding\corners\map-tv-data\data\meta'
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


with open('./data/full-grab-check.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    wrong_count = 0
    vid_count = -1
    for row in csv_reader:
        vid_count += 1
    print("total videos for full grab: ", vid_count)


full_file = open("./data/full-grab-check.csv", "r")
full_data = list(csv.reader(full_file, delimiter=","))
full_file.close()
full_data = [x[0] for x in full_data[1:]]

crawler_file = open("./tvscraper/one-month-check.csv", "r")
crawler_data = list(csv.reader(crawler_file, delimiter=","))
crawler_file.close()
crawler_data = [x[0] for x in crawler_data[1:]]

print("# of videos missing from full grab: ", len(list(set(crawler_data) - set(full_data))))

print(len(full_data))
print(len(set(full_data)))

print(len(crawler_data))
print(len(set(crawler_data)))