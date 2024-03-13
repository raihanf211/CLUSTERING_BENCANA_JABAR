import streamlit as st
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import plotly_express as px
from folium import plugins


# Set Streamlit options
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load the dataset
df = pd.read_csv("DATA_JABAR.csv")

# Set Streamlit page configuration
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

# Read CSS file for styling
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to perform Agglomerative Hierarchical Clustering based on selected features and linkage
def ahc_clustering(data, n_clusters, selected_features, linkage_method):
    features = data[selected_features + ['LATITUDE', 'LONGITUDE']]
    clusterer = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_method)
    data['cluster'] = clusterer.fit_predict(features)

    # Calculate centroid for each cluster
    centroids = data.groupby('cluster')[['JUMLAH_LONGSOR']].mean()

    # Define threshold values for density categories (adjust these based on your analysis)
    threshold_low = 20  # Example threshold for "not dense"
    threshold_high = 50  # Example threshold for "dense"

    # Add Density Category column based on centroid values
    data['Landslide Category'] = data['cluster'].map(lambda cluster: 'Tingkat Rawan Rendah' if centroids.loc[cluster].mean() < threshold_low else ('Tingkat Rawan Sedang' if centroids.loc[cluster].mean() < threshold_high else 'Tingkat Rawan Tinggi'))
    
    return data

# Function to add Google Maps to Folium map
def add_google_maps(m):
    tiles = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
    attr = "Google Digital Satellite"
    folium.TileLayer(tiles=tiles, attr=attr, name=attr, overlay=True, control=True).add_to(m)

    # Add labels for streets and objects
    label_tiles = "https://mt1.google.com/vt/lyrs=h&x={x}&y={y}&z={z}"
    label_attr = "Google Labels"
    folium.TileLayer(tiles=label_tiles, attr=label_attr, name=label_attr, overlay=True, control=True).add_to(m)

    return m

# Function to create Folium map with clustered markers
def create_marker_map(df_clustered):
    # Set the width and height directly when creating the Folium map
    m = folium.Map(location=[df_clustered['LATITUDE'].mean(), df_clustered['LONGITUDE'].mean()], zoom_start=10, width=1240, height=600)

    # Add a marker for each data point
    for i, row in df_clustered.iterrows():
        # Customize popup content
        popup_content = f"""
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <div style='width:400px; height:300px;'>
            <ul class="list-group">
                <li class="list-group-item active" aria-current="true">
                    <h3 class="mb-0">Cluster Information</h3>
                </li>
                <li class="list-group-item">Cluster Number: {row['cluster']}</li>
                <li class="list-group-item">KABUPATEN: {row['KABUPATEN']}</li>
                <li class="list-group-item">TAHUN: {row['TAHUN']}</li>
                <li class="list-group-item">JUMLAH_LONGSOR: {row['JUMLAH_LONGSOR']}</li>
                <li class="list-group-item">JIWA_TERDAMPAK: {row['JIWA_TERDAMPAK']}</li>
                <li class="list-group-item">JIWA_MENINGGAL: {row['JIWA_MENINGGAL']}</li>
                <li class="list-group-item">RUSAK_TERDAMPAK: {row['RUSAK_TERDAMPAK']}</li>
                <li class="list-group-item">RUSAK_RINGAN: {row['RUSAK_RINGAN']}</li>
                <li class="list-group-item">RUSAK_SEDANG: {row['RUSAK_SEDANG']}</li>
                <li class="list-group-item">RUSAK_BERAT: {row['RUSAK_BERAT']}</li>
                <li class="list-group-item">TERTIMBUN: {row['TERTIMBUN']}</li>
            </ul>
        </div>
        """

        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            tooltip=row['KABUPATEN'],
            icon=folium.Icon(color='red', icon='home', prefix='fa'),
        ).add_to(m).add_child(folium.Popup(popup_content, max_width=1240))

    # Heatmap Layer
    heat_data = [[row['LATITUDE'], row['LONGITUDE']] for _, row in df_clustered.iterrows()]
    HeatMap(heat_data).add_to(m)
    # Drawing Tools
    draw = plugins.Draw()
    draw.add_to(m)

    # Add Google Maps
    add_google_maps(m)

    return m

# Function to handle Agglomerative Hierarchical Clustering page
def ahc_page():
    center = True
    st.header("Agglomerative Hierarchical Clustering Page", anchor='center' if center else 'left')

    # Sidebar: Choose the number of clusters
    num_clusters = st.sidebar.slider("Number of Clusters", min_value=2, max_value=10, value=1)

    # Sidebar: Select Year
    selected_year = st.sidebar.selectbox('Select year', ['2021', '2022', '2023'])

    # Sidebar: Choose the linkage method
    linkage_method = st.sidebar.selectbox('Select Linkage Method', ['complete', 'single', 'average'])

    # Load data from the home page
    data_from_homepage = pd.read_csv('DATA_JABAR.csv')  # Replace with the actual path to your CSV file

    # Filter data for the selected year
    filtered_data = data_from_homepage[data_from_homepage['TAHUN'] == int(selected_year)]

    # Perform Agglomerative Hierarchical Clustering based on selected features and linkage method
    if len(filtered_data) >= 2:
        df_clustered = ahc_clustering(filtered_data, num_clusters, [], linkage_method)  # Empty list for selected_features
    else:
        # Handle the case when there are not enough data points for clustering
        st.warning("Not enough data points for clustering. Please select different criteria.")
        return

    # Save the clustered data in session_state
    st.session_state.df_clustered = df_clustered

    tab1, tab2 = st.tabs(["DATASET", "VISUALISASI MAP"])

    with tab1:
        # Display metrics for each cluster
        for cluster_num in range(num_clusters):

            landslide_category = df_clustered.loc[df_clustered['cluster'] == cluster_num, 'Landslide Category'].iloc[0]


            cluster_data = df_clustered[df_clustered['cluster'] == cluster_num][["KABUPATEN", "cluster"]]

            with st.expander(f"Cluster {cluster_num + 1} Data Table - {landslide_category}", expanded=True):
                st.dataframe(cluster_data,
                            column_order=("KABUPATEN", "cluster"),
                            hide_index=True,
                            width=500,
                            use_container_width=True,
                            column_config={
                                "KABUPATEN": st.column_config.TextColumn(
                                    "Area",
                                )}
                            )


    with tab2:
        with st.expander('Desa Maps View Analytics Clustering', expanded=True):
            # Use folium_static to display the Folium map
            folium_map = create_marker_map(st.session_state.df_clustered)
            folium_static(folium_map, width=1240, height=600)

        # Graphs
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                # Bar chart
                st.bar_chart(df_clustered.groupby('cluster').size(), use_container_width=True)

        with col2:
            with st.container(border=True):
                # Pie chart
                st.write("Cluster Distribution:")
                st.plotly_chart(px.pie(df_clustered, names='cluster', title='Cluster Distribution'), use_container_width=True)

        with col3:
            with st.expander("⬇ SCATTER PLOT:"):
                    st.write("Scatter Plot:")
            
                    # Assuming 'LATITUDE' and 'LONGITUDE' are the columns you want to use for the scatter plot
                    scatter_fig = px.scatter(st.session_state.df_clustered, x='LATITUDE', y='LONGITUDE', color='cluster', title='Scatter Plot')
                    st.plotly_chart(scatter_fig, use_container_width=True)

        with st.expander('Informasi', expanded=True):
            st.write('''
            - Data: [Data Penduduk Kabupaten Purwakarta](your_data_source_link).
            - :orange[**Area Teratas berdasarkan Penduduk**]: Area dengan penduduk tertinggi untuk tahun yang dipilih.
            - :orange[**Perubahan Penduduk Ekstrem**]: Area dengan peningkatan dan penurunan penduduk terbesar dari tahun sebelumnya.
            - :information_source: **Rata-rata Penduduk:** Rata-rata penduduk untuk tahun yang dipilih.
            - :information_source: **Rata-rata Penduduk (Area Teratas):** Rata-rata penduduk di area teratas.
            - :information_source: **Modus Penduduk (Area Teratas):** Modus penduduk di area teratas.
            - :bar_chart: **Visualisasi Penduduk:** Peta korelasi dan peta panas menampilkan total penduduk di berbagai area.
            - :chart_with_upwards_trend: **Tren Penduduk:** Kenaikan/Penurunan, Area Teratas/Terendah berdasarkan Penduduk, dan Perubahan Penduduk Ekstrem divisualisasikan untuk memberikan wawasan tentang dinamika penduduk.
            ''')

if __name__ == "__main__":
    # Call the ahc_page function
    ahc_page()
