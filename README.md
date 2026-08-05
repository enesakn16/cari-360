# Cari 360 — Offline Demo

Cari 360'ın public ve güvenli tanıtım sürümüdür. Uygulama yalnız sentetik veriler kullanır ve gerçek sisteme bağlanabilecek bir veri tabanı istemcisi içermez.

## Güvenlik mimarisi

- Supabase, PostgreSQL veya başka bir uzak veri tabanı bağlantısı yoktur.
- URL, token, API anahtarı, `.env` veya üretim ayarı okunmaz.
- Şube seçimi ve gerçek şube isimleri bulunmaz.
- Ağ kütüphanesi kullanılmaz.
- Kayıt ekleme, silme, güncelleme, içe aktarma ve dışa aktarma yoktur.
- Bütün cari, bakiye, vade ve satış değerleri `demo_data.py` içinde üretilen sentetik örneklerdir.
- CI testi yasaklı bağlantı kütüphanelerini ve gizli bilgi işaretlerini tarar.

## Çalıştırma

Python 3.12 veya 3.13 gerekir.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Windows'ta doğrudan `run_demo.bat` dosyası da kullanılabilir.

## Offline cari yaşlandırma raporu

Sentetik açık hareketleri vade gününe göre sabit yaşlandırma aralıklarında özetlemek için:

```bash
python aging_report.py
```

Rapor; gecikmiş 1-7, 8-30, 31-60 ve 61+ gün gruplarını, bugün vadeli belgeleri ve yaklaşan vade aralıklarını ayrı gösterir. Tamamlanmış veya vadesiz hareketler hesaba katılmaz. Hesaplamalar `Decimal` ile yapılır; ağ erişimi, veri tabanı bağlantısı veya dosya dışa aktarımı kullanılmaz.

## Test

```bash
python -m pip install pytest
pytest -q
```

Bu repo üretim uygulamasının veritabanı katmanını, migration dosyalarını, güncelleme altyapısını veya şirket verilerini içermez.
