import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/aldakurniaputri/Tugas_Akhir/main/dashboard/day_data.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/aldakurniaputri/Tugas_Akhir/main/dashboard/hour_data.csv")

# Membagi data menjadi beberapa kelompok suhu yaitu suhu rendah, sedang, dan tinggi berdasarkan kuartil
def categorize_by_temperature(temp):
    if temp < day_df['temp'].quantile(0.25):
        return 'rendah'
    elif temp < day_df['temp'].quantile(0.75):
        return 'sedang'
    else:
        return 'tinggi'

# Menambahkan kolom kategori suhu
day_df['temp_category'] = day_df['temp'].apply(categorize_by_temperature)


# Set style
sns.set(style='darkgrid')

# Create Streamlit app
st.title(':sparkles: BIKE RENTALS DASHBOARD:sparkles:')

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://png.pngtree.com/png-clipart/20230807/original/pngtree-vector-illustration-of-a-bicycle-rental-logo-on-a-white-backdrop-vector-picture-image_10130391.png")
    
    st.write(
        """Dashboard ini sebagai informasi mengenai tren persewaan sepeda pada tahun 2011-2012
        dengan berdasarkan perubahan musim, perbandingan antara hari libur dengan hari kerja, serta
        menunjukkan pola persewaan sepeda rentang waktu bulanan."""
    )

tab1, tab2, tab3, tab4 = st.tabs(["Tab 1", "Tab 2", "Tab 3", "Tab 4"])
 
with tab1:
    from matplotlib.dates import DateFormatter
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    day_df.set_index('dteday', inplace=True)  # Set 'dteday' as index
    
    # Agregasi data bulanan
    monthly_rentals = day_df.resample('M')['cnt'].sum()
    
    st.header('Pola Persewaan Sepeda Bulanan:sparkles:')
    
    # Plot pola persewaan sepeda bulanan
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_rentals.index, monthly_rentals.values, marker='o', linestyle='-')
    ax.set_title('Pola Persewaan Sepeda Bulanan')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    ax.grid(True)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    plt.tight_layout()

    # Display plot
    st.pyplot(fig)

    with st.expander("Baca Penjelasan Grafik"):
        st.write(
            """Terlihat jumlah penyewaan sepeda pada kurun waktu 2011-2012
            cenderung meningkat ketika memasuki bulan April dan kemudian menurun memasuki bulan Oktober.
            Dengan melihat pola kenaikan jumlah penyewaan sepeda pada bulan-bulan tertentu tersebut,
            kita dapat memastikan ketersediaan yang cukup selama periode lonjakan untuk meningkatkan layanan
            terkait permintaan penyewaan sepeda."""
    )
 
with tab2:
    st.header('Persebaran Jumlah Penyewaan Sepeda pada Hari Libur dan Hari Kerja:sparkles:')

    # Plot persebaran jumlah penyewaan sepeda
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=day_df, x='holiday', y='cnt', ax=ax)
    ax.set_title('Pengaruh Hari Libur terhadap Jumlah Penyewaan Sepeda')
    ax.set_xlabel('Hari Libur (0: Bukan Hari Libur, 1: Hari Libur)')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Bukan Hari Libur', 'Hari Libur'])
    ax.grid(True)
    plt.tight_layout()

    # Display plot
    st.pyplot(fig)

    with st.expander("Baca Penjelasan Grafik"):
        st.write(
            """Terlihat kotak (box) pada kategori "Hari Libur" lebih tinggi daripada kotak pada kategori "Bukan Hari Libur",
            menunjukkan bahwa rata-rata jumlah penyewaan sepeda lebih tinggi pada hari libur daripada pada hari kerja.
            Persebaran pada kategori "Hari Libur" lebih besar daripada pada kategori "Bukan Hari Libur",
            menunjukkan variasi yang lebih besar dalam jumlah penyewaan sepeda pada hari libur."""
    )

with tab3:
    st.header('Jumlah Penyewaan Sepeda berdasarkan Musim:sparkles:')

    # Plot rata-rata jumlah penyewaan sepeda berdasarkan musim
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=day_df, x='season', y='cnt', ci=None, ax=ax)
    ax.set_title('Rata-rata Jumlah Penyewaan Sepeda Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan Sepeda')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])

    # Display plot
    st.pyplot(fig)

    with st.expander("Baca Penjelasan Grafik"):
        st.write(
            """Berdasarkan visualisasi grafik pola persewaan sepeda pada setiap musim di atas, 
            terlihat bahwa musim panas (summer) dan musim gugur (fall) cenderung memiliki jumlah penyewaan sepeda 
            yang lebih tinggi daripada musim semi (spring) dan musim dingin (winter).
            Hal ini mungkin disebabkan oleh kondisi cuaca yang lebih menyenangkan bagi aktivitas luar ruangan
            selama musim panas dan kebutuhan transportasi alternatif selama musim dingin."""
    )
        
with tab4:
    st.header('Preferensi penyewa sepeda terhadap tingkatan suhu:sparkles:')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='temp_category', y='cnt', data=day_df, palette='pastel', ax=ax)
    ax.set_title('Distribusi Jumlah Penyewaan Sepeda Berdasarkan Kategori Suhu')
    ax.set_xlabel('Kategori Suhu')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    
    st.pyplot(fig)
    
    with st.expander("Baca Penjelasan Grafik"):
        st.write(
            """Berdasarkan visualisasi suhu yang dikelompokkan menjadi suhu rendah, sedang, dan tinggi
            terlihat pengguna cenderung menggunakan sepeda lebih sering saat suhu tinggi dibandingkan dengan suhu sedang atau rendah. 
            Hal ini selaras dengan analisis kita sebelumnya mengenai musim panas dan musim gugur (bersuhu tinggi) yang memiliki
            jumlah penyewaan sepeda lebih banyak dibanding ketika musim semi dan musim dingin."""
    )
