import xlwings as xw
import os
import pandas as pd
from icecream import ic
import pickle
import itertools
import time
import datetime
import xlsxwriter

zip_dump = []

cwd = str(os.getcwd())
# date = ["8/21/2019", "8/22/2019"]
# description = ["Store 1", "Store 2"]
# cat = ["Food", "Refund"]
# amount = ["-$20.12", "$403.11"]

# date2 = ["9/21/2019", "9/22/2019"]
# description2 = ["Store 69", "Noice 2"]
# cat2 = ["Woops"]
# amount2 = ["$20.12", "-$403.11"]

# temp1 = itertools.zip_longest(date, description, cat, amount)
# temp2 = itertools.zip_longest(date2, description2, cat2, amount2)

labels = ["Index", "Date", "Description", "Category", "Amount"]

# zip_dump.append(temp1)
# zip_dump.append(temp2)

# for i in temp2:
#     print(i)

file_path = str(os.getcwd()) + r"\x\dump"
with open(file_path, "rb") as f:
    data = pickle.load(f)


def clean_data(data=None):
    clean_data = []
    try:
        for row in data:
            clean_data.append(row[3])
    # ic(clean_data)
    # print(clean_data)
        return clean_data
    except:
        print("rip")
        return None

data = clean_data(data)

# print(temp1)
# ic(temp1)
# ic(temp2)
# ic(zip_dump)
# ic(data)

# df = pd.DataFrame(temp1)
# sht.range('A1').value = df

# print(len(data[0]))

# for i in data[1]:
#     print(i)



# start = time.time()
# # start = time.perf_counter_ns()
# pretty_start = time.strftime("%H:%M:%S", time.gmtime(start))


wb1 = xw.Book(str(os.getcwd()) + r"\x\template.xlsx")
sht1 = wb1.sheets["Sheet1"]

wb2 = xw.Book(str(os.getcwd()) + r"\x\transaction.csv")
sht2 = wb2.sheets[0]

col_range = sht2.range('A1').expand()
# last_row_int = int(str(col_range).split('$')[4].split('>')[0])

amount_col = sht2[:,4:9]
new_amount_col = sht2[:,5:10]
# table = sht2.range(col_range).value
table = sht2.range(amount_col).value
sht2.range(amount_col).value = None
sht2.range(new_amount_col).value = table

# sht1.range('a1').value = table
# sht1.range( sht1[1:,3] ).options(transpose=True).value = data
# print(data[0])
sht2.range(sht2[1:,4]).options(transpose=True).value = data
sht2.range('E1').value = 'Signed Amount'
# print(sht1.range('A1').value)

print(len(data))
# #TODO xlwings version
# for page in range(0, len(data)):
#     df = pd.DataFrame(data[page])
#     df.columns = df.iloc[0]
#     df = df.reindex(df.index.drop(0)).reset_index(drop=True)
#     df.columns.name = None
#     df.index.name = None
#     row = page * 100 + 2
#     sht1.range(f"A{row}").value = df
# sht1.range("A1").value = labels

# #TODO lsxwriter version
# # writer = pd.ExcelWriter(cwd +"\\x\\Data.xlsx", engine='xlsxwriter')
# # for page in range(0,len(data)):
# #     df = pd.DataFrame(data[page])
# #     df.columns = df.iloc[0]
# #     df = df.reindex(df.index.drop(0)).reset_index(drop=True)
# #     df.columns.name = None
# #     df.index.name = None
# #     row = page * 100 + 1
# #     df.to_excel(writer, sheet_name='Sheet1',startrow=row,index=False)
# # writer.save()
# # writer.close()

# p_elapse = time.time()
# # p_elapse = time.perf_counter_ns()
# elapse = p_elapse - start
# pretty_p_elapse = time.strftime("%H:%M:%S", time.gmtime(p_elapse))
# pretty_elapse = time.strftime("%H:%M:%S", time.gmtime(elapse))
# print(start, p_elapse, elapse)
# print(pretty_start, pretty_p_elapse, pretty_elapse)
# # print(elapse)
# # wb1.save()
# # wb1.close()



