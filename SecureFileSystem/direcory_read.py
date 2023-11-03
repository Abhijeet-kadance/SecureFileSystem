import os
import pandas as pd
import MySQLdb
import json
import xlwt
from xlwt import Workbook


path = '{0}\media\core\\articles'.format(os.getcwd())
print("woking directory path ",path)
dir_list = os.listdir(path)
print("directory list ",dir_list)
wb = Workbook()

sheet1 = wb.add_sheet('Sheet 1')
sheet1.write(0, 0, "title")
row_count=1
for dir in dir_list:
    sheet1.write(row_count, 0, dir)
    row_count += 1
wb.save('test.xls')

df = pd.read_excel('test.xls')
dict = df.to_dict()
dict_keys = list(dict["title"].keys())
print("dictionary ",dict["title"])
print("dictionary keys ",dict_keys)
db = MySQLdb.connect(
     host="localhost",
     user="root",
     passwd="tanvi",
     database="link_creation_db",
     auth_plugin='mysql_native_password' ### added to resolve Authentication plugin 'caching_sha2_password' is not supported error
)

cursor = db.cursor()
truncate_query = "TRUNCATE TABLE link_creation_linkcreation"
cursor.execute(truncate_query)
for key in dict_keys:
    sql = "INSERT INTO link_creation_linkcreation(id, title, download_link) VALUES (%s,%s, %s)"
    id = key+1
    cursor.execute(sql, (id, dict["title"][key], 'core/articles/{0}'.format(dict["title"][key])))
db.commit()
