import csv
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['best'] 
collection = db['test']  

with open('37176ff3-dd70-4f1f-8e1d-83eda3cf77e4.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        collection.insert_one(row)

print("เสร็จสิ้นการนำเข้าข้อมูลลงใน MongoDB")
## เพิ่มข้อมูลไฟล์ CSV ลงใน mongodb
