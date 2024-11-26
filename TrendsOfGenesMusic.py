import pandas as pd
import matplotlib.pyplot as plt
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



phantan()
