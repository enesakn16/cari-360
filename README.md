# Cari 360 — Offline Finance & Receivables Demo

Cari 360, işletmelerin **cari hesap bakiyelerini, açık hareketlerini ve vade riskini tek ekranda takip etmesini** hedefleyen masaüstü finans/operasyon uygulamasının güvenli public demosudur.

Bu repository yalnızca sentetik veri kullanır. Gerçek şirket verisi, üretim veritabanı bağlantısı, API anahtarı veya gizli yapılandırma içermez.

## Ne işe yarar?

- Cari hesap ve bakiye görünümü
- Açık hareket ve vade takibi
- Gecikmiş / bugün vadeli / yaklaşan alacakların yaşlandırılması
- Deterministik offline aging report
- Finans operasyonlarını hızlı incelemek için masaüstü dashboard

**Kim için?** KOBİ finans ekipleri, muhasebe/operasyon kullanıcıları ve cari risk takibini masaüstünden yapmak isteyen işletmeler.

## Hızlı başlangıç

Python **3.12 veya 3.13** gerekir.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Windows'ta `run_demo.bat` dosyası da kullanılabilir.

## Öne çıkan özellikler

### Offline cari yaşlandırma raporu

Sentetik açık hareketleri vade gününe göre sabit yaşlandırma aralıklarında özetlemek için:

```bash
python aging_report.py
```

Rapor şu grupları ayrı gösterir:

- gecikmiş 1–7 gün
- gecikmiş 8–30 gün
- gecikmiş 31–60 gün
- gecikmiş 61+ gün
- bugün vadeli belgeler
- yaklaşan vadeler

Tamamlanmış veya vadesiz hareketler hesaba katılmaz. Para hesaplamalarında `Decimal` kullanılır.

## Test ve CI

```bash
python -m pip install pytest
pytest -q
```

GitHub Actions; testleri ve public demo için güvenlik kontrollerini çalıştırır. Son doğrulanmış `main` workflow'u başarıyla tamamlanmıştır.

## Güvenlik modeli

Public demo bilinçli olarak üretim sisteminden izole edilmiştir:

- Supabase, PostgreSQL veya başka bir uzak veritabanı bağlantısı yoktur.
- URL, token, API anahtarı, `.env` veya üretim ayarı okunmaz.
- Gerçek şube / müşteri / şirket isimleri bulunmaz.
- Ağ kütüphanesi kullanılmaz.
- Kayıt ekleme, silme, güncelleme, import veya export yoktur.
- Cari, bakiye, vade ve satış değerleri `demo_data.py` içindeki sentetik örneklerden üretilir.
- CI, yasaklı bağlantı kütüphanelerini ve gizli bilgi işaretlerini tarar.

## Repository yapısı

```text
main.py            # PyQt masaüstü demo arayüzü
aging_report.py    # Deterministik vade/aging hesaplama katmanı
demo_data.py       # Sentetik demo verisi
tests/             # Headless ve domain testleri
.github/workflows/ # CI ve güvenlik kontrolleri
```

## Kapsam

Bu repository üretim uygulamasının veritabanı katmanını, migration dosyalarını, güncelleme altyapısını veya şirket verilerini içermez. Amaç, ürünün finans operasyonu mantığını güvenli ve tekrar üretilebilir bir public demo üzerinden göstermek.
