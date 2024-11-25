import pandas as pd

file_path = '/Users/macbookpro/Downloads/cleaned_data.xlsx'
spotify_data = pd.read_excel(file_path, sheet_name='Cleaned Data')

# Chọn cột dữ liệu cần thiết để phù hợp với mục tiêu xu hướng âm nhạc
management_data = spotify_data[[
    'Track Name', 'Artist Name(s)', 'Album Name', 'Album Release Date','Artist Genres',
    'Danceability', 'Energy', 'Valence', 'Tempo', 'Popularity'
]]

# Đổi tên cột cho dễ hiểu cũng như dễ quản lý và trực quan hoá dữ liệu
management_data.rename(columns={
    'Track Name': 'Tên Bài Hát',
    'Artist Name(s)': 'Nghệ Sĩ',
    'Album Name': 'Tên Album',
    'Album Release Date': 'Ngày Phát Hành Album',
    'Artist Genres': 'Thể Loại',
    'Danceability': 'Độ Nhảy',
    'Energy': 'Năng Lượng',
    'Valence': 'Cảm Xúc',
    'Tempo': 'Tốc Độ',
    'Popularity': 'Độ Phổ Biến'
}, inplace=True)
management_data.to_csv('music_trends_data.csv', index=False, sep='|')
management_data.to_excel('music_trends.xlsx', index=False)
print(management_data)
# Hàm tạo dữ liệu mới với kiểm tra trùng lặp
def add_new_song(dataframe):
    print("\n--- Thêm bài hát mới ---")
    new_song = {
        'Tên Bài Hát': input("Nhập tên bài hát: ").strip(),
        'Nghệ Sĩ': input("Nhập tên nghệ sĩ: ").strip(),
        'Tên Album': input("Nhập tên album: ").strip(),
        'Ngày Phát Hành Album': input("Nhập ngày phát hành album (YYYY-MM-DD): ").strip(),
        'Thể Loại': input("Nhập thể loại (dùng dấu phẩy để phân cách nếu nhiều thể loại): ").strip(),
        'Độ Nhảy': float(input("Nhập độ nhảy (0.0 - 1.0): ")),
        'Năng Lượng': float(input("Nhập năng lượng (0.0 - 1.0): ")),
        'Cảm Xúc': float(input("Nhập cảm xúc (0.0 - 1.0): ")),
        'Tốc Độ': float(input("Nhập tốc độ (bpm): ")),
        'Độ Phổ Biến': int(input("Nhập độ phổ biến (0 - 100): "))
    }
    
    # Kiểm tra trùng lặp
    duplicate = dataframe[
        (dataframe['Tên Bài Hát'] == new_song['Tên Bài Hát']) &
        (dataframe['Nghệ Sĩ'] == new_song['Nghệ Sĩ'])
    ]
    
    if not duplicate.empty:
        print("\nBài hát đã tồn tại, không thể thêm vào.")
    else:
        dataframe = dataframe.append(new_song, ignore_index=True)
        print("\nThêm bài hát thành công!")
    
    return dataframe
def update_song(dataframe):
    print("\n--- Cập nhật bài hát ---")
    song_name = input("Nhập tên bài hát cần cập nhật: ")
    
    # Kiểm tra xem bài hát có tồn tại không
    if song_name in dataframe['Tên Bài Hát'].values:
        index = dataframe[dataframe['Tên Bài Hát'] == song_name].index[0]
        
        print("Chọn thuộc tính cần cập nhật:")
        print("1. Tên Bài Hát")
        print("2. Nghệ Sĩ")
        print("3. Tên Album")
        print("4. Ngày Phát Hành Album")
        print("5. Thể Loại")
        print("6. Độ Nhảy")
        print("7. Năng Lượng")
        print("8. Cảm Xúc")
        print("9. Tốc Độ")
        print("10. Độ Phổ Biến")
        
        choice = int(input("Nhập số thuộc tính cần cập nhật: "))
        column_names = list(dataframe.columns)
        selected_column = column_names[choice - 1]
        
        # Cập nhật giá trị mới
        new_value = input(f"Nhập giá trị mới cho '{selected_column}': ")
        if selected_column in ['Độ Nhảy', 'Năng Lượng', 'Cảm Xúc']:
            new_value = float(new_value)
        elif selected_column == 'Độ Phổ Biến':
            new_value = int(new_value)
        
        dataframe.at[index, selected_column] = new_value
        print("\nCập nhật thành công!")
    else:
        print("Bài hát không tồn tại.")
    return dataframe
management_data = add_new_song(management_data)
management_data = update_song(management_data)

# Lưu lại file sau khi chỉnh sửa
management_data.to_csv('updated_music_trends_data.csv', index=False, sep='|')
management_data.to_excel('updated_music_trends.xlsx', index=False)
print("Lưu file thành công!")