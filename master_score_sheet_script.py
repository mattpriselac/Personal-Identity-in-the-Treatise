#master score sheet generating script
import csv
import os
from treatise_reference_data import master_score_sheet
#get to the project root dir and operate from there
os.chdir('..')

score_file = open('data_out/blank_master_score_sheet.csv', 'w')
dict_writer = csv.writer(score_file)

header = ['paragraph', 'score']
dict_writer.writerow(header)
for key in master_score_sheet.keys():
    outline = []
    outline.append(key)
    outline.append(master_score_sheet[key])
    dict_writer.writerow(outline)

score_file.close()
print('done writing score sheet to data_out/blank_master_score_sheet.csv')
