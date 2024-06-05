import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import folium
from folium import plugins
from folium.plugins import HeatMap
from sklearn.metrics import silhouette_score
import plotly.express as px
from streamlit_folium import folium_static

# Set page configuration
st.set_page_config(
    page_title="KMeans Clustering and Visualization",
    layout="wide",  # Set layout to wide for full-width content
    initial_sidebar_state="collapsed",  # Collapse the sidebar by default
)

# Function to load data
@st.cache_data
def load_data(file_path):
    data = pd.read_csv("Jumlah-2021 - 2023 -Lengkap-Dataset_Longsor - PROV JABAR.csv")
    return data

# Function to perform KMeans clustering and calculate Silhouette Score
def kmeans_clustering(data, num_clusters):
    features = data[['JUMLAH_LONGSOR', 'JIWA_TERDAMPAK', 'JIWA_MENINGGAL', 'RUSAK_TERDAMPAK', 'RUSAK_RINGAN', 'RUSAK_SEDANG', 'RUSAK_BERAT', 'TERTIMBUN', 'LATITUDE', 'LONGITUDE']]
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(features)
    
    # Calculate centroid for each cluster
    centroids = data.groupby('cluster')[['JUMLAH_LONGSOR']].mean()

    # Define threshold values for density categories (adjust these based on your analysis)
    threshold_low = 10  # Example threshold for "not dense"
    threshold_high = 101  # Example threshold for "dense"

    # Add Density Category column based on centroid values
    data['Landslide Category'] = data['cluster'].map(lambda cluster: 'Tingkat Rawan Rendah' if centroids.loc[cluster].mean() < threshold_low else ('Tingkat Rawan Sedang' if centroids.loc[cluster].mean() < threshold_high else 'Tingkat Rawan Tinggi'))
    
    # Elbow Method data
    elbow_data = pd.DataFrame({'num_clusters': range(1, 11),
                               'inertia': [KMeans(n_clusters=i, random_state=42).fit(features).inertia_ for i in range(1, 11)]})
    
    return data, elbow_data

# Function to calculate silhouette scores for a range of cluster numbers
def calculate_silhouette_scores(data, max_clusters=10):
    features = data[['JUMLAH_LONGSOR', 'JIWA_TERDAMPAK', 'JIWA_MENINGGAL', 'RUSAK_TERDAMPAK', 'RUSAK_RINGAN', 'RUSAK_SEDANG', 'RUSAK_BERAT', 'TERTIMBUN', 'LATITUDE', 'LONGITUDE']]
    silhouette_scores = []
    for n_clusters in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(features)
        silhouette_avg = silhouette_score(features, labels)
        silhouette_scores.append(silhouette_avg)
    return pd.DataFrame({'num_clusters': range(2, max_clusters + 1), 'silhouette_score': silhouette_scores})

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

# Function to handle KMeans page
def kmeans_page():
    st.header("KMeans Clustering Page", anchor='center')

    st.latex(r"SSE = \sum_{i=1}^{k} \sum_{j=1}^{n} ||x_{ij} - c_i||^2")

    # Sidebar: Choose the number of clusters
    num_clusters = st.sidebar.slider("Number of Clusters", min_value=2, max_value=10, value=3)

    # Load data from the home page
    data_from_homepage = load_data('Jumlah-2021 - 2023 -Lengkap-Dataset_Longsor - PROV JABAR.csv')  # Replace with your actual data file path

    # Perform KMeans clustering
    df_clustered, elbow_data = kmeans_clustering(data_from_homepage, num_clusters)
   
    # Calculate Silhouette Scores for a range of clusters
    silhouette_scores_df = calculate_silhouette_scores(data_from_homepage)

    # Save the clustered data in session_state
    st.session_state.df_clustered = df_clustered
    st.session_state.elbow_data = elbow_data
    st.session_state.silhouette_scores_df = silhouette_scores_df

    tab1, tab2, tab3 = st.tabs(["DATASET", "VISUALISASI MAP", "SILHOUETTE SCORE"])
    
    with tab1:
        # Display metrics for each cluster
        for cluster_num in range(num_clusters):
            landslide_category = df_clustered.loc[df_clustered['cluster'] == cluster_num, 'Landslide Category'].iloc[0]
            
            # Add a new column for index
            cluster_data = df_clustered[df_clustered['cluster'] == cluster_num].reset_index(drop=True)
            cluster_data.insert(1, "Index", cluster_data.index)  # Add index column
            
            with st.expander(f"Cluster {cluster_num + 1} Data Table - {landslide_category}", expanded=True):
                st.dataframe(cluster_data,
                            column_order=("Index", "KABUPATEN", "JUMLAH_LONGSOR", "cluster"),
                            hide_index=True,
                            width=500,
                            use_container_width=True,
                            column_config={
                                "Index": st.column_config.TextColumn(
                                    "Index",
                                ),
                                "KABUPATEN": st.column_config.TextColumn(
                                    "Area",
                                )}
                            )

    with tab2:
        with st.expander('Desa Maps View Analitycs Clustering', expanded=True):
            # Use folium_static to display the Folium map
            folium_map = create_marker_map(st.session_state.df_clustered)
            folium_static(folium_map, width=1240, height=600)

        # Graphs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.expander("⬇ HISTOGRAM:"):
                # Bar chart
                st.bar_chart(df_clustered.groupby('cluster').size(), use_container_width=True)

        with col2:
            with st.expander("⬇ DONUT CHART:"):
                # Donut chart
                fig = px.pie(df_clustered, names='cluster', hole=0.3)
                st.plotly_chart(fig, use_container_width=True)

        with col3:
            with st.expander("⬇ SCATTERPLOT:"):
                scatter_plot = px.scatter(df_clustered, x='LATITUDE', y='LONGITUDE', color='cluster',
                                          hover_data=['KABUPATEN'])
                st.plotly_chart(scatter_plot, use_container_width=True)
                
        with col4:
            with st.expander("⬇ ELBOW METHOD:"):
                fig_elbow = px.line(elbow_data, x='num_clusters', y='inertia', markers=True, title='Elbow Method',
                                    labels={'num_clusters': 'Number of Clusters', 'inertia': 'Inertia'})
                fig_elbow.update_layout(
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
                    yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
                    font=dict(color='#cecdcd'),
                )
                st.plotly_chart(fig_elbow, use_container_width=True)
                
        with st.expander('Informasi', expanded=True):
            st.write('''
            - **Klastering Data Bencana Longsor:** Data telah dikelompokkan ke dalam beberapa klaster berdasarkan jumlah longsor dan faktor lainnya.
            - **Peta Klastering:** Titik-titik merah menandakan lokasi longsor di peta, dengan warna yang berbeda-beda sesuai dengan klaster.
            - **Histogram:** Histogram menunjukkan distribusi jumlah longsor di setiap klaster.
            - **Donut Chart:** Grafik donat menunjukkan proporsi jumlah longsor dalam setiap klaster.
            - **Scatterplot:** Scatterplot memvisualisasikan lokasi longsor dengan sumbu x dan y sebagai koordinat lintang dan bujur.
            - **Elbow Method:** Grafik ini membantu menentukan jumlah klaster yang optimal berdasarkan metode elbow.
            ''')

    with tab3:
        col = st.columns((5, 1.5), gap='medium')
    
        with col[0]:
            st.expander('Desa Maps View Silhouette Score Clustering', expanded=True)
            # Line plot for silhouette scores
            silhouette_line_plot = px.line(silhouette_scores_df, x='num_clusters', y='silhouette_score',
                                           markers=True, labels={'num_clusters': 'Number of Clusters', 'silhouette_score': 'Silhouette Score'})
            st.plotly_chart(silhouette_line_plot, use_container_width=True)
    
        with col[1]:
            st.write(silhouette_scores_df)
    
        best_silhouette_score = silhouette_scores_df['silhouette_score'].max()
        best_cluster_number = silhouette_scores_df.loc[silhouette_scores_df['silhouette_score'] == best_silhouette_score, 'num_clusters'].values[0]
    
        with st.expander('Informasi', expanded=True):
            st.write('''
            - Data: [Sumber Data](link_sumber_data_anda).
            - :orange[**Evaluasi Kualitas Klastering dengan Silhouette Score**]: Silhouette Score memberikan gambaran tentang seberapa baik data dapat dikelompokkan secara alami. Semakin tinggi nilai Silhouette Score, semakin jelas pemisahan antara klaster, yang menunjukkan struktur yang lebih baik dalam data. Namun, penting untuk dicatat bahwa Silhouette Score juga dapat membantu mengidentifikasi apakah ada klaster yang mungkin terlalu rapat (nilai mendekati 0) atau terlalu longgar (nilai negatif).
            - :chart_with_upwards_trend: **Perbaikan Klastering**: Dengan memonitor perubahan Silhouette Score seiring dengan penambahan atau pengurangan jumlah klaster, pengguna dapat mengeksplorasi bagaimana perubahan konfigurasi klastering dapat mempengaruhi kualitas klastering secara keseluruhan.
            - :star: **Hasil Terbaik**: Klastering terbaik ditemukan saat menggunakan {best_cluster_number} klaster, dengan nilai Silhouette Score tertinggi mencapai {best_silhouette_score:.3f}. Ini menunjukkan struktur klaster yang sangat baik dalam data Anda!
            ''')





# Run the Streamlit app
if __name__ == "__main__":
    kmeans_page()
