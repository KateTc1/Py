import pandas as pd
import matplotlib.pyplot as plt
import numpy as numpy
from matplotlib.colors import LinearSegmentedColormap
df = pd.read_excel("C:\\Users\\ASUS\\Desktop\\python\\Spotify\\cleaned_data (1).xlsx")

def duong():
    # Group data by year and calculate the average Acousticness for each year
    acousticness_trend = df.groupby('Year')['Acousticness'].mean().dropna()
    valence_trend = df.groupby('Year')['Valence'].mean().dropna()
    energy_trend = df.groupby('Year')['Energy'].mean().dropna()
    danceability_trend = df.groupby('Year')['Danceability'].mean().dropna()


    # Plot the trend of Acousticness over the years
    plt.figure(figsize=(12, 8))
    plt.plot(acousticness_trend.index, acousticness_trend.values, marker='o', label = 'acoustic')
    plt.plot(valence_trend.index, valence_trend.values, marker = 'o', label = 'valence')
    plt.plot(energy_trend.index, energy_trend.values, marker = 'o', label = 'energy')
    plt.plot(danceability_trend.index, danceability_trend.values, marker = 'o', label = 'danceability')
    plt.title('Xu hướng đặc điểm của âm thanh', fontsize=16)
    plt.xlabel('Năm', fontsize=12)
    plt.ylabel('Trung bình', fontsize=12)
    plt.axis('tight')
    plt.legend(loc = 'best')
    plt.grid(True)
    plt.show()
def mien(df):

    # Sắp xếp theo năm
    df = df.sort_values("Year")

    # Chuyển đổi True/False thành 1/0
    df['Explicit'] = df['Explicit'].map({True: 1, False: 0})

    # Tính tỷ lệ Explicit và UnExplicit theo từng năm
    grouped = df.groupby('Year').agg(
        explicit=('Explicit', 'mean'),  # Tỷ lệ True (explicit)
        count=('Explicit', 'size')     # Số lượng tổng trong từng năm
    ).reset_index()

    # Nhân tỷ lệ explicit và unexplicit với 100 để chuyển sang phần trăm
    grouped['explicit'] = grouped['explicit'] * 100
    grouped['unexplicit'] = (1 - grouped['explicit'] / 100) * 100

    # Vẽ biểu đồ miền
    plt.figure(figsize=(12, 8))

    # Vẽ biểu đồ miền cho tỷ lệ explicit và unexplicit
    plt.fill_between(grouped['Year'], 0, grouped['explicit'], label='Explicit', alpha=0.6)
    plt.fill_between(grouped['Year'], grouped['explicit'], 100, label='UnExplicit', alpha=0.6)

    # Thêm các nhãn và tiêu đề
    plt.title('Biểu đồ miền thể hiện tỷ lệ Explicit (True) qua các năm')
    plt.xlabel('Năm')
    plt.ylabel('Tỷ lệ (%)')  # Thay đổi đơn vị trục y thành phần trăm
    plt.axis('tight')
    plt.legend(title="Nhóm", bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout() 
    # Hiển thị biểu đồ
    plt.show()
def phantan():

    # Selecting 'Valence' and 'Danceability' for the scatter plot
    x_valence = df['Valence']
    y_danceability = df['Danceability']

    # Creating scatter plot to show the relationship between Valence and Danceability
    plt.figure(figsize=(10, 6))
    plt.scatter(x_valence, y_danceability, alpha=0.6, color='green')
    plt.title('Scatter Plot of Valence vs Danceability')
    plt.xlabel('Valence (Positivity)')
    plt.ylabel('Danceability')
    plt.grid(alpha=0.3)
    plt.show()

import matplotlib.pyplot as plt
import pandas as pd

def TopTrack(df):
    # Nhóm dữ liệu theo 'Track Name' và tính trung bình cộng của 'Popularity'
    df_grouped = df.groupby('Track Name', as_index=False)['Popularity'].sum()
    
    # Sắp xếp dữ liệu theo 'Popularity' giảm dần
    df_sorted = df_grouped.sort_values("Popularity", ascending=False)
    
    # Lấy 10 track phổ biến nhất và độ phổ biến tương ứng
    top10Track = df_sorted['Track Name'].head(10)
    top10Popularity = df_sorted['Popularity'].head(10)
    
    # Tạo một danh sách màu sắc (mỗi cột một màu)
    colors = plt.cm.tab10(range(len(top10Track)))  # Tối đa 10 màu từ colormap
    
    # Vẽ biểu đồ
    plt.figure(figsize=(12, 7))
    plt.bar(top10Track, top10Popularity, color=colors)
    plt.title('Top 10 Track Phổ Biến Nhất (Tính Trung Bình)')
    plt.xlabel('Tên Track')
    plt.ylabel('Độ Phổ Biến (Trung Bình)')
    plt.xticks(rotation=45, ha='right')  # Xoay nhãn trục x
    plt.tight_layout()  # Đảm bảo bố cục không bị chồng chéo
    plt.show()
def Max_Popularity_Track_Over_Year():
    # Nhóm theo 'Key' và tính trung bình cộng của 'Popularity'
    yearly_max_popularity = df.groupby('Year')['Popularity'].max().dropna()


    # Vẽ biểu đồ
    plt.figure(figsize=(12, 8))
    plt.bar(yearly_max_popularity.index, yearly_max_popularity.values, color='skyblue')  # Trục x là tên key, trục y là Popularity
    plt.title('Độ Phổ Biến của bài hát phổ biến nhất từng năm')
    plt.xlabel('Năm(s)')
    plt.ylabel('Độ Phổ Biến (Trung Bình)')
    plt.xticks(ticks=yearly_max_popularity.index.astype(int), labels=yearly_max_popularity.index, rotation=90, ha='right')
    plt.tight_layout()  # Đảm bảo bố cục gọn gàng
    plt.show()

def Top_10_Artist(df):
    # Count the number of tracks per artist
    artist_counts = df.groupby('Artist Name(s)').size().reset_index(name='Track Count')
    artist_counts = artist_counts.sort_values('Track Count', ascending=False)
    top_artists = artist_counts.head(10)
    colors = [
    "#D5BAFF",  # Light Lavender
    "#E2BAFF",  # Pastel Purple
    "#FFCCE5",  # Pastel Magenta
    "#FFC4C4",   # Soft Red
    "#FFB3BA",  # Pastel Pink
    "#FFDFBA",  # Pastel Peach
    "#FFFFBA",  # Pastel Yellow
    "#B9FBC6",  # Pastel Green
    "#BAFFFF",  # Light Cyan
    "#BAE1FF"  # Pastel Blue
    ]
    # Plot the bar chart with similar pastel colors
    plt.figure(figsize=(12, 8))
    plt.barh(
        top_artists['Artist Name(s)'], 
        top_artists['Track Count'], 
        color=colors # Apply similar pastel colors
    )
    
    plt.xlabel('Số lượng track', fontsize=14)
    plt.ylabel('Nghệ sĩ', fontsize=14)
    plt.title('Top 10 nghệ sĩ có nhiều bài hát trong top', fontsize=16)
    plt.gca().invert_yaxis()  # Reverse Y-axis so the top artist is on top
    plt.tight_layout()
    plt.show()

Max_Popularity_Track_Over_Year()


