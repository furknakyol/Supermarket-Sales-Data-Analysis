# Supermarket Sales Data Analysis (BI Dashboard Projesi)

Bu repo, süpermarket satış verileri üzerinde veri hazırlama (ETL), keşifsel veri analizi (EDA) ve bir BI dashboard (prototip) oluşturma sürecini içerir. Amaç: tekrarlanabilir veri pipeline'ı oluşturmak ve interaktif dashboard ile KPI/insight sunmak.

İçerik
- data/ : Veri dosyaları (büyük dosyalar repoya konmamalı; örnek sample koyulabilir)
- notebooks/ : EDA ve prototip çalışmalar için Jupyter notebook'lar
- src/ : ETL ve yardımcı python modülleri
- scripts/ : veri indirme / sample oluşturma script'leri
- dashboards/ : seçilen BI / prototip uygulama dosyaları (Dash/Streamlit veya Power BI export)
- .github/workflows/ : opsiyonel CI konfigürasyonları

Hızlı başlangıç
1. Klonla:
   git clone https://github.com/furknakyol/Supermarket-Sales-Data-Analysis.git
   cd Supermarket-Sales-Data-Analysis

2. Branch (project-setup) veya main:
   git checkout project-setup  # (eğer branch varsa) veya yeni branch oluştur: git checkout -b project-setup

3. Sanal ortam:
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows

4. Bağımlılıklar:
   pip install -r requirements.txt

5. Veri örneği oluşturma (varsa tam CSV'den sample al):
   python scripts/get_data.py --source data/sales.csv --out data/sample_sales.csv --sample 1000

6. ETL çalıştırma (örnek):
   python -c "from src.etl import load_csv, clean_sales; df=load_csv('data/sample_sales.csv'); df=clean_sales(df); print(df.head())"

Önerilen KPI'lar (dashboard için)
- Toplam satış (perioda göre; günlük/aylık/yıllık)
- Ortalama sipariş değeri (AOV)
- Satış başına adet / ort. ürün sayısı
- En çok satan ürünler / kategori kırılımları
- Bölge / mağaza bazlı karşılaştırmalar
- Zaman içindeki trendler ve sezonluk (seasonality)
- İade oranı / net satışlar (veri varsa)

Veri politikası
- Büyük veri dosyalarını repoya eklemeyin. data/ içine örnek (sample) CSV koyun.
- Hassas müşteri verisi (PII) kesinlikle repoda olmamalıdır.

Katkı
- Issues aç ve feature branch ile PR gönder.
- Kod stil: black + flake8

Lisans
- Bu proje için MIT lisansı kullanılmıştır; detaylar LICENSE dosyasında.