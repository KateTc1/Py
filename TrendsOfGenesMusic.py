import pandas as pd
import matplotlib.pyplot as plt
import numpy as numpy
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
df = pd.read_excel("C:\\Users\\ASUS\\Desktop\\python\\Spotify\\cleaned_data (1).xlsx")

def duong():
    # Group data by year and calculate the average Acousticness for each year
    acousticness_trend = df.groupby('Year')['Acousticness'].mean().dropna()
    valence_trend = df.groupby('Year')['Valence'].mean().dropna()
    energy_trend = df.groupby('Year')['Energy'].mean().dropna()
    danceability_trend = df.groupby('Year')['Danceability'].mean().dropna()
    liveness_trend = df.groupby('Year')['Liveness'].mean().dropna()
    speechiness_trend = df.groupby('Year')['Speechiness'].mean().dropna()

    # Plot the trend of Acousticness over the years
    plt.figure(figsize=(12, 8))
    plt.plot(acousticness_trend.index, acousticness_trend.values, label = 'acoustic')
    plt.plot(valence_trend.index, valence_trend.values, label = 'valence')
    plt.plot(energy_trend.index, energy_trend.values, label = 'energy')
    plt.plot(danceability_trend.index, danceability_trend.values, label = 'danceability')
    plt.plot(liveness_trend.index, liveness_trend.values, label = 'Liveness')
    plt.plot(speechiness_trend.index, speechiness_trend.values, label = 'speechiness')
    
    plt.title('Xu hướng đặc điểm của âm thanh', fontsize=16)
    plt.xlabel('Năm', fontsize=12)
    plt.ylabel('Trung bình', fontsize=12)
    plt.axis('tight')
    plt.legend(loc = 'upper right')
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

def TopTrack():
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
    plt.xticks(ticks=yearly_max_popularity.index.astype(int), labels=yearly_max_popularity.index.astype(int), rotation=90, ha='right')
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
def heat_map():
    # Extract numerical columns related to audio features
    numerical_columns = [
        'Danceability', 'Energy', 'Speechiness', 'Acousticness','Loudness','Mode','Time Signature','Track Duration (ms)',
        'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Year','Popularity'
    ]
    numerical_data = df[numerical_columns]

    # Calculate the correlation matrix
    correlation_matrix = numerical_data.corr()

    # Set up the figure size
    plt.figure(figsize=(10, 8))

    # Create a heatmap for the correlation matrix
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True)

    # Add title and adjust layout
    plt.title("Bản đồ nhiệt của sự tương quan của các dữ liệu", fontsize=16)
    plt.tight_layout()

    # Display the heatmap
    plt.show()
def test():
    
    plot_data = df[['Tempo', 'Danceability', 'Popularity']]

    # Create scatter plot with color based on 'Popularity'
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        plot_data['Tempo'], 
        plot_data['Danceability'], 
        c=plot_data['Popularity'], 
        cmap='viridis', 
        s=240,  # Point size
        alpha=0.7  # Transparency
    )

    # Add color bar for popularity
    plt.colorbar(scatter, label='Popularity')

    # Add labels and title
    plt.xlabel('Tempo')
    plt.ylabel('Danceability')
    plt.title('Correlation Between Tempo and Danceability with Popularity Color-Coding')

    # Display plot
    plt.tight_layout()
    plt.show()
def do_phan_bo_cua_do_pho_bien():
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Popularity'], bins=20, kde=True, color='skyblue')

    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Phân Bố Độ Phổ Biến của Các Bài Hát', fontsize=16)
    plt.xlabel('Độ Phổ Biến', fontsize=14)
    plt.ylabel('Tần Suất', fontsize=14)

    # Hiển thị biểu đồ
    plt.tight_layout()
    plt.show()
def Over_view():
    plt.figure(figsize=(10, 6))
    
    plt.subplot(3, 4, 1)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Acousticness'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Acouticness', fontsize=16)
    
    plt.subplot(3, 4, 2)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Valence'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Valence', fontsize=16)
    
    plt.subplot(3, 4, 3)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Liveness'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Liveness', fontsize=16)
    
    plt.subplot(3, 4, 4)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Speechiness'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Speechiness', fontsize=16)
    
    plt.subplot(3, 4, 5)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Energy'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Energy', fontsize=16)
    
    plt.subplot(3, 4, 6)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Tempo'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Tempo', fontsize=16)
    
    plt.subplot(3, 4, 7)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Loudness'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Loudness', fontsize=16)
    
    plt.subplot(3, 4, 8)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Danceability'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Danceability', fontsize=16)
    
    plt.subplot(3, 4, 9)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Track Duration (ms)'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Track Duration (ms)', fontsize=16)
    
    plt.subplot(3, 4, 10)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Instrumentalness'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Instrumentalness', fontsize=16)
    
    plt.subplot(3, 4, 11)  # (số dòng, số cột, vị trí)
    sns.histplot(df['Explicit'], bins=20, kde=True, color='skyblue')
    # Cài đặt tiêu đề và nhãn cho biểu đồ
    plt.title('Explicit', fontsize=16)
    
    # Hiển thị biểu đồ
    plt.tight_layout()
    plt.show()
    
heat_map()



