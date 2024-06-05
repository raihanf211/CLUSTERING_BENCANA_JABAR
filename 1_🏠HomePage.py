import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import folium_static
from folium import plugins
import altair as alt


# Set page configuration
st.set_page_config(
    page_title="Analisis Bencana Longsor Di Provinsi Jawa Barat",
    layout="wide",  # Set layout to wide for full-width content
    initial_sidebar_state="collapsed",  # Collapse the sidebar by default
)

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


# Aplikasi Streamlit
st.title('ANALISIS BENCANA LONGSOR JAWA BARAT')

# Load your DataFrame from DATA_JABAR.csv
file_path = 'UPDATE-Selection-Dataset_Longsor 2021 - 2023 - PROV JABAR.csv'
df = pd.read_csv(file_path)

# Sidebar for selecting the year
selected_year = st.sidebar.slider('Select Year', min_value=df['TAHUN'].min(), max_value=df['TAHUN'].max(), value=df['TAHUN'].max(), step=1)

# Create a map with a unique key based on the selected year
m = folium.Map(location=[df['LATITUDE'].mean(), df['LONGITUDE'].mean()], zoom_start=10, key=f"map-{selected_year}", width='100%')

# Add a marker for each data point
for i, row in df[df['TAHUN'] == selected_year].iterrows():
    popup_content = f"""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <div style='width:400px; height:300px;'>
        <ul class="list-group">
            <li class="list-group-item active" aria-current="true">
                <h3 class="mb-0">Information of {row['KABUPATEN']}</h3>
            </li>
            <li class="list-group-item">
                <b>Number of Landslides:</b> {row['JUMLAH_LONGSOR']}
            </li>
            <li class="list-group-item">
                <b>Affected Population:</b> {row['JIWA_TERDAMPAK']}
            </li>
            <li class="list-group-item">
                <b>Deaths:</b> {row['JIWA_MENINGGAL']}
            </li>
            <li class="list-group-item">
                <b>Infrastructure Affected:</b> {row['RUSAK_TERDAMPAK']}
            </li>
            <li class="list-group-item">
                <b>Minor Damage:</b> {row['RUSAK_RINGAN']}
            </li>
            <li class="list-group-item">
                <b>Moderate Damage:</b> {row['RUSAK_SEDANG']}
            </li>
            <li class="list-group-item">
                <b>Severe Damage:</b> {row['RUSAK_BERAT']}
            </li>
            <li class="list-group-item">
                <b>Buried:</b> {row['TERTIMBUN']}
            </li>
            <li class="list-group-item">
                <h4>Latitude: {row['LATITUDE']}</h4>
            </li>
            <li class="list-group-item">
                <h4>Longitude: {row['LONGITUDE']}</h4>
            </li>
        </ul>
    </div>
"""

    folium.Marker(
    location=[row['LATITUDE'], row['LONGITUDE']],
    tooltip=row['KABUPATEN'],
    icon=folium.Icon(color='red', icon='exclamation-triangle-fill', prefix='fa'),  # Menggunakan ikon untuk longsor
).add_to(m).add_child(folium.Popup(popup_content, max_width=600))



# Heatmap Layer
heat_data = [[row['LATITUDE'], row['LONGITUDE']] for _, row in df[df['TAHUN'] == selected_year].iterrows()]
HeatMap(heat_data).add_to(m)

# Fullscreen Control
plugins.Fullscreen(position='topright', title='Fullscreen', title_cancel='Exit Fullscreen').add_to(m)

# Drawing Tools
draw = plugins.Draw()
draw.add_to(m)

def add_google_maps(m):
    tiles = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
    attr = "Google Digital Satellite"
    folium.TileLayer(tiles=tiles, attr=attr, name=attr, overlay=True, control=True).add_to(m)
    # Add labels for streets and objects
    label_tiles = "https://mt1.google.com/vt/lyrs=h&x={x}&y={y}&z={z}"
    label_attr = "Google Labels"
    folium.TileLayer(tiles=label_tiles, attr=label_attr, name=label_attr, overlay=True, control=True).add_to(m)

    return m

# Function for creating a heatmap with color theme selection
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="TAHUN", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        color=alt.Color(f'{input_color}:Q',
                        legend=None,
                        scale=alt.Scale(scheme=input_color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
    ).properties(width=500  # Adjust width as needed
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    return heatmap

# Fungsi format_number untuk memformat angka dengan koma sebagai pemisah ribuan
def format_number(num):
    return "{:,}".format(num)

# Fungsi perhitungan migrasi penduduk tahun ke tahun
def calculate_population_difference(input_df, input_year):
    selected_year_data = input_df[input_df['TAHUN'] == input_year].reset_index()
    previous_year_data = input_df[input_df['TAHUN'] == input_year - 1].reset_index()
    selected_year_data['population_difference'] = selected_year_data['JUMLAH_LONGSOR'].sub(previous_year_data['JUMLAH_LONGSOR'], fill_value=0)
    return pd.concat([selected_year_data['KABUPATEN'], selected_year_data['TAHUN'], selected_year_data['JUMLAH_LONGSOR'], selected_year_data['population_difference']], axis=1).sort_values(by="population_difference", ascending=False)

# Main Dashboard Panel
col = st.columns((1.5, 5, 2), gap='medium')

with col[0]:
    df_population_difference_sorted = calculate_population_difference(df, selected_year)
    if selected_year > 2020:
        first_state_name = df_population_difference_sorted['KABUPATEN'].iloc[0]
        first_state_population = format_number(int(df_population_difference_sorted['JUMLAH_LONGSOR'].iloc[0]))
        first_state_delta = format_number(int(df_population_difference_sorted['population_difference'].iloc[0]))
    else:
        first_state_name = '-'
        first_state_population = '-'
        first_state_delta = ''
    st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

    if selected_year > 2020:
        last_state_name = df_population_difference_sorted['KABUPATEN'].iloc[-1]
        last_state_population = format_number(int(df_population_difference_sorted['JUMLAH_LONGSOR'].iloc[-1]))   
        last_state_delta = format_number(int(df_population_difference_sorted['population_difference'].iloc[-1]))   
    else:
        last_state_name = '-'
        last_state_population = '-'
        last_state_delta = ''
    st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

    if selected_year > 2020:
        total_landslides_selected_year = df[df['TAHUN'] == selected_year]['JUMLAH_LONGSOR'].sum()
        total_landslides_last_year = df[df['TAHUN'] == selected_year - 1]['JUMLAH_LONGSOR'].sum()
        landslide_difference = total_landslides_selected_year - total_landslides_last_year

        total_landslides_name = "Total Landslides"
        total_landslides_value = format_number(total_landslides_selected_year)
        total_landslides_delta = format_number(landslide_difference) if landslide_difference != 0 else "0"

        st.metric(label=total_landslides_name, value=total_landslides_value, delta=total_landslides_delta)
    else:
        st.metric(label="-", value="-", delta="")


with col[1]:
    with st.container(border=True):
        m = add_google_maps(m)
        m.add_child(folium.LayerControl(collapsed=False))
        folium_static(m, width=700, height=450)

with col[2]:
    # Filter the dataframe based on the selected year
    df_filtered = df[df['TAHUN'] == selected_year]
    
    # Sort the filtered dataframe by the number of landslides
    df_landslide_sorted = df_filtered.sort_values(by="JUMLAH_LONGSOR", ascending=False)
    
    # Drop the LATITUDE and LONGITUDE columns for display purposes
    df_landslide_sorted_no_geom = df_landslide_sorted.drop(columns=['LATITUDE', 'LONGITUDE'])

    # Display the dataframe
    st.dataframe(df_landslide_sorted_no_geom,
                 column_order=("KABUPATEN", "JUMLAH_LONGSOR"),
                 hide_index=True,
                 width=500,
                 column_config={
                     "KABUPATEN": st.column_config.TextColumn(
                         "Area",
                     ),
                     "JUMLAH_LONGSOR": st.column_config.ProgressColumn(
                         "Number of Landslides",
                         format="%f",
                         min_value=0,
                         max_value=max(df_landslide_sorted.JUMLAH_LONGSOR),
                     )}
                 )


with st.expander("HeatMap", expanded=False):
    st.markdown('#### HeatMap')

    heatmap_chart = make_heatmap(df, 'TAHUN', 'KABUPATEN', 'JUMLAH_LONGSOR', 'viridis') # Assuming 'viridis' as the color theme

    st.altair_chart(heatmap_chart, use_container_width=True)

# Calculate total landslides for the selected year
total_landslides_selected_year = df[df['TAHUN'] == selected_year]['JUMLAH_LONGSOR'].sum()

with st.expander('Informasi', expanded=True):
    st.write(f'''
        - **Sumber Data**: [Data Longsor Provinsi Jawa Barat](link_sumber_data_anda).
        - :orange[**Area Prioritas Berdasarkan Longsor**]: Kabupaten dengan jumlah longsor tertinggi untuk tahun yang dipilih.
        - :orange[**Perubahan Longsor yang Signifikan**]: Area dengan peningkatan atau penurunan jumlah longsor terbesar dari tahun sebelumnya.
        - :information_source: **Total Longsor**: Total jumlah kejadian longsor pada tahun yang dipilih adalah {total_landslides_selected_year}.
        - :information_source: **Populasi Terdampak**: Total jumlah orang yang terdampak longsor pada tahun yang dipilih.
        - :information_source: **Kerusakan Infrastruktur**: Rincian kerusakan infrastruktur akibat longsor (ringan, sedang, berat) pada tahun yang dipilih.
        - :bar_chart: **Visualisasi Peta Panas**: Peta panas yang menunjukkan distribusi longsor di berbagai area.
        - :chart_with_upwards_trend: **Tren Longsor**: Dinamika dan tren longsor, termasuk peningkatan/penurunan dan area dengan jumlah longsor tertinggi dan terendah setiap tahunnya.
    ''')

