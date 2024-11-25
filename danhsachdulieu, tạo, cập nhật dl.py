import pandas as pd

file_path = '/Users/macbookpro/Downloads/cleaned_data.xlsx'
spotify_data = pd.read_excel(file_path, sheet_name='Cleaned Data')

# Chọn cột dữ liệu cần thiết để phù hợp với mục tiêu xu hướng âm nhạc
management_data = spotify_data[[
    'Track Name', 'Artist Name(s)', 'Album Name', 'Album Release Date','Artist Genres',
    'Danceability', 'Energy', 'Valence', 'Tempo', 'Popularity'
]]

# Đổi tên cột cho dễ hiểu cũng như dễ quản lý và phù hợp với ng dùng việt
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

# Hàm nhập kiểm tra khi sai điều kiện vd như độ nhảy, tốc độ, năng lượng,... và yêu cầu nhập lại khi sai
def get_input(prompt, data_type, condition=None, error_message="Dữ liệu không hợp lệ, vui lòng nhập lại!"):
    while True:
        try:
            value = data_type(input(prompt).strip())
            if condition and not condition(value):
                print(error_message)
                continue
            return value
        except ValueError:
            print(error_message)

# Hàm thêm bài hát mới 
def add_new_song(dataframe):
    print("\n--- Thêm bài hát mới ---")
    confirm = input("Bạn có muốn thêm bài hát mới? (có/không): ").strip().lower()
    
    if confirm in ['có', 'co', 'yes', 'y']:
        new_song = {
            'Tên Bài Hát': get_input("Nhập tên bài hát: ", str),
            'Nghệ Sĩ': get_input("Nhập tên nghệ sĩ: ", str),
            'Tên Album': get_input("Nhập tên album: ", str),
            'Ngày Phát Hành Album': get_input("Nhập ngày phát hành album (YYYY-MM-DD): ", str),
            'Thể Loại': get_input("Nhập thể loại (dùng dấu phẩy để phân cách nếu nhiều thể loại): ", str),
            'Độ Nhảy': get_input("Nhập độ nhảy (0.0 - 1.0): ", float, lambda x: 0.0 <= x <= 1.0, "Độ nhảy phải từ 0.0 đến 1.0."),
            'Năng Lượng': get_input("Nhập năng lượng (0.0 - 1.0): ", float, lambda x: 0.0 <= x <= 1.0, "Năng lượng phải từ 0.0 đến 1.0."),
            'Cảm Xúc': get_input("Nhập cảm xúc (0.0 - 1.0): ", float, lambda x: 0.0 <= x <= 1.0, "Cảm xúc phải từ 0.0 đến 1.0."),
            'Tốc Độ': get_input("Nhập tốc độ (bpm): ", float, lambda x: x > 0, "Tốc độ phải lớn hơn 0."),
            'Độ Phổ Biến': get_input("Nhập độ phổ biến (0 - 100): ", int, lambda x: 0 <= x <= 100, "Độ phổ biến phải từ 0 đến 100.")
        }
        
        # Xem có trùng lặp không
        duplicate = dataframe[
    (dataframe['Tên Bài Hát'] == new_song['Tên Bài Hát']) &
    (dataframe['Nghệ Sĩ'] == new_song['Nghệ Sĩ']) &
    (dataframe['Tên Album'] == new_song['Tên Album'])
    ]

        
        if not duplicate.empty:
            print("\nBài hát đã tồn tại, không thể thêm vào.")
        else:
            # Nếu chưa tồn tại thì thêm vào
            new_df = pd.DataFrame([new_song])
            dataframe = pd.concat([dataframe, new_df], ignore_index=True)
            print("\nThêm bài hát thành công!")
    else:
        print("\nKhông thêm bài hát mới.")
    
    return dataframe

# Hàm cập nhật dữ liệu 
def update_song(dataframe):
    print("\n--- Cập nhật bài hát ---")
    confirm = input("Bạn có muốn cập nhật bài hát? (có/không): ").strip().lower()

    if confirm in ['có', 'co', 'yes', 'y']:
        song_name = get_input("Nhập tên bài hát cần cập nhật: ", str)
        
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
            
            choice = get_input("Nhập số thuộc tính cần cập nhật (1-10): ", int, lambda x: 1 <= x <= 10, "Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 10.")
            column_names = list(dataframe.columns)
            selected_column = column_names[choice - 1]
            
            # Nhập phần cần cập nhật
            if selected_column == 'Độ Nhảy':
                new_value = get_input(f"Nhập giá trị mới cho '{selected_column}' (0.0 - 1.0): ", float, lambda x: 0.0 <= x <= 1.0, f"Giá trị cho '{selected_column}' phải từ 0.0 đến 1.0.")
            elif selected_column == 'Năng Lượng':
                new_value = get_input(f"Nhập giá trị mới cho '{selected_column}' (0.0 - 1.0): ", float, lambda x: 0.0 <= x <= 1.0, f"Giá trị cho '{selected_column}' phải từ 0.0 đến 1.0.")
            elif selected_column == 'Cảm Xúc':
                new_value = get_input(f"Nhập giá trị mới cho '{selected_column}' (0.0 - 1.0): ", float, lambda x: 0.0 <= x <= 1.0, f"Giá trị cho '{selected_column}' phải từ 0.0 đến 1.0.")
            elif selected_column == 'Tốc Độ':
                new_value = get_input(f"Nhập giá trị mới cho '{selected_column}' (> 0): ", float, lambda x: x > 0, f"Giá trị cho '{selected_column}' phải lớn hơn 0.")
            elif selected_column == 'Độ Phổ Biến':
                new_value = get_input(f"Nhập giá trị mới cho '{selected_column}' (0 - 100): ", int, lambda x: 0 <= x <= 100, f"Giá trị cho '{selected_column}' phải từ 0 đến 100.")
            else:
                new_value = get_input(f"Nhập giá trị mới cho '{selected_column}': ", str)
            
            # Cập nhật giá trị 
            dataframe.at[index, selected_column] = new_value
            print("\nCập nhật thành công!")
        else:
            print("Bài hát không tồn tại.")
    else:
        print("\nKhông cập nhật bài hát nào.")
    
    return dataframe

management_data = add_new_song(management_data)
management_data = update_song(management_data)

# Lưu lại file sau khi thêm hoặc cập nhật
management_data.to_csv('updated_music_trends_data.csv', index=False, sep='|')
management_data.to_excel('updated_music_trends.xlsx', index=False)
print("Lưu file thành công!")
