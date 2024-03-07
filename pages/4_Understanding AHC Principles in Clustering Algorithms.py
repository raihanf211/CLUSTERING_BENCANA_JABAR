import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import cophenet, dendrogram, linkage
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import fcluster
from streamlit_folium import folium_static
import folium
from folium import plugins
from folium.plugins import HeatMap
import plotly_express as px

# Set page configuration
st.set_page_config(
    page_title="Dashboard",
    page_icon="📈",
    layout="wide"
)

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header("UNDERSTANDING AGGLOMERATIVE HIERARCHICAL CLUSTERING (AHC)")

st.latex(r"d(x, y) = \sqrt{(x_1 - y_1)^2 + (x_2 - y_2)^2 + \ldots + (x_n - y_n)^2}")

# Explanation of AHC
st.markdown(
 """
 <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
 <hr>

<div class="card mb-3">
<div class="card">
  <div class="card-body">
    <h3 class="card-title" style="color:#007710;"><strong>⏱ PEMAHAMAN ALGORITMA KMEANS DALAM KLASTERISASI POPULASI</strong></h3>
    <p class="card-text">Algoritma KMeans mengelompokkan data dengan mencoba memisahkan sampel ke dalam n kelompok dengan varian yang sama, meminimalkan kriteria yang dikenal sebagai inersia atau jumlah kuadrat dalam cluster. Algoritma ini memerlukan jumlah cluster yang harus ditentukan. Ini berskala baik untuk sejumlah besar sampel dan telah digunakan di berbagai bidang aplikasi di berbagai bidang.</p>
    <p class="card-text">Algoritme K-means membagi satu set sampel ke dalam cluster yang terpisah-pisah, masing-masing dijelaskan dengan mean sampel yang ada di cluster tersebut. Sarana tersebut umumnya disebut cluster “centroids”; perhatikan bahwa secara umum poin-poin tersebut bukan berasal dari, meskipun mereka tinggal di ruang yang sama.</p>
    <p class="card-text">Algoritma KMeans bekerja dengan mencoba meminimalkan inersia atau jumlah kuadrat dalam cluster. Inersia diukur sebagai jumlah jarak kuadrat antara setiap sampel dalam cluster dengan centroidnya. Proses ini melibatkan iterasi di mana setiap sampel ditempatkan dalam cluster berdasarkan jarak Euclidean ke centroid terdekat. Centroid diupdate dengan menghitung mean dari semua sampel dalam cluster, dan proses ini diulangi hingga konvergensi.</p>
    <p class="card-text">Algoritma ini memerlukan jumlah cluster sebagai parameter input, dan pemilihan jumlah cluster yang tepat dapat dilakukan dengan menggunakan metode seperti Elbow Method.</p>
  </div>
</div>
</div>
 <style>
    [data-testid=stSidebar] {
         color: white;
         text-size:24px;
    }
</style>
""",unsafe_allow_html=True
)
# Read data
df = pd.read_csv("DATA_JABAR.csv")

# Select features for clustering
features_ahc = df[
    [
        'JUMLAH_LONGSOR',
        'JIWA_TERDAMPAK',
        'JIWA_MENINGGAL',
        'RUSAK_TERDAMPAK',
        'RUSAK_RINGAN',
        'RUSAK_SEDANG',
        'RUSAK_BERAT',
        'TERTIMBUN',
        'LATITUDE',
        'LONGITUDE'
    ]
]

# Agglomerative Hierarchical Clustering method
linkage_matrix = linkage(features_ahc, method='ward')

# Ekspander untuk menampilkan data
with st.expander("⬇ DATA UNDERSTANDING FOR AGGLOMERATIVE HIERARCHICAL CLUSTERING :"):
    # Display summary statistics
    st.write("Pendekatan statistik dari data populasi memberikan wawasan mendalam tentang karakteristik keseluruhan dari dataset. Dengan menganalisis statistik deskriptif, seperti yang ditampilkan di atas, kita dapat melihat gambaran umum tentang bagaimana nilai-nilai tersebar, tendensi sentral, dan sebaran data.")

    st.write("Selain itu, pendekatan inferensial dapat digunakan untuk membuat estimasi atau pengambilan keputusan lebih lanjut berdasarkan sampel data yang diambil dari populasi. Misalnya, penggunaan interval kepercayaan atau pengujian hipotesis dapat memberikan pemahaman lebih lanjut tentang parameter populasi.")

    st.write("Analisis spasial dengan mempertimbangkan koordinat geografis (Latitude dan Longitude), seperti yang terdapat dalam dataset, juga dapat membantu mengidentifikasi pola atau keterkaitan spasial di antara entitas populasi, memberikan wawasan lebih lanjut dalam konteks geografis.")

    st.write("### Summary Statistics:")
    st.write(df.describe())

# Choose the column for the line chart
selected_column = 'JUMLAH_LONGSOR'

# Calculate quartiles
quartiles = df[selected_column].quantile([0.25, 0.5, 0.75])

# Create columns for expanders
c1, c2, c3 = st.columns(3)

with c1:
    with st.expander("⬇ QUARTILE TIDAK PADAT"):
        # Display quartile values
        st.write(f"**Quartile Information for {selected_column}:**")
        st.write(f"- 0.25% Percentile (Q1): {quartiles[0.25]}")

        # Line chart for the 25th percentile
        fig = px.line(df, x=df.index, y=selected_column, title="Line Chart - 25th Percentile (Q1)")
        fig.update_layout(height=300, width=400)  # Adjust the size
        st.plotly_chart(fig)

with c2:
    with st.expander("⬇ QUARTILE PADAT"):
        # Display quartile values
        st.write(f"**Quartile Information for {selected_column}:**")
        st.write(f"- 50th Percentile (Q2): {quartiles[0.5]}")

        # Line chart for the 50th percentile
        fig = px.line(df, x=df.index, y=selected_column, title="Line Chart - 50th Percentile (Q2)")
        fig.update_layout(height=300, width=400)  # Adjust the size
        st.plotly_chart(fig)

with c3:
    with st.expander("⬇ QUARTILE SANGAT PADAT"):
        # Display quartile values
        st.write(f"**Quartile Information for {selected_column}:**")
        st.write(f"- 75th Percentile (Q3): {quartiles[0.75]}")

        # Line chart for the 75th percentile
        fig = px.line(df, x=df.index, y=selected_column, title="Line Chart - 75th Percentile (Q3)")
        fig.update_layout(height=300, width=400)  # Adjust the size
        st.plotly_chart(fig)

# Exploring variables
with st.expander("⬇ EKSPLORASI VARIABEL:"):
    st.subheader("Korelasi antara Variabel")
    st.write("Melihat matriks korelasi antara variabel dalam dataset.")

    selected_features = [
        'JUMLAH_LONGSOR',
        'JIWA_TERDAMPAK',
        'JIWA_MENINGGAL',
        'RUSAK_TERDAMPAK',
        'RUSAK_RINGAN',
        'RUSAK_SEDANG',
        'RUSAK_BERAT',
        'TERTIMBUN',
        'LATITUDE',
        'LONGITUDE'
    ]

    # Calculate correlation matrix
    correlation_matrix = df[selected_features].corr()

    # Plot heatmap using Plotly Express
    fig = px.imshow(correlation_matrix,
                    labels=dict(x="Features", y="Features", color="Correlation"),
                    x=selected_features,
                    y=selected_features,
                    color_continuous_scale="viridis",
                    title="Heatmap Korelasi")

    st.plotly_chart(fig)

    st.write("Visualisasi ini memberikan gambaran distribusi univariat dari setiap variabel dalam dataset. Histogram menunjukkan sebaran nilai-nilai di setiap variabel, dan kernel density estimation (KDE) memberikan perkiraan kurva distribusi.")

# checking null value
with st.expander("⬇ NULL VALUES, TENDENCY & VARIABLE DISPERSION"):
    a1, a2 = st.columns(2)
    a1.write("Jumlah nilai yang hilang (NaN atau None) di setiap kolom dalam DataFrame")
    a1.dataframe(df.isnull().sum(), use_container_width=True)

    a2.write("Insight ke dalam kecenderungan sentral, dispersi, dan distribusi data.")
    a2.dataframe(df.describe().T, use_container_width=True)

# Convert 'KABUPATEN' column to numeric
df['KABUPATEN'] = pd.factorize(df['KABUPATEN'])[0]

# Select numerical columns for clustering
numeric_columns = ['JUMLAH_LONGSOR', 'JIWA_TERDAMPAK', 'JIWA_MENINGGAL', 'RUSAK_TERDAMPAK', 'RUSAK_RINGAN', 'RUSAK_SEDANG', 'RUSAK_BERAT', 'TERTIMBUN', 'LATITUDE', 'LONGITUDE']
X_ahc = df[numeric_columns]

# Handle NaN values by filling with column means
X_ahc.fillna(X_ahc.mean(), inplace=True)

# Perform Agglomerative Hierarchical Clustering (AHC)
ahc = AgglomerativeClustering(n_clusters=None, distance_threshold=0)
df['Cluster_AHC'] = ahc.fit_predict(X_ahc)

# Calculate CCC for Ward linkage
linkage_matrix_ward = linkage(X_ahc, method='ward')
cophenet_matrix_ward, _ = cophenet(linkage_matrix_ward, pdist(X_ahc))
ccc_ward = cophenet_matrix_ward.mean()

# Calculate CCC for Complete linkage
linkage_matrix_complete = linkage(X_ahc, method='complete')
cophenet_matrix_complete, _ = cophenet(linkage_matrix_complete, pdist(X_ahc))
ccc_complete = cophenet_matrix_complete.mean()

# Calculate CCC for Average linkage
linkage_matrix_average = linkage(X_ahc, method='average')
cophenet_matrix_average, _ = cophenet(linkage_matrix_average, pdist(X_ahc))
ccc_average = cophenet_matrix_average.mean()

# Definisikan tinggi pemotongan untuk setiap metode linkage
cut_height_ward = 25  # Sesuaikan dengan visualisasi dendrogram Ward
cut_height_complete = 10.0  # Sesuaikan dengan visualisasi dendrogram Complete
cut_height_average = 5.0

# Menggunakan fcluster untuk mendapatkan label klaster
labels_ward = fcluster(linkage_matrix_ward, t=cut_height_ward, criterion='distance')
labels_complete = fcluster(linkage_matrix_complete, t=cut_height_complete, criterion='distance')
labels_average = fcluster(linkage_matrix_average, t=cut_height_average, criterion='distance')

# Menampilkan kesimpulan
c1, c2, c3 = st.columns(3)

with c1:
    with st.expander("⬇ DENDROGRAM WARD"):
        # Visualisasi Dendrogram untuk Ward
        plt.figure(figsize=(8, 6))
        dendrogram(linkage_matrix_ward)
        plt.title('Dendrogram AHC (Ward)')
        plt.xlabel('Indeks Data')
        plt.ylabel('Jarak')
        st.pyplot()

        st.write(f"Cophenetic Correlation Coefficient (CCC) untuk Dendrogram AHC (Ward): {ccc_ward:.4f}")
        st.write(f"Jumlah klaster optimal untuk metode linkage Ward: {len(set(labels_ward))}")

with c2:
    with st.expander("⬇ DENDROGRAM COMPLETE"):
        # Visualisasi Dendrogram untuk Complete
        plt.figure(figsize=(8, 6))
        dendrogram(linkage_matrix_complete)
        plt.title('Dendrogram AHC (Complete)')
        plt.xlabel('Indeks Data')
        plt.ylabel('Jarak')
        st.pyplot()

        st.write(f"Cophenetic Correlation Coefficient (CCC) untuk Dendrogram AHC (Complete): {ccc_complete:.4f}")
        st.write(f"Jumlah klaster optimal untuk metode linkage Complete: {len(set(labels_complete))}")

with c3:
    with st.expander("⬇ DENDROGRAM AVERAGE"):
        # Visualisasi Dendrogram untuk Average
        plt.figure(figsize=(8, 6))
        dendrogram(linkage_matrix_average)
        plt.title('Dendrogram AHC (Average)')
        plt.xlabel('Indeks Data')
        plt.ylabel('Jarak')
        st.pyplot()

        st.write(f"Cophenetic Correlation Coefficient (CCC) untuk Dendrogram AHC (Average): {ccc_average:.4f}")
        st.write(f"Jumlah klaster optimal untuk metode linkage Average: {len(set(labels_average))}")

with st.expander("⬇ LINKAGE INFORMATION"):
    st.write("Complete Linkage: Menggunakan jarak maksimum antara anggota klaster.")
    st.write("Single Linkage: Menggunakan jarak minimum antara anggota klaster.")
    st.write("Average Linkage: Menggunakan rata-rata jarak antara semua pasangan anggota klaster.")
    st.write("Ward's Method: Menggunakan kriteria minimisasi varians dalam klaster.")

# Map visualization
with st.expander("⬇ MAP VISUALIZATION"):
    st.subheader("Agglomerative Hierarchical Clustering (AHC) - Map Visualization")

    # Create a Folium map with markers
    m = folium.Map(location=[df['LATITUDE'].mean(), df['LONGITUDE'].mean()], zoom_start=10, width='100%')

    # Add a marker for each data point
    for i, row in df.iterrows():
        popup_content = f"""
        <div style='width:400px; height:300px;'>
            <ul class="list-group">
                <li class="list-group-item active" aria-current="true">
                    <h3 class="mb-0">Information of {row['KABUPATEN']}</h3>
                </li>
                <li class="list-group-item">Cluster: {row['Cluster_AHC']}</li>
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
            popup=folium.Popup(html=popup_content, max_width=400),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # Display the map
    folium_static(m)
