import csv
from pymongo import MongoClient

# เปิดการเชื่อมต่อ MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']  # เลือกฐานข้อมูล
collection = db['mycollection']  # เลือกคอลเล็กชัน

# อ่านไฟล์ CSV และเพิ่มข้อมูลลงใน MongoDB
with open('37176ff3-dd70-4f1f-8e1d-83eda3cf77e4.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # เพิ่มข้อมูลลงใน MongoDB
        collection.insert_one(row)

print("เสร็จสิ้นการนำเข้าข้อมูลลงใน MongoDB")
