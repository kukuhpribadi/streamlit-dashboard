import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

def filtered_df(df):
    # Resample dan agregasi data
    data_df = df.resample("MS", on="dteday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": ["max", "min", "mean", "sum"]
    }).reset_index()  # Reset index untuk mengembalikan 'dteday' sebagai kolom
    return data_df

# Membaca data
bike_sharing_df = pd.read_csv("day.csv")

# Mengubah kolom 'dteday' menjadi tipe datetime
datetime_columns = ["dteday"]
bike_sharing_df.sort_values(by="dteday", inplace=True)
bike_sharing_df.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    bike_sharing_df[column] = pd.to_datetime(bike_sharing_df[column])

# Mendapatkan rentang tanggal minimum dan maksimum
min_date = bike_sharing_df["dteday"].min()
max_date = bike_sharing_df["dteday"].max()

# Sidebar untuk memilih rentang tanggal
with st.sidebar:
    st.image('bike.png')

    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter DataFrame berdasarkan rentang tanggal
main_df = bike_sharing_df[
    (bike_sharing_df["dteday"] >= pd.to_datetime(start_date)) &
    (bike_sharing_df["dteday"] <= pd.to_datetime(end_date))
]

# Menghasilkan DataFrame hasil resample dan agregasi
daily_rentals_df = filtered_df(main_df)

# Membuat header dan layout Streamlit
st.header('Bike Sharing Dashboard 🚲')

col1, col2 = st.columns(2)

# Membuat plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_rentals_df["dteday"], daily_rentals_df[("cnt", "sum")], marker='o', linewidth=2, color="#72BCD4")
ax.set_title("Number of Rentals per Month", fontsize=16)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
fig.autofmt_xdate()
ax.grid()

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Pie Chart
casual_total = daily_rentals_df[("casual", "sum")].sum()
registered_total = daily_rentals_df[("registered", "sum")].sum()

# Data untuk pie chart
labels = ['Casual', 'Registered']
sizes = [casual_total, registered_total]
colors = ['#ff9999', '#66b3ff']
wedgeprops = {
    'linewidth': 5,    # Ketebalan garis tepi
    'edgecolor': 'white'  # Warna garis tepi
}

# Membuat pie chart
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops=wedgeprops)
ax.set_title('Comparison of Casual and Registered Users')
# Menampilkan pie chart di Streamlit
st.pyplot(fig)