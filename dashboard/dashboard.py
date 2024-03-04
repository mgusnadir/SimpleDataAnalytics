import streamlit as st
import pandas as pd
import plotly.express as px
from pandas.plotting import register_matplotlib_converters

st.set_option('deprecation.showPyplotGlobalUse', False)

# Membaca data frame
shunyi_df = pd.read_csv("dashboard/shunyi_cleaned.csv")

def plot_air_quality_distribution():
    # Membuat pivot table
    pivot_table = pd.pivot_table(shunyi_df, values='PM2.5', index='year', columns='Kategori Kualitas Udara', aggfunc='count', fill_value=0)

    # Plotly bar chart
    color_map = {
        'Baik': '#ffffff',
        'Sedang': '#ffd3cc',
        'Tidak Sehat': '#ff9380',
        'Sangat Tidak Sehat': '#ff674d',
        'Berbahaya': '#ff2701'
    }

    ordered_categories = ['Baik', 'Sedang', 'Tidak Sehat', 'Sangat Tidak Sehat', 'Berbahaya']

    fig = px.bar(
        pivot_table,
        x=pivot_table.index,
        y=pivot_table.columns,
        barmode='group',
        color_discrete_map=color_map,
        category_orders={'Kategori Kualitas Udara': ordered_categories}
    )

    fig.update_layout(
        title='Distribusi Kualitas Udara di Stasiun Shunyi per Tahun',
        xaxis_title='Tahun',
        yaxis_title='Jumlah',
        legend_title='Kategori Kualitas Udara'
    )

    # Menampilkan chart pada Streamlit
    st.plotly_chart(fig)

def plot_air_quality_trends(shunyi_df):
    # Sidebar for user input
    st.sidebar.title("Filter Data")
    start_year = st.sidebar.slider("Select start year", min_value=shunyi_df['year'].min(), max_value=shunyi_df['year'].max(), value=2013)
    end_year = st.sidebar.slider("Select end year", min_value=shunyi_df['year'].min(), max_value=shunyi_df['year'].max(), value=2016)

    # Filter data based on user input
    filtered_data = shunyi_df[(shunyi_df['year'] >= start_year) & (shunyi_df['year'] <= end_year)]

    # Define custom colors
    custom_colors = ['#ffffff', '#ffd3cc', '#ff9380', '#ff674d', '#ff2701']

    # Pivot table for filtered data
    pivot_table = pd.pivot_table(filtered_data, values='PM2.5', index='year', columns='Kategori Kualitas Udara', aggfunc='count', fill_value=0)
    kualitas_udara_order = ['Baik', 'Sedang', 'Tidak Sehat', 'Sangat Tidak Sehat', 'Berbahaya']
    pivot_table = pivot_table[kualitas_udara_order].sort_index()

    # Convert to long format for Plotly Express
    pivot_table = pivot_table.reset_index().melt(id_vars='year', var_name='Kategori Kualitas Udara', value_name='Count')

    # Plot using Plotly Express with custom colors
    fig = px.line(pivot_table, x='year', y='Count', color='Kategori Kualitas Udara', markers=True,
                  title=f'Tren Kualitas Udara di Shunyi Station ({start_year}-{end_year})',
                  labels={'Count': 'Jumlah', 'year': 'Tahun'},
                  line_shape='linear', render_mode='svg',
                  color_discrete_sequence=custom_colors)

    # Display chart in Streamlit
    st.plotly_chart(fig)

def plot_average_values():
    
    # Buat pivot table untuk rata-rata WSPM per tahun
    wspm_pivot_table = shunyi_df.pivot_table(values='WSPM', index='year', aggfunc='mean')

    # Tentukan warna untuk bar dengan nilai tertinggi
    max_wspm_color = ['blue' if value == wspm_pivot_table['WSPM'].max() else 'lightblue' for value in wspm_pivot_table['WSPM']]

    # Plotly bar chart for WSPM
    fig_wspm = px.bar(
        wspm_pivot_table, 
        x=wspm_pivot_table.index, 
        y='WSPM',
        title='Rata-rata Kecepatan Angin (WSPM) per Tahun di Stasiun Shunyi',
        labels={'WSPM': 'Rata-rata WSPM dalam m/s'},
        color=max_wspm_color  # Atur warna bar dengan nilai tertinggi menjadi biru
    )

    # Menampilkan chart WSPM pada Streamlit
    st.plotly_chart(fig_wspm)

    # Buat pivot table untuk rata-rata RAIN per tahun
    rain_pivot_table = shunyi_df.pivot_table(values='RAIN', index='year', aggfunc='mean')

    # Tentukan warna untuk bar dengan nilai tertinggi
    max_rain_color = ['blue' if value == rain_pivot_table['RAIN'].max() else 'lightblue' for value in rain_pivot_table['RAIN']]

    # Plotly bar chart for RAIN
    fig_rain = px.bar(
        rain_pivot_table, 
        x=rain_pivot_table.index, 
        y='RAIN',
        title='Rata-rata Curah Hujan (RAIN) per Tahun di Stasiun Shunyi',
        labels={'RAIN': 'Rata-rata Curah Hujan (RAIN) dalam mm'},
        color=max_rain_color  # Atur warna bar dengan nilai tertinggi menjadi biru
    )

    # Menampilkan chart RAIN pada Streamlit
    st.plotly_chart(fig_rain)


    # Buat pivot table untuk rata-rata PM2.5 per tahun
    pm25_pivot_table = shunyi_df.pivot_table(values='PM2.5', index='year', aggfunc='mean')

    max_pm25_color = ['blue' if value == pm25_pivot_table['PM2.5'].max() else 'lightblue' for value in pm25_pivot_table['PM2.5']]

    # Plotly bar chart for PM2.5
    fig_pm25 = px.bar(
        pm25_pivot_table, 
        x=pm25_pivot_table.index, 
        y='PM2.5',
        title='Rata-rata Polusi Udara (PM2.5) per Tahun di Stasiun Shunyi',
        labels={'PM2.5': 'Rata-rata PM2.5 dalam µg/m³'},
        color=max_pm25_color  # Atur warna bar dengan nilai tertinggi menjadi biru
    )

    # Menampilkan chart PM2.5 pada Streamlit
    st.plotly_chart(fig_pm25)

def plot_correlation_heatmap():
    wspm_rain_pm25_cor = ['PM2.5', 'WSPM', 'RAIN']
    correlation_mat = shunyi_df[wspm_rain_pm25_cor].corr()

    # Plotly heatmap with custom colors
    fig = px.imshow(
        correlation_mat,
        labels=dict(x='Variable', y='Variable', color='Correlation'),
        x=wspm_rain_pm25_cor,
        y=wspm_rain_pm25_cor,
        color_continuous_scale=[
            [0, '#ff2701'],  # red for negative correlation
            [0.5, '#ffffff'],  # white for no correlation
            [1, '#0b51c1'],  # blue for positive correlation
        ],
        color_continuous_midpoint=0
    )

    fig.update_layout(
        title='Heatmap Korelasi antara PM2.5, WSPM, dan RAIN di Stasiun Shunyi',
        xaxis_title='Variable',
        yaxis_title='Variable'
    )

    # Menampilkan chart pada Streamlit
    st.plotly_chart(fig)

# Sidebar untuk memilih chart
st.sidebar.title("Dashboard Kualitas Udara")
selected_chart = st.sidebar.selectbox("Pilih Chart", ["Distribusi Kualitas Udara", "Tren Kualitas Udara", "Rata-rata WSPM, RAIN, PM2.5", "Korelasi PM2.5, WSPM, RAIN"])

# Memanggil fungsi sesuai dengan pilihan
if selected_chart == "Distribusi Kualitas Udara":
    plot_air_quality_distribution()
elif selected_chart == "Tren Kualitas Udara":
    plot_air_quality_trends(shunyi_df)
elif selected_chart == "Rata-rata WSPM, RAIN, PM2.5":
    plot_average_values()
elif selected_chart == "Korelasi PM2.5, WSPM, RAIN":
    plot_correlation_heatmap()
