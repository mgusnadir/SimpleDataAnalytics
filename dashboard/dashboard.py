import streamlit as st
import pandas as pd
import plotly.express as px
from pandas.plotting import register_matplotlib_converters

shunyi_df = pd.read_csv("dashboard/shunyi_cleaned.csv")

def distribusi_kualitas_udara():
    
    tabel_distribusi_kualitas_udara = pd.pivot_table(shunyi_df, values='PM2.5', index='year', columns='Kategori Kualitas Udara', aggfunc='count', fill_value=0)

    map_color = {
        'Baik': '#ffffff',
        'Sedang': '#ffd3cc',
        'Tidak Sehat': '#ff9380',
        'Sangat Tidak Sehat': '#ff674d',
        'Berbahaya': '#ff2701'
    }

    ordered_categories = ['Baik', 'Sedang', 'Tidak Sehat', 'Sangat Tidak Sehat', 'Berbahaya']

    fig = px.bar(
        tabel_distribusi_kualitas_udara ,
        x=tabel_distribusi_kualitas_udara .index,
        y=tabel_distribusi_kualitas_udara .columns,
        barmode='group',
        color_discrete_map=map_color,
        category_orders={'Kategori Kualitas Udara': ordered_categories}
    )

    fig.update_layout(
        title='Distribusi Kualitas Udara di Stasiun Shunyi per Tahun',
        xaxis_title='Tahun',
        yaxis_title='Jumlah',
        legend_title='Kategori Kualitas Udara'
    )
    
    st.plotly_chart(fig)

def plot_air_quality_trends(shunyi_df):

    st.sidebar.title("Filter Data")
    start_year = st.sidebar.slider("Select start year", min_value=shunyi_df['year'].min(), max_value=shunyi_df['year'].max())
    end_year = st.sidebar.slider("Select end year", min_value=shunyi_df['year'].min(), max_value=shunyi_df['year'].max())


    data_filter = shunyi_df[(shunyi_df['year'] >= start_year) & (shunyi_df['year'] <= end_year)]

    custom_color = ['#ffffff', '#ffd3cc', '#ff9380', '#ff674d', '#ff2701']

    tabel_trend = pd.pivot_table(data_filter, values='PM2.5', index='year', columns='Kategori Kualitas Udara', aggfunc='count', fill_value=0)
    urutan_kualitas_udara = ['Baik', 'Sedang', 'Tidak Sehat', 'Sangat Tidak Sehat', 'Berbahaya']
    tabel_trend = tabel_trend[urutan_kualitas_udara].sort_index()

    tabel_trend = tabel_trend.reset_index().melt(id_vars='year', var_name='Kategori Kualitas Udara', value_name='Count')

    fig = px.line(tabel_trend, x='year', y='Count', color='Kategori Kualitas Udara', markers=True,
                  title=f'Tren Kualitas Udara di Shunyi Station ({start_year}-{end_year})',
                  labels={'Count': 'Jumlah', 'year': 'Tahun'},
                  line_shape='linear', render_mode='svg',
                  color_discrete_sequence=custom_color)

    st.plotly_chart(fig)

def plot_average_values():
    

    wspm_tabel = shunyi_df.pivot_table(values='WSPM', index='year', aggfunc='mean')
    # Menentukan warna untuk bar dengan nilai tertinggi
    max_wspm_color = ['blue' if value == wspm_tabel['WSPM'].max() else 'lightblue' for value in wspm_tabel['WSPM']]

    fig_wspm = px.bar(
        wspm_tabel, 
        x=wspm_tabel.index, 
        y='WSPM',
        title='Rata-rata Kecepatan Angin (WSPM) per Tahun di Stasiun Shunyi',
        labels={'WSPM': 'Rata-rata WSPM dalam m/s'},
        color=max_wspm_color
    )
    st.plotly_chart(fig_wspm)


    rain_tabel = shunyi_df.pivot_table(values='RAIN', index='year', aggfunc='mean')
    max_rain_color = ['blue' if value == rain_tabel['RAIN'].max() else 'lightblue' for value in rain_tabel['RAIN']]

    fig_rain = px.bar(
        rain_tabel, 
        x=rain_tabel.index, 
        y='RAIN',
        title='Rata-rata Curah Hujan (RAIN) per Tahun di Stasiun Shunyi',
        labels={'RAIN': 'Rata-rata Curah Hujan (RAIN) dalam mm'},
        color=max_rain_color
    )
    st.plotly_chart(fig_rain)



    pm25_tabel = shunyi_df.pivot_table(values='PM2.5', index='year', aggfunc='mean')
    max_pm25_color = ['blue' if value == pm25_tabel['PM2.5'].max() else 'lightblue' for value in pm25_tabel['PM2.5']]

    fig_pm25 = px.bar(
        pm25_tabel, 
        x=pm25_tabel.index, 
        y='PM2.5',
        title='Rata-rata Polusi Udara (PM2.5) per Tahun di Stasiun Shunyi',
        labels={'PM2.5': 'Rata-rata PM2.5 dalam µg/m³'},
        color=max_pm25_color  
    )
    st.plotly_chart(fig_pm25)

def plot_correlation_heatmap():
    
    wspm_rain_pm25_cor = ['PM2.5', 'WSPM', 'RAIN']
    correlation_mat = shunyi_df[wspm_rain_pm25_cor].corr()

    fig = px.imshow(
        correlation_mat,
        labels=dict(x='Variable', y='Variable', color='Correlation'),
        x=wspm_rain_pm25_cor,
        y=wspm_rain_pm25_cor,
        color_continuous_scale=[
            [0, '#ff2701'], 
            [0.5, '#ffffff'],  
            [1, '#0b51c1'],  
        ],
        color_continuous_midpoint=0
    )

    fig.update_layout(
        title='Heatmap Korelasi antara PM2.5, WSPM, dan RAIN di Stasiun Shunyi',
        xaxis_title='Variable',
        yaxis_title='Variable'
    )

    st.plotly_chart(fig)

# Sidebar untuk memilih chart
st.sidebar.title("Dashboard Kualitas Udara")
selected_chart = st.sidebar.selectbox("Pilih Chart", ["Distribusi Kualitas Udara", "Tren Kualitas Udara", "Rata-rata WSPM, RAIN, PM2.5", "Korelasi PM2.5, WSPM, RAIN"])

if selected_chart == "Distribusi Kualitas Udara":
    distribusi_kualitas_udara()
elif selected_chart == "Tren Kualitas Udara":
    plot_air_quality_trends(shunyi_df)
elif selected_chart == "Rata-rata WSPM, RAIN, PM2.5":
    plot_average_values()
elif selected_chart == "Korelasi PM2.5, WSPM, RAIN":
    plot_correlation_heatmap()
