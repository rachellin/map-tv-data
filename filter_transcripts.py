import csv

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

'''

with open('./data/archive-out-min2.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')