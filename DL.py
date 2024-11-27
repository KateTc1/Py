import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime
import random

# Đọc dữ liệu từ file CSV
file_path = 'top_10000_1950-now.csv'
df = pd.read_csv(file_path)

# Xóa cột "Album Genres"
columns_to_drop = ['Album Genres', 'Key']
df = df.drop(columns=columns_to_drop, errors='ignore')

# Điền giá trị NaN và 0 trong các cột số bằng giá trị trung bình
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
for col in numeric_columns:
    mean_value = df[col][df[col] != 0].mean()  # Tính trung bình, bỏ qua giá trị bằng 0
    df[col] = df[col].apply(lambda x: mean_value if pd.isna(x) or x == 0 else x)

# Xóa các dòng có dữ liệu chữ bị thiếu
string_columns = df.select_dtypes(include=['object']).columns
df = df.dropna(subset=string_columns)

# Hàm xử lý ngày tháng cho cột "Album Release Date"
def generate_full_date(date_str):
    try:
        if pd.isna(date_str):
            return date_str

        date_str = str(date_str).strip()
        if len(date_str) == 4 and date_str.isdigit():
            year = int(date_str)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # Đảm bảo ngày hợp lệ
            return datetime(year, month, day).strftime('%Y-%m-%d')
        return date_str
    except Exception:
        return date_str

# Xử lý "Album Release Date"
if 'Album Release Date' in df.columns:
    df['Album Release Date'] = df['Album Release Date'].apply(generate_full_date)

df['Album Release Date'] = pd.to_datetime(df['Album Release Date'], errors='coerce')
df['Year'] = df['Album Release Date'].dt.year
df['Album Release Date'] = df['Album Release Date'].dt.strftime('%Y-%m-%d')

# Loại bỏ các dòng trùng lặp
df = df.drop_duplicates()

# Tạo workbook và worksheet
wb = Workbook()
ws = wb.active
ws.title = "Cleaned Data"

# Thêm dữ liệu từ DataFrame vào worksheet
for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
    for c_idx, value in enumerate(row, 1):
        cell = ws.cell(row=r_idx, column=c_idx, value=value)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        if r_idx == 1:
            cell.font = Font(bold=True)

# Lưu file Excel
output_path = 'cleaneddata.xlsx'
wb.save(output_path)

print("Dữ liệu đã được lưu vào file Excel với định dạng:", output_path)
