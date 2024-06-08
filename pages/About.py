import streamlit as st
import streamlit.components.v1 as components

# Set page configuration
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide") 


# Define a function for the tooltip (if needed)
def tooltip(image_url, text):
    return f'<img src="{image_url}" title="{text}" style="border: 1px solid blue; border-radius:4px; background-color:green; color: white; padding:2px;">'

# HTML content
html_content = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <style>
    iframe {{
        margin-bottom: 0px;
    }}
    html {{
        margin-top: 0px;
        margin-bottom: 0px;
        border: 1px solid #de3f53; padding:0px 4px;
        font-family: "Source Sans Pro", sans-serif;
        font-weight: 400;
        line-height: 1.6;
        color: rgb(49, 51, 63);
        background-color: rgb(255, 255, 255);
        text-size-adjust: 100%;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        -webkit-font-smoothing: auto;
    }}
    </style>

    <h2 style='color: #de3f53; margin-top:0px; border-bottom: solid 5px;'>What is PISA?</h2>
    
    <a href='https://www.oecd.org/pisa/' target='_blank'><b>PISA</b></a> stands for the "<b>Programme for International Student Assessment</b>".
    It is an international assessment conducted by the <a href='https://www.oecd.org' target='_blank'>Organisation for Economic Co-operation and Development (OECD)</a>
    to evaluate the knowledge and skills of in 
    <span style='color: blue;font-weight: bold;'>reading <i class="fa-solid fa-book-open-reader fa-beat"></i></span>, 
    <span style='color: red; font-weight: bold;'>mathematics <i class="fa-solid fa-calculator fa-fade"></i></span>, and 
    <span style='color: green;font-weight: bold;'>science <i class="fa-solid fa-flask-vial fa-shake"></i></span>. PISA assessments are conducted <b>every three years</b>, 
    and the results provide insights into the performance of education systems around the <span style='margin-top: 0px;margin-bottom: 10px;font-family: sans-serif; font-weight: bold; background: linear-gradient(to right, #ef5350, #f48fb1, #7e57c2, #2196f3, #26c6da, #43a047, #eeff41, #f9a825, #ff5722);-webkit-background-clip: text;-webkit-text-fill-color: transparent;'>world</span>.
"""

# Display the HTML content
st.markdown(html_content, unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:

    # Judul dan deskripsi
    st.title("Video Tutorial tentang K-Means dan AHC Clustering")
    st.markdown("""
    Berikut adalah beberapa video YouTube yang menjelaskan tentang K-Means dan Agglomerative Hierarchical Clustering (AHC). Anda dapat menonton video ini langsung di YouTube untuk mendapatkan pemahaman yang lebih baik tentang kedua metode tersebut.
    """)

    # Embed YouTube video
    video_url = "https://www.youtube.com/embed/BMzXuG1p3lQ?t=887s"
    video_html = f"""
        <div style="display: flex; justify-content: center;">
            <iframe width="1000" height="450" src="{video_url}" 
            frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
        </div>
    """
    components.html(video_html, height=450)

    with st.expander("**Tentang Analisis Klaster AHC dan K-Means pada Data BPS Kabupaten Purwakarta**"):
        st.markdown('''
        **Pendahuluan: 📊**
        Bagian ini membahas penerapan Analisis Klaster Agglomerative Hierarchical Clustering (AHC) dan K-Means pada data demografis yang diperoleh dari Badan Pusat Statistik (BPS) Kabupaten Purwakarta. Metode klaster ini memberikan wawasan yang berharga untuk memahami pola dan kelompok dalam populasi, memungkinkan pengambilan keputusan yang terinformasi dan intervensi yang lebih terarah.

        **Pendekatan Utama: 🌐**

        1. **Agglomerative Hierarchical Clustering (AHC):**
            - AHC adalah metode klaster hierarkis yang secara iteratif menggabungkan titik data yang mirip ke dalam klaster.
            - Analisis ini bertujuan untuk mengungkap struktur alami dalam data demografis, mengidentifikasi kelompok wilayah dengan karakteristik populasi yang serupa.

        2. **K-Means Clustering:**
            - K-Means membagi data menjadi 'k' klaster berdasarkan kemiripan.
            - Dengan menerapkan K-Means pada data BPS Kabupaten Purwakarta, kita bertujuan untuk menemukan segmen populasi yang berbeda dan fitur-fitur yang mendefinisikannya.

        **Sumber Data: 📈**

        Data demografis yang digunakan dalam analisis ini berasal dari Badan Pusat Statistik (BPS) Kabupaten Purwakarta. Data ini mencakup indikator-indikator utama selama beberapa tahun, memberikan pandangan komprehensif tentang lanskap populasi.

        **Tujuan: 🎯**

        Tujuan utama adalah menggunakan teknik klaster untuk mengkategorikan wilayah-wilayah dalam Kabupaten Purwakarta berdasarkan pola demografis. Analisis ini dapat membantu pembuat kebijakan, peneliti, dan otoritas lokal dalam memahami keragaman dalam wilayah tersebut dan merancang strategi pembangunan secara tepat.

        **Manfaat Analisis Klaster: 📚**

        - **Pola yang Memberi Wawasan:** Mengungkap pola dan struktur bawaan dalam populasi Kabupaten Purwakarta, memungkinkan pihak terkait untuk membuat kebijakan yang lebih terfokus.
        - **Identifikasi Kelompok Demografis:** Memahami kelompok penduduk dengan karakteristik serupa.
        - **Perencanaan Pembangunan:** Menyediakan dasar untuk perencanaan pembangunan berdasarkan kebutuhan dan profil populasi.
        - **Pemahaman Keanekaragaman:** Analisis membantu menggambarkan keanekaragaman dalam konteks demografis.

        **Pendekatan Metodologis: 📊**

        Metode AHC digunakan untuk mengeksplorasi struktur hierarkis dalam data demografis, sementara K-Means memberikan pemahaman tentang kelompok populasi yang lebih terdefinisi. Kombinasi kedua metode ini memberikan pandangan holistik tentang distribusi dan hubungan antarwilayah.

        **Kesimpulan: 🌟**

        Analisis klaster dengan AHC dan K-Means diharapkan dapat memberikan gambaran yang lebih dalam tentang populasi Kabupaten Purwakarta. Hasilnya dapat digunakan sebagai dasar untuk kebijakan pembangunan yang lebih efektif, memastikan bahwa sumber daya dialokasikan dengan bijak sesuai dengan kebutuhan unik setiap wilayah.
        ''')
        
    st.info('''
        Hasil analisis klaster menggunakan metode Agglomerative Hierarchical Clustering (AHC) dan K-Means pada data demografis BPS Kabupaten Purwakarta dapat memberikan wawasan yang berharga untuk:

        * **Mengidentifikasi** pola dan kelompok dalam populasi.
        * **Mendukung** pengambilan keputusan yang terinformasi.
        * **Mengarahkan** intervensi dengan lebih tepat.

        Analisis ini dapat menjadi **alat penting** bagi **pembuat kebijakan**, **peneliti**, dan **otoritas lokal** dalam:

        * **Memahami** keragaman dalam wilayah tersebut.
        * **Merancang** strategi pembangunan yang sesuai.

        Dengan menggunakan teknik klaster seperti AHC dan K-Means, kita dapat mengeksplorasi struktur alami dalam data demografis, mengidentifikasi kelompok wilayah dengan karakteristik populasi yang serupa, dan menemukan segmen populasi yang berbeda.

        Analisis ini memberikan landasan untuk **menginformasikan** kebijakan pembangunan wilayah dan **mengeksplorasi** faktor-faktor yang dapat mempengaruhi pola demografis di Kabupaten Purwakarta.
        ''', icon="🧐")

with c2:

    # Judul dan deskripsi
    st.title("Video Tutorial tentang K-Means dan AHC Clustering")
    st.markdown("""
    Berikut adalah beberapa video YouTube yang menjelaskan tentang K-Means dan Agglomerative Hierarchical Clustering (AHC). Anda dapat menonton video ini langsung di YouTube untuk mendapatkan pemahaman yang lebih baik tentang kedua metode tersebut.
    """)

    # Embed YouTube video
    video_url = "https://www.youtube.com/embed/s8K0lO9OFOA?start=1067"
    video_html = f"""
        <div style="display: flex; justify-content: center;">
            <iframe width="1000" height="450" src="{video_url}" 
            frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
        </div>
    """
    components.html(video_html, height=450)

    with st.expander("**Tentang Analisis Klaster AHC dan K-Means pada Data BPS Kabupaten Purwakarta**"):
        st.markdown('''
        **Pendahuluan: 📊**
        Bagian ini membahas penerapan Analisis Klaster Agglomerative Hierarchical Clustering (AHC) dan K-Means pada data demografis yang diperoleh dari Badan Pusat Statistik (BPS) Kabupaten Purwakarta. Metode klaster ini memberikan wawasan yang berharga untuk memahami pola dan kelompok dalam populasi, memungkinkan pengambilan keputusan yang terinformasi dan intervensi yang lebih terarah.

        **Pendekatan Utama: 🌐**

        1. **Agglomerative Hierarchical Clustering (AHC):**
            - AHC adalah metode klaster hierarkis yang secara iteratif menggabungkan titik data yang mirip ke dalam klaster.
            - Analisis ini bertujuan untuk mengungkap struktur alami dalam data demografis, mengidentifikasi kelompok wilayah dengan karakteristik populasi yang serupa.

        2. **K-Means Clustering:**
            - K-Means membagi data menjadi 'k' klaster berdasarkan kemiripan.
            - Dengan menerapkan K-Means pada data BPS Kabupaten Purwakarta, kita bertujuan untuk menemukan segmen populasi yang berbeda dan fitur-fitur yang mendefinisikannya.

        **Sumber Data: 📈**

        Data demografis yang digunakan dalam analisis ini berasal dari Badan Pusat Statistik (BPS) Kabupaten Purwakarta. Data ini mencakup indikator-indikator utama selama beberapa tahun, memberikan pandangan komprehensif tentang lanskap populasi.

        **Tujuan: 🎯**

        Tujuan utama adalah menggunakan teknik klaster untuk mengkategorikan wilayah-wilayah dalam Kabupaten Purwakarta berdasarkan pola demografis. Analisis ini dapat membantu pembuat kebijakan, peneliti, dan otoritas lokal dalam memahami keragaman dalam wilayah tersebut dan merancang strategi pembangunan secara tepat.

        **Manfaat Analisis Klaster: 📚**

        - **Pola yang Memberi Wawasan:** Mengungkap pola dan struktur bawaan dalam populasi Kabupaten Purwakarta, memungkinkan pihak terkait untuk membuat kebijakan yang lebih terfokus.
        - **Identifikasi Kelompok Demografis:** Memahami kelompok penduduk dengan karakteristik serupa.
        - **Perencanaan Pembangunan:** Menyediakan dasar untuk perencanaan pembangunan berdasarkan kebutuhan dan profil populasi.
        - **Pemahaman Keanekaragaman:** Analisis membantu menggambarkan keanekaragaman dalam konteks demografis.

        **Pendekatan Metodologis: 📊**

        Metode AHC digunakan untuk mengeksplorasi struktur hierarkis dalam data demografis, sementara K-Means memberikan pemahaman tentang kelompok populasi yang lebih terdefinisi. Kombinasi kedua metode ini memberikan pandangan holistik tentang distribusi dan hubungan antarwilayah.

        **Kesimpulan: 🌟**

        Analisis klaster dengan AHC dan K-Means diharapkan dapat memberikan gambaran yang lebih dalam tentang populasi Kabupaten Purwakarta. Hasilnya dapat digunakan sebagai dasar untuk kebijakan pembangunan yang lebih efektif, memastikan bahwa sumber daya dialokasikan dengan bijak sesuai dengan kebutuhan unik setiap wilayah.
        ''')
        
    st.info('''
        Hasil analisis klaster menggunakan metode Agglomerative Hierarchical Clustering (AHC) dan K-Means pada data demografis BPS Kabupaten Purwakarta dapat memberikan wawasan yang berharga untuk:

        * **Mengidentifikasi** pola dan kelompok dalam populasi.
        * **Mendukung** pengambilan keputusan yang terinformasi.
        * **Mengarahkan** intervensi dengan lebih tepat.

        Analisis ini dapat menjadi **alat penting** bagi **pembuat kebijakan**, **peneliti**, dan **otoritas lokal** dalam:

        * **Memahami** keragaman dalam wilayah tersebut.
        * **Merancang** strategi pembangunan yang sesuai.

        Dengan menggunakan teknik klaster seperti AHC dan K-Means, kita dapat mengeksplorasi struktur alami dalam data demografis, mengidentifikasi kelompok wilayah dengan karakteristik populasi yang serupa, dan menemukan segmen populasi yang berbeda.

        Analisis ini memberikan landasan untuk **menginformasikan** kebijakan pembangunan wilayah dan **mengeksplorasi** faktor-faktor yang dapat mempengaruhi pola demografis di Kabupaten Purwakarta.
        ''', icon="🧐")

