import csv

with open('test1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    links = []
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            links.append(row[0])
            line_count += 1
    print(f'Processed {line_count} lines.\n')

def check_dups(lst):
  seen = []
  # dups = []
  dup_idx = []
  for idx, item in enumerate(lst):
    if item in seen:
      dup_idx.append(idx)
    else:
      seen.append(item)
  return dup_idx

def check_consec(lst):
  for i, num in enumerate(lst):
    if i > 0 and num != lst[i - 1] + 1:
      return False
  return True
    

# print("original len: ", len(links))
# print("set len: ", len(set(links)))
# print(set(links))

# print(len(check_dups(links)))
# print(check_dups(links)[4400:])

#print(check_consec(check_dups(links)))
#print(check_dups(links)[:10])
print(len(check_dups(links)))