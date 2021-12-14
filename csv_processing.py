import csv
import glob

import pandas as pd
import argparse
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--csv', type=str, default = None)
parser.add_argument('--numpydir', type=str, default=None)
args = parser.parse_args()

csv_f = args.csv #open("/data2/queenie/IEEE2015Ace/dataset/Dev/Speech/Lin8Ch/20211031T125843_test_gen_corpus_dataset_results.csv",'r')
csv_data = pd.read_csv(csv_f)
numpy_dir = args.numpydir#"/data2/queenie/IEEE2015Ace/solution/DatasetProcessing/Lin8Ch"
#csv_save_path = "/data2/queenie/IEEE2015Ace/solution/DatasetProcessing/" +"Mobile.csv"
csv_save_path = "/data2/queenie/IEEE2015Ace/solution/DatasetProcessing/" + numpy_dir.split("/")[-1]+".csv"
for i in csv_data:
    print(i)

room_name = ['Building_Lobby','Lecture_Room_1','Lecture_Room_2','Meeting_Room_1','Meeting_Room_2','Office_1','Office_2']

def file_name_parse(name):
    for i in room_name:
        if i in name:
            room = i
            break
    cfg = ((name.split(room))[1].split('_'))[1]
    room = ' ' + room
    config = int(cfg)
    chan = int(((name.split('_'))[len((name.split('_')))-1]).split('.')[0]) + 1
    return room, config, chan

DDR_column = []
DDR_M_column = []
T60_column = []
T60_M_column = []
for i in range(30):
    DDR_str = 'DDR_B' + str(i+1)
    DDR_column.append(DDR_str)
    DDR_M_str = 'DDR_B' + str(i+1)
    DDR_M_column.append(DDR_M_str)
    T60_str = 'DDR_B' + str(i+1)
    T60_column.append(T60_str)
    T60_M_str = 'DDR_B' + str(i+1)
    T60_M_column.append(T60_M_str)
print(DDR_column)
print(DDR_M_column)
print(T60_column)
print(T60_M_column)

#for p in glob.glob(r'C:\Users\Admin\PycharmProjects\audio'+r'\*.npy'):
for p in glob.glob(numpy_dir+r'/*.npy'):
    ss = p.split('/')
    print(ss[len(ss)-1])
    room, config, chan = file_name_parse(ss[len(ss)-1])
    print(room, config, chan)
    data = csv_data[(csv_data[' Room:'] == room) & (csv_data[' Room Config:'] == config) & (csv_data[' Channel:'] == chan)]

    DDR_data = data.loc[:, [' DRR:']]
    DDR_data_csv = pd.DataFrame(DDR_data.values.T, index=DDR_data.columns, columns=DDR_data.index)
    DDR_data_csv.index = [p]
    DDR_data_csv.columns = DDR_column
    #print(DDR_data_csv)

    DDR_M = data.loc[:, [' DRR Mean (Ch):']]
    DDR_M_csv = pd.DataFrame(DDR_M.values.T, index=DDR_M.columns, columns=DDR_M.index)
    DDR_M_csv.index = [p]
    DDR_M_csv.columns = DDR_M_column
    #print(DDR_M_csv)

    T60_data = data.loc[:, [' T60:']]
    T60_data_csv = pd.DataFrame(T60_data.values.T, index=T60_data.columns, columns=T60_data.index)
    T60_data_csv.index = [p]
    T60_data_csv.columns = T60_column
    #print(T60_data_csv)

    T60_M_data = data.loc[:, [' T60 Mean (Ch):']]
    T60_M_data_csv = pd.DataFrame(T60_M_data.values.T, index=T60_M_data.columns, columns=T60_M_data.index)
    T60_M_data_csv.index = [p]
    T60_M_data_csv.columns = T60_M_column
    #print(T60_M_data_csv)

    FB_DDR_data = (data.loc[:, [' FB DRR :']]).iloc[0 ,0]
    #print(FB_DDR_data)

    FB_DDR_M_data = (data.loc[:, [' FB DRR Mean (Ch):']]).iloc[0 ,0]
    #print(FB_DDR_M_data)

    FB_T60_data = (data.loc[:, [' FB T60:']]).iloc[0 ,0]
    #print(FB_T60_data)

    FB_T60_M_data = (data.loc[:, [' FB T60 Mean (Ch):']]).iloc[0 ,0]
    #print(FB_T60_M_data)

    data_to_csv = pd.concat([DDR_data_csv, DDR_M_csv, T60_data_csv, T60_M_data_csv], axis = 1)
    data_to_csv['FB DDR'] = FB_DDR_data
    data_to_csv['FB DDR M'] = FB_DDR_M_data
    data_to_csv['FB T60'] = FB_T60_data
    data_to_csv['FB T60 M'] = FB_T60_M_data
    print(data_to_csv)

    #data_to_csv.to_csv('test.csv', mode='a', index=True,header=True)
    data_to_csv.to_csv(csv_save_path, mode='a', index=True,header=False)
    data_to_csv.drop(data_to_csv.index, inplace=True)

