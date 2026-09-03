import time
import random
import asyncio
from playwright.async_api import async_playwright

# Rastgele gerçekçi tarayıcı kimlikleri
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

VIEWPORTS = [
    {"width": 1366, "height": 768},
    {"width": 1920, "height": 1080},
    {"width": 1536, "height": 864}
]

# ÖRNEK PROXY LİSTESİ (Kendi proxy'lerini buraya ekleyebilirsin: "ip:port")
PROXY_LIST = [
    # "http://proxy_ip_1:port",
]

async def bot_worker(bot_id, video_url, izleme_suresi):
    print(f"\n[Bot-{bot_id}/{toplam_hedef_global}] Oturum hazırlanıyor...")
    
    secilen_proxy = None
    if PROXY_LIST:
        secilen_proxy = {"server": random.choice(PROXY_LIST)}
        print(f"[Bot-{bot_id}] Proxy atandı: {secilen_proxy['server']}")

    async with async_playwright() as p:
        launch_options = {
            "headless": False,  # YouTube engellerini aşmak için görünür mod
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                "--disable-dev-shm-usage"
            ]
        }
        
        browser = await p.chromium.launch(**launch_options)
        
        context_options = {
            "user_agent": random.choice(USER_AGENTS),
            "viewport": random.choice(VIEWPORTS),
            "locale": "tr-TR"
        }
        if secilen_proxy:
            context_options["proxy"] = secilen_proxy

        context = await browser.new_context(**context_options)
        page = await context.new_page()
        
        try:
            print(f"[Bot-{bot_id}] Hedef URL yükleniyor...")
            await page.goto(video_url, timeout=60000)
            
            # Çerez onay pencerelerini atlat
            try:
                accept_button = page.locator("button:has-text('Kabul ediyorum'), button:has-text('Accept all'), button:has-text('Tümünü kabul et')")
                if await accept_button.count() > 0:
                    await accept_button.first.click()
                    print(f"[Bot-{bot_id}] Çerez onay penceresi geçildi.")
            except Exception:
                pass
            
            await asyncio.sleep(random.randint(3, 6))
            
            # Captcha / Doğrulama Duvarı Kontrolü
            page_content = await page.content()
            if "unusual traffic" in page_content.lower() or "robot" in page_content.lower():
                print(f"[Bot-{bot_id}] ⚠️ [DİKKAT] Bot doğrulama (Captcha/Engel) duvarına takıldı!")
                return

            # Oynatma Simülasyonu
            print(f"[Bot-{bot_id}] Video alanı tetikleniyor...")
            await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
            
            try:
                player = page.locator("video, .html5-video-player")
                if await player.count() > 0:
                    await player.first.click()
                    print(f"[Bot-{bot_id}] Video oynatıcıya tıklandı.")
            except Exception:
                await page.mouse.click(640, 360)
            
            print(f"[Bot-{bot_id}] Akış başlatıldı. {izleme_suresi} saniye izleniyor...")
            
            gecen_sure = 0
            while gecen_sure < izleme_suresi:
                bekleme_parcasi = random.randint(5, 10)
                await asyncio.sleep(bekleme_parcasi)
                gecen_sure += bekleme_parcasi
                await page.mouse.move(random.randint(200, 400), random.randint(200, 400))
            
            print(f"[Bot-{bot_id}] Görev başarıyla tamamlandı.")
            
        except Exception as e:
            print(f"[Bot-{bot_id}] İşlem sırasında hata oluştu: {e}")
            
        finally:
            await browser.close()

# Global değişken referansı için
toplam_hedef_global = 0

async def ana_yonetici(video_url, toplam_izlenme):
    global toplam_hedef_global
    toplam_hedef_global = toplam_izlenme
    
    # Bilgisayarının RAM/CPU sınırlarını korumak için eşzamanlı limit akıllıca belirlenir (Görünür modda en fazla 2 pencer aynı anda açılır)
    eszamanli_limit = 2 if toplam_izlenme >= 2 else 1  
    izleme_suresi = random.randint(25, 40)
    
    print("\n" + "=" * 55)
    print(f"🚀 DİNAMİK OPTİMİZE YOUTUBE OPERASYON MERKEZİ")
    print(f"🔗 Hedef Link: {video_url}")
    print(f"🎯 Hedeflenen Toplam İzlenme: {toplam_izlenme}")
    print(f"⚙️ Optimizasyon: Aynı anda maksimum {eszamanli_limit} bot çalışacak (Sistem koruması aktif)")
    print(f"⏱️ Her Bot Süresi: Rastgele {izleme_suresi} saniye")
    print("=" * 55 + "\n")
    
    semaphore = asyncio.Semaphore(eszamanli_limit)
    
    async def sinirli_bot_calistir(bot_id):
        async with semaphore:
            await bot_worker(bot_id, video_url, izleme_suresi)
            # Botlar arası doğal geçiş gecikmesi
            await asyncio.sleep(random.randint(4, 8))

    # Girilen izlenme sayısına göre görev kuyruğu oluşturulur
    gorevler = [sinirli_bot_calistir(i) for i in range(1, toplam_izlenme + 1)]
    await asyncio.gather(*gorevler)
    
    print("\n[✔] Belirlenen tüm izlenme hedefleri başarıyla tamamlandı!")

if __name__ == "__main__":
    print("--- YOUTUBE AKILLI İZLEME OTOMASYONU ---")
    hedef_link = input("Hedef YouTube Video Linkini Girin: ").strip()
    
    try:
        hedef_izlenme_input = int(input("İstediğiniz Toplam İzlenme Sayısı (Örn: 5): "))
        
        if hedef_link and hedef_izlenme_input > 0:
            asyncio.run(ana_yonetici(hedef_link, hedef_izlenme_input))
        else:
            print("[-] Geçerli bir link veya sayı girmediniz!")
            
    except ValueError:
        print("[-] Hatalı giriş! Lütfen izlenme sayısı için sayısal bir değer girin.")
