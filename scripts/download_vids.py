import csv 
import re 
import requests

#urllib.request.urlretrieve(url_link, 'video_name.mp4') 

# TODO: command line options

data_file = "./data/archive-out-min.csv"

with open(data_file) as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        pattern = "'(.*?)'"
        identifier = re.search(pattern, str(row["identifier"])).group().replace("'", "")
        mp4_link = row["mp4 link"]
        pattern = '(?<=\?)(.*?)(?=\&)'
        timestamp = re.search(pattern, mp4_link).group().replace("/", "-")

        out_file = "./data/mp4/{identifier}_{timestamp}.mp4".format(
            identifier = identifier,
            timestamp = timestamp
        )

        res = requests.get(mp4_link)
        with open(out_file, "wb") as f:
            f.write(res.content)
            print("downloaded {identifier} {timestamp}".format(identifier=identifier, timestamp=timestamp))

