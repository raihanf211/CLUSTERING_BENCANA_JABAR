import streamlit as st
import streamlit.components.v1 as components

# Set page configuration
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

# Fungsi untuk tooltip (jika diperlukan)
def tooltip(image_url, text):
    return f'<img src="{image_url}" title="{text}" style="border: 1px solid blue; border-radius: 4px; background-color: green; color: white; padding: 2px;">'

# Konten HTML yang diperbarui
html_content = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <style>
    iframe {{
        margin-bottom: 0px;
    }}
    html {{
        margin-top: 0px;
        margin-bottom: 0px;
        border: 1px solid #de3f53;
        padding: 0px 4px;
        font-family: "Source Sans Pro", sans-serif;
        font-weight: 400;
        line-height: 1.6;
        color: rgb(49, 51, 63);
        background-color: rgb(255, 255, 255);
        text-size-adjust: 100%;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        -webkit-font-smoothing: auto;
    }}
    h2 {{
        color: #de3f53;
        margin-top: 0px;
        border-bottom: solid 5px;
        text-align: center;
    }}
    .highlight-text {{
        font-weight: bold;
    }}
    p {{
        text-align: justify;
    }}
    </style>

    <h2>Pengelompokan Daerah Rawan Bencana Tanah Longsor Kabupaten/Kota di Provinsi Jawa Barat</h2>
    
    <p>Tujuan dari penelitian ini adalah untuk mengelompokkan (clustering) dan mengimplementasikan tampilan antarmuka dengan visualisasi pemetaan daerah rawan bencana tanah longsor di Provinsi Jawa Barat.</p> 
    <p>Sehingga penelitian ini dapat menjadi referensi dalam mencapai perencanaan mitigasi optimal, pengembangan kebijakan efektif tingkat provinsi, infrastruktur, dan upaya peningkatan kesiapsiagaan, kecepatan, serta ketepatan penanggulangan antisipasi bencana di Provinsi Jawa Barat.</p>
"""

# Tampilkan konten HTML
st.markdown(html_content, unsafe_allow_html=True)

# Adding a divider line
st.divider()

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
        Berikut adalah video YouTube yang menjelaskan tentang teknik analisis clustering menggunakan algoritma k-means.
    """)

    # Embed YouTube video
    video_url_kmeans = "https://www.youtube.com/embed/BMzXuG1p3lQ?t=887s"
    video_html_kmeans = f"""
        <div style="display: flex; justify-content: center;">
            <iframe width="1000" height="450" src="{video_url_kmeans}" 
            frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
        </div>
    """
    st.markdown(video_html_kmeans, unsafe_allow_html=True)

with c2:
    st.markdown("""
    Berikut adalah video YouTube yang menjelaskan tentang teknik analisis clustering menggunakan algoritma AHC (Agglomerative Hierarchical Clustering).
    """)

    # Embed YouTube video
    video_url_ahc = "https://www.youtube.com/embed/s8K0lO9OFOA?start=1067"
    video_html_ahc = f"""
        <div style="display: flex; justify-content: center;">
            <iframe width="1000" height="450" src="{video_url_ahc}" 
            frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
        </div>
    """
    components.html(video_html_ahc, height=450)

# Ekspander untuk informasi tentang clustering bencana longsor
with st.expander("**Tentang Analisis Klaster Bencana Tanah Longsor di Kabupaten dan Kota di Provinsi Jawa Barat**"):
    st.markdown('''
    **Pendahuluan: 📊**
    Dalam menghadapi bencana alam, kesiapsiagaan menjadi kunci utama dalam meminimalisir dampak yang ditimbulkan. Masyarakat khususnya di Jawa Barat sebagai elemen terdepan harus memiliki kemampuan untuk bersiap dan bertindak saat bencana terjadi. Kecepatan dan ketepatan dalam penanggulangan bencana sangatlah krusial untuk menjamin keberhasilan prosesnya. Untuk mengurangi semua kerentanan fisik dan sosial ekonomi, kesiapsiagaan bencana menjadi pendekatan penting.

    **Pendekatan Utama: 🌐**

    **Metode Klaster:**
    - Metode clustering digunakan untuk mengelompokkan daerah rawan bencana di kabupaten dan kota Provinsi Jawa Barat, berdasarkan atribut:
      - Jumlah kejadian bencana longsor
      - Jiwa terdampak
      - Jiwa meninggal
      - Rusak terdampak
      - Rusak ringan
      - Rusak sedang
      - Rusak berat
      - Tertimbun

    **Sumber Data: 📈**
    - Data yang digunakan dalam analisis ini mencakup data jumlah menurut Kabupaten/Kota yang mengalami kejadian bencana tanah longsor di Provinsi Jawa Barat.
    - Bersumber dari website BARATA yang dikelola oleh Badan Penanggulangan Bencana Daerah Provinsi Jawa Barat

    **Tujuan: 🎯**
    - Tujuan utama adalah mengetahui pemetaan dan pengelompokan daerah rawan bencana longsor di kabupaten dan kota di Provinsi Jawa Barat. 
    - Metode ini memberikan wawasan yang berharga untuk mencapai perencanaan mitigasi optimal dan pengembangan kebijakan efektif tingkat provinsi, infrastruktur, serta upaya peningkatan kesiapsiagaan, kecepatan, dan ketepatan penanggulangan antisipasi bencana di Provinsi Jawa Barat.
    ''')

