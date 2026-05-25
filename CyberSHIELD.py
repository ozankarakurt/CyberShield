import sys
import time
import hashlib
import math
import os
import urllib.request
import urllib.error
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QPushButton, QStackedWidget, QLabel, 
                             QFrame, QLineEdit, QTextEdit, QProgressBar, QFileDialog, QComboBox, QListWidget, QSplashScreen, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

# =====================================================================
# 1. LOCALIZATION SYSTEM (Dil Paketleri Veri Yapısı)
# =====================================================================

LANGUAGES = {
    "EN": {
        "app_title": "🛡️ CyberShield",
        "menu_dashboard": "  Dashboard",
        "menu_url": "  URL Scanner",
        "menu_pwd": "  Password Analyzer",
        "menu_file": "  File Analyzer",
        "menu_reports": "  Reports",
        "menu_settings": "  Settings",
        "menu_about": "  Alerts",
        
        "dash_title": "CYBERSHIELD DASHBOARD",
        "dash_status": "🛡️ SYSTEM STATUS: SECURE",
        "dash_scans": "TOTAL SCANS",
        "dash_risk": "RISK INDEX",
        "dash_events": "Recent Security Events:",
        "dash_log1": "[INFO] Core engine initialized successfully.",
        "dash_log2": "[SUCCESS] Firewall synchronization active.",
        "dash_log3": "[MONITOR] Zero threads hanging. Memory heap clean.",
        
        "url_title": "URL VULNERABILITY SCANNER",
        "url_placeholder": "Enter target domain or deep URL (e.g., https://example.com)",
        "url_btn": "Scan URL",
        "url_console": "Console Output Matrix:",
        "url_err_empty": "[-] Error: Input field is empty. Please enter a URL.",
        "url_scanning": "[*] SEC_ENGINE: Initiating handshake with {}\n[*] VT_API: Querying database threat matrix...\n[~] Network routing check underway. Please standby...",
        
        "pwd_title": "PASSWORD ENTROPY ANALYZER",
        "pwd_placeholder": "Input raw string password vector...",
        "pwd_entropy": "Calculated Entropy : {} bits",
        "pwd_crack": "Estimated Crack Time: {}",
        "pwd_suggest": "Remediation Strategy : {}",
        "pwd_time_instant": "Instantaneous",
        "pwd_time_low": "Milliseconds / Brute-force vulnerable",
        "pwd_time_med": "2 Months to 4 Years",
        "pwd_time_high": "Centuries (Cryptographically Resilient)",
        "pwd_sug_low": "Inject non-alphanumeric and uppercase variables.",
        "pwd_sug_med": "Increase length past 12 characters.",
        "pwd_sug_high": "Excellent structural integrity.",
        "pwd_sug_dict": "⚠️ CRITICAL: Password found in common vulnerability dictionary!",
        
        "file_title": "STATIC MALWARE & FILE ANALYZER",
        "file_btn": "📁 Load Binary / Select Local Target File",
        "file_reading": "[*] FILE_IO: Streaming byte array from memory map: {}\n[*] CRYPTO: Calculating cryptographic hash sequences...\n[~] VT_INTEL: Querying global Antivirus engines via VirusTotal API...",
        "file_err": "[-] Critical IO Error: {}",
        
        "set_title": "CYBERSHIELD SYSTEM CONFIGURATION",
        "set_lang_lbl": "Select Application Language / Dil Seçimi:",
        "set_theme_lbl": "Select Cockpit Interface Theme / Tema Seçimi:",
        "theme_cyber": "Futuristic Cyber (Default)",
        "theme_hacker": "Hacker Mode (Matrix Green)",
        
        "rep_title": "HISTORICAL SCAN REPORTS",
        "rep_list_lbl": "Saved Reports Log:",
        "rep_details_lbl": "Report Document Details:",
        "rep_empty": "No scan reports found in 'reports/' directory.",
        "rep_load_err": "Could not read report file.",
        "rep_download_btn": "📥 Download Report",
        "rep_delete_btn": "🗑️ Delete Report",
        "rep_clear_btn": "💥 Clear All History",
        "rep_dl_success_title": "Success",
        "rep_dl_success_msg": "Report successfully saved to:\n{}",
        "rep_dl_err_title": "Error",
        "rep_dl_err_no_select": "Please select a valid report from the log.",
        "rep_dl_err_fail": "Failed to write document to specified location.",
        "rep_del_confirm_title": "Confirm Delete",
        "rep_del_confirm_msg": "Are you sure you want to permanently delete this report file?",
        "rep_clear_confirm_title": "Confirm Wipeout",
        "rep_clear_confirm_msg": "WARNING: This will permanently purge ALL stored reports. Proceed?",
        
        "about_title": "MALWARE DETECTION & ALERTS THEORY",
        "about_content": "📖 WHY DID MY TROJAN SHOW 0/0 DETECTIONS?\n\nWhen analyzing local, custom-made, or newly compiled malware vectors, threat intelligence engines frequently return a 0/0 (Clean/Not Found) classification. Understanding this behavior requires breaking down malware analysis into its two main foundational pillars:\n\n1. STATIC ANALYSIS (Signature Matching)\n- Method: The analyzer extracts the cryptographic fingerprint (SHA-256 / MD5 hash) of the binary file and cross-references it with global databases like VirusTotal.\n- Limitation: If a Trojan is compiled locally and has never been captured in the wild, no Antivirus vendor has its signature recorded. It acts as a Zero-Day threat.\n- Result: Global engines will report 0/0 detections because the file's hash is completely unique and unknown to the world.\n\n2. DYNAMIC ANALYSIS (Heuristic & Behavioral Tracking)\n- Method: Local Endpoint Detection & Response (EDR) agents or Antiviruses deploy sandboxing environments. They actively monitor process execution, API hooks, and memory injections.\n- Indicators of Compromise (IoC): System behaviors such as executing Windows API sequences (e.g., VirtualAlloc, WriteProcessMemory), creating persistence in the Registry, or opening a raw TCP socket connection (Reverse Shell) immediately trigger heuristic flags.\n- Result: Even if a Trojan is mathematically invisible to static database checks (0/0), runtime behavior analysis will instantly neutralize it on a local endpoint.\n\n⚠️ DEFENDER NOTE FOR RED TEAMERS:\nUploading a custom payload directly to VirusTotal exposes the source code and signature template to security vendors. Within 24-72 hours, signature updates propagate globally, converting your FUD (Fully Undetectable) project into a universally flagged signature."
    },
    "TR": {
        "app_title": "🛡️ CyberShield",
        "menu_dashboard": "  Panel",
        "menu_url": "  URL Tarayıcı",
        "menu_pwd": "  Şifre Analizi",
        "menu_file": "  Dosya Analizi",
        "menu_reports": "  Raporlar",
        "menu_settings": "  Ayarlar",
        "menu_about": "  Uyarılar",
        
        "dash_title": "CYBERSHIELD KONTROL PANELİ",
        "dash_status": "🛡️ SİSTEM DURUMU: GÜVENLİ",
        "dash_scans": "TOPLAM TARAMA",
        "dash_risk": "RISK ENDEKSİ",
        "dash_events": "Son Güvenlik Olayları:",
        "dash_log1": "[BİLGİ] Çekirdek motor başarıyla başlatıldı.",
        "dash_log2": "[BAŞARILI] Güvenlik duvarı senkronizasyonu aktif.",
        "dash_log3": "[İZLEME] Askıda iş parçacığı yok. Bellek yığını temiz.",
        
        "url_title": "URL ZAFİYET TARAYICI",
        "url_placeholder": "Hedef alan adını veya URL'yi girin (örn: https://example.com)",
        "url_btn": "URL'yi Tara",
        "url_console": "Konsol Çıktı Matrisi:",
        "url_err_empty": "[-] Hata: Giriş alanı boş. Lütfen bir URL yazın.",
        "url_scanning": "[*] GÜV_MOTORU: {} ile el sakinşma başlatılıyor...\n[*] VT_API: Veritabanı tehdit matrisi sorgulanıyor...\n[~] Ağ yönlendirme kontrolü yapılıyor. Lütfen bekleyin...",
        
        "pwd_title": "ŞİFRE ENTROPİ ANALİZİ",
        "pwd_placeholder": "Analiz edilecek şifreyi giriniz...",
        "pwd_entropy": "Hesaplanan Entropi : {} bit",
        "pwd_crack": "Tahmini Kırılma Süresi: {}",
        "pwd_suggest": "İyileştirme Stratejisi : {}",
        "pwd_time_instant": "Anında",
        "pwd_time_low": "Milisaniyeler / Brute-force'a karşı zayıf",
        "pwd_time_med": "2 Ay ile 4 Yıl Arası",
        "pwd_time_high": "Yüzyıllar (Kriptografik Olarak Dayanıklı)",
        "pwd_sug_low": "Alfanumerik olmayan (özel karakter) ve büyük harf ekleyin.",
        "pwd_sug_med": "Şifre uzunluğunu 12 karakterin üzerine çıkarın.",
        "pwd_sug_high": "Mükemmel yapısal bütünlük.",
        "pwd_sug_dict": "⚠️ KRİTİK: Şifre yaygın zafiyet sözlüğünde bulundu!",
        
        "file_title": "STATİK ZARARLI YAZILIM & DOSYA ANALİZİ",
        "file_btn": "📁 İkili Dosya Yükle / Yerel Hedef Dosyayı Seç",
        "file_reading": "[*] DOSYA_IO: Bellek haritasından bayt dizisi akıtılıyor: {}\n[*] KRİPTO: Kriptografik hash dizileri hesaplanıyor...\n[~] VT_ISTİHBARAT: VirusTotal API üzerinden küresel Antivirüs motorları sorgulanıyor...",
        "file_err": "[-] Kritik Dosya Okuma Hatası: {}",
        
        "set_title": "CYBERSHIELD SİSTEM YAPILANDIRMASI",
        "set_lang_lbl": "Uygulama Dilini Seçin / Select Application Language:",
        "set_theme_lbl": "Kokpit Arayüz Temasını Seçin / Select Interface Theme:",
        "theme_cyber": "Fütüristik Siber Mavi (Varsayılan)",
        "theme_hacker": "Hacker Modu (Matrix Yeşili)",
        
        "rep_title": "GEÇMİŞ TARAMA RAPORLARI",
        "rep_list_lbl": "Kaydedilen Rapor Günlüğü:",
        "rep_details_lbl": "Rapor Belgesi Detayları:",
        "rep_empty": "'reports/' dizininde kayıtlı tarama raporu bulunamadı.",
        "rep_load_err": "Rapor dosyası okunamadı.",
        "rep_download_btn": "📥 Raporu İndir",
        "rep_delete_btn": "🗑️ Raporu Sil",
        "rep_clear_btn": "💥 Tüm Geçmişi Temizle",
        "rep_dl_success_title": "Başarılı",
        "rep_dl_success_msg": "Rapor dosyası başarıyla kaydedildi:\n{}",
        "rep_dl_err_title": "Hata",
        "rep_dl_err_no_select": "Lütfen listeden geçerli bir rapor seçin.",
        "rep_dl_err_fail": "Belge belirtilen konuma yazılırken hata oluştu.",
        "rep_del_confirm_title": "Silme Onayı",
        "rep_del_confirm_msg": "Bu rapor dosyasını kalıcı olarak silmek istediğinize emin misiniz?",
        "rep_clear_confirm_title": "Tüm Geçmişi Temizle",
        "rep_clear_confirm_msg": "DİKKAT: Bu işlem kayıtlı TÜM raporları diskten kalıcı olarak silecektir. Devam edilsin mi?",
        
        "about_title": "ZARARLI TESPİTİ & UYARI TEORİSİ",
        "about_content": "📖 YAZDIĞIM TROJAN NEDEN 0/0 (TEMİZ) OLARAK GÖRÜNÜYOR?\n\nKendi geliştirdiğin, yerel olarak derlediğin veya üzerinde oynadığın zararlı yazılımları test ederken sistemin tehdit bulamaması siber güvenliğin en temel kurallarıyla ilgilidir. Zararlı yazılım analizi iki ana başlıkta incelenir:\n\n1. STATİK ANALİZ (İmza Tabanlı Kontrol)\n- Çalışma Mantığı: Sistem, analiz edilmek istenen dosyanın benzersiz parmak izini (SHA-256 hash kodu) çıkarır ve bunu VirusTotal gibi küresel kütüphanelerde aratır.\n- Sınırları: Eğer bir Trojan'ı kendi bilgisayarında yeni yazdıysan, bu imza dünyadaki hiçbir antivirüs şirketi tarafından henüz görülmemiştir (Zero-Day / Sıfırıncı Gün).\n- Sonucu: Veritabanında eşleşen kayıt olmadığı için sistem haklı olarak 0/0 (Bilinmeyen/Temiz) sonucunu döner.\n\n2. DİNAMİK ANALİZ (Sezgisel & Davranışsal Takip)\n- Çalışma Mantığı: Bilgisayardaki yerel antivirüs veya EDR yazılımları, dosyanın koduna bakmak yerine onun çalışma anındaki davranışlarını izler.\n- Tehdit Göstergeleri (IoC): Dosyanın belleğe sızmaya çalışması (VirtualAlloc, WriteProcessMemory API çağrıları), arka planda dış dünyaya gizli bağlantı açması (Reverse Shell) gibi eylemler sezgisel motorlarca yakalanır.\n- Sonuç: Statik sorguda 0/0 çıkan bir virüs, bilgisayarda çalıştırıldığı an davranış analizine takılarak anında imha edilir.\n\n⚠️ RED TEAM VE GÜVENLİK UYARISI:\nGeliştirdiğin bir backdoor veya trojanı direkt olarak VirusTotal'e web sitesinden yüklersen, bu dosya tüm antivirüs üreticilerine analiz için gönderilir. Maksimum 1-3 gün içinde dosyan 'patlar' ve FUD (antivirüslere yakalanmama) özelliğini tamamen kaybeder."
    }
}

current_lang = "EN"
current_theme = "CYBER" 

def tr(key):
    return LANGUAGES[current_lang].get(key, key)

if not os.path.exists("reports"):
    os.makedirs("reports")


# =====================================================================
# 2. CORE / WORKERS (Thread Yapısı)
# =====================================================================

class URLScanWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, url):
        super().__init__()
        if not url.startswith("http://") and not url.startswith("https://"):
            self.url = "https://" + url
        else:
            self.url = url

    def run(self):
        start_time = time.time()
        ssl_status = "Valid / Active" if self.url.startswith("https://") else "No SSL (Insecure HTTP)"
        
        try:
            req = urllib.request.Request(
                self.url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) CyberShield/1.2'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                code = response.getcode()
                status_desc = f"HTTP {code} OK" if code == 200 else f"HTTP {code}"
        except urllib.error.HTTPError as e:
            status_desc = f"HTTP Error {e.code}"
        except urllib.error.URLError:
            status_desc = "Connection Refused / Host Unreachable" if current_lang == "EN" else "Bağlantı Reddedildi / Sunucuya Ulaşılamıyor"
            ssl_status = "Unknown" if current_lang == "EN" else "Bilinmiyor"
        except Exception:
            status_desc = "Scan Failed" if current_lang == "EN" else "Tarama Başarısız"
            ssl_status = "Unknown" if current_lang == "EN" else "Bilinmiyor"

        elapsed = round(time.time() - start_time, 2)
        
        results = {
            "url": self.url,
            "ssl_status": ssl_status,
            "domain_age": f"Response Time: {elapsed}s",
            "risk_level": "Low Risk" if "OK" in status_desc else "Suspicious / Unresponsive",
            "vt_result": f"Live Network Scan: {status_desc}"
        }
        
        if current_lang == "TR":
            if "OK" in status_desc:
                results["risk_level"] = "Düşük Risk"
            else:
                results["risk_level"] = "Şüpheli / Yanıt Vermiyor"

        self.finished.emit(results)


class FileAnalyzeWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.api_key = "e2c3b2e591b79f8b725c899c7bf5d0d8692780e0fa70b991ff5bfa95f32b85e0"

    def calculate_entropy(self, data):
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(x)) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return round(entropy, 2)

    # VT'deki gerçek engine isimleri prefix bazlı eşleştirilir.
    # Örnek: "BitDefender" → "BitDefenderFalx", "BitDefenderTheta" gibi isimlerle eşleşir.
    TARGET_ENGINES = {
        "Kaspersky":   "Kaspersky",
        "BitDefender": "BitDefender",
        "Microsoft":   "Microsoft",
        "Symantec":    "Symantec",
        "Sophos":      "Sophos",
        "Avast":       "Avast",
    }

    def _match_engines(self, results_map):
        """results_map içindeki engine isimlerini prefix eşleşmesiyle TARGET_ENGINES'e bağlar."""
        matched = {label: {"found": False, "malicious": False, "result": ""} for label in self.TARGET_ENGINES}
        for vt_engine, data in results_map.items():
            for label, prefix in self.TARGET_ENGINES.items():
                if vt_engine.lower().startswith(prefix.lower()):
                    # Aynı motor birden fazla isimle gelebilir; malicious olanı önceliklendir
                    if not matched[label]["found"] or data["category"] == "malicious":
                        matched[label]["found"] = True
                        matched[label]["malicious"] = data["category"] == "malicious"
                        matched[label]["result"] = data.get("result") or ("Clean" if current_lang == "EN" else "Temiz")
        engine_details = []
        for label, info in matched.items():
            if info["found"]:
                engine_details.append({
                    "name": label,
                    "malicious": info["malicious"],
                    "result": info["result"] if info["malicious"] else ("Clean" if current_lang == "EN" else "Temiz"),
                })
            else:
                engine_details.append({
                    "name": label,
                    "malicious": False,
                    "result": "Clean" if current_lang == "EN" else "Temiz",
                })
        return engine_details

    def _upload_file_and_get_analysis(self):
        """Dosyayı VT'ye yükler, analiz ID'sini döner."""
        import email.mime.multipart
        boundary = "----CyberShieldBoundary7MA4YWxkTrZu0gW"
        with open(self.file_path, "rb") as f:
            file_data = f.read()
        filename = os.path.basename(self.file_path)
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

        upload_req = urllib.request.Request("https://www.virustotal.com/api/v3/files", data=body)
        upload_req.add_header("x-apikey", self.api_key)
        upload_req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        with urllib.request.urlopen(upload_req, timeout=60) as resp:
            upload_data = json.loads(resp.read().decode())
        return upload_data["data"]["id"]

    def _poll_analysis(self, analysis_id):
        """Analiz tamamlanana kadar polling yapar, sonuç döner."""
        poll_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        for _ in range(20):  # max ~60 saniye bekle
            time.sleep(3)
            poll_req = urllib.request.Request(poll_url)
            poll_req.add_header("x-apikey", self.api_key)
            with urllib.request.urlopen(poll_req, timeout=15) as resp:
                poll_data = json.loads(resp.read().decode())
            status = poll_data["data"]["attributes"].get("status", "")
            if status == "completed":
                return poll_data["data"]["attributes"]
        return None

    def run(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError("Target file missing.")

            sha256_hash = hashlib.sha256()
            with open(self.file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256_hash.update(chunk)
            sha256 = sha256_hash.hexdigest()

            with open(self.file_path, "rb") as f:
                data = f.read()
            entropy = self.calculate_entropy(data)

            engine_details = []
            malicious_count = 0
            total_engines = 0
            is_clean = True
            threat_assessment = "Unknown / First Seen" if current_lang == "EN" else "Bilinmeyen / İlk Kez Görülüyor"

            # --- 1. Adım: Hash ile VT'yi sorgula ---
            hash_url = f"https://www.virustotal.com/api/v3/files/{sha256}"
            hash_req = urllib.request.Request(hash_url)
            hash_req.add_header("x-apikey", self.api_key)

            results_map = None
            stats = None

            try:
                with urllib.request.urlopen(hash_req, timeout=15) as response:
                    res_data = json.loads(response.read().decode())
                    stats = res_data["data"]["attributes"]["last_analysis_stats"]
                    results_map = res_data["data"]["attributes"]["last_analysis_results"]

            except urllib.error.HTTPError as e:
                if e.code == 404:
                    # --- 2. Adım: Hash bulunamadı → dosyayı yükle ve analiz et ---
                    try:
                        analysis_id = self._upload_file_and_get_analysis()
                        attrs = self._poll_analysis(analysis_id)
                        if attrs:
                            stats = attrs.get("stats", {})
                            results_map = attrs.get("results", {})
                        else:
                            threat_assessment = "Analysis timed out. Try again later." if current_lang == "EN" else "Analiz zaman aşımına uğradı. Tekrar deneyin."
                    except Exception as upload_err:
                        threat_assessment = f"Upload Error: {upload_err}" if current_lang == "EN" else f"Yükleme Hatası: {upload_err}"
                else:
                    threat_assessment = f"API Communication Error (HTTP {e.code})"

            # --- 3. Adım: Sonuçları işle ---
            if stats is not None and results_map is not None:
                malicious_count = stats.get("malicious", 0)
                total_engines = malicious_count + stats.get("undetected", 0) + stats.get("harmless", 0) + stats.get("suspicious", 0)
                engine_details = self._match_engines(results_map)

                if malicious_count > 0:
                    is_clean = False
                    threat_assessment = (
                        f"⚠️ CRITICAL: Threat Detected! ({malicious_count} AV Flagged)"
                        if current_lang == "EN" else
                        f"⚠️ KRİTİK: Tehdit Tespit Edildi! ({malicious_count} AV Yakaladı)"
                    )
                else:
                    threat_assessment = (
                        "✅ SAFE: Verified Clean by Global Indices"
                        if current_lang == "EN" else
                        "✅ GÜVENLİ: Küresel Motorlar Tarafından Doğrulandı"
                    )
            else:
                # Hiç sonuç gelemediyse fallback badge listesi
                for label in self.TARGET_ENGINES:
                    engine_details.append({"name": label, "malicious": False, "result": "N/A"})

            results = {
                "success": True,
                "filename": os.path.basename(self.file_path),
                "sha256": sha256,
                "entropy": entropy,
                "vt_result": f"{malicious_count} / {total_engines}" if total_engines > 0 else "0 / 0",
                "risk": threat_assessment,
                "is_clean": is_clean,
                "details": engine_details
            }
        except Exception as e:
            results = {"success": False, "error": str(e)}

        self.finished.emit(results)


# =====================================================================
# 3. MODERNIZED GUI MODULES (Görsel Ekran Yapıları)
# =====================================================================

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        self.title = QLabel()
        layout.addWidget(self.title)

        self.status_card = QFrame()
        status_layout = QVBoxLayout(self.status_card)
        self.status_lbl = QLabel()
        status_layout.addWidget(self.status_lbl, alignment=Qt.AlignCenter)
        layout.addWidget(self.status_card)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.scan_card = QFrame()
        v_box1 = QVBoxLayout(self.scan_card)
        self.lbl1 = QLabel()
        v_box1.addWidget(self.lbl1, alignment=Qt.AlignCenter)
        self.total_scan_val = QLabel("0")
        v_box1.addWidget(self.total_scan_val, alignment=Qt.AlignCenter)
        
        self.risk_card = QFrame()
        v_box2 = QVBoxLayout(self.risk_card)
        self.lbl2 = QLabel()
        v_box2.addWidget(self.lbl2, alignment=Qt.AlignCenter)
        self.risk_val = QLabel("0 / 100")
        v_box2.addWidget(self.risk_val, alignment=Qt.AlignCenter)

        stats_layout.addWidget(self.scan_card)
        stats_layout.addWidget(self.risk_card)
        layout.addLayout(stats_layout)

        self.event_lbl = QLabel()
        layout.addWidget(self.event_lbl)
        
        self.log_box = QFrame()
        log_layout = QVBoxLayout(self.log_box)
        log_layout.setSpacing(10)
        
        self.log1 = QLabel()
        self.log2 = QLabel()
        self.log3 = QLabel()
        for log in [self.log1, self.log2, self.log3]:
            log_layout.addWidget(log)
            
        layout.addWidget(self.log_box)
        
        layout.addSpacing(15)
        self.dev_frame = QFrame()
        dev_layout = QHBoxLayout(self.dev_frame)
        
        dev_name_lbl = QLabel("👨‍💻 Core Developer: <span style='color:#00FF66; font-weight:bold;'>Ozan Karakurt</span>")
        dev_name_lbl.setStyleSheet("font-size: 15px; color: #ffffff; font-family: 'Segoe UI';")
        dev_layout.addWidget(dev_name_lbl)
        dev_layout.addStretch()
        
        links_lbl = QLabel(
            "<a href='https://github.com/ozankarakurt' style='color:#00E5FF; text-decoration:none; font-weight:bold;'>🔗 GitHub</a>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;::&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
            "<a href='https://www.linkedin.com/in/ozan-karakurt-6a36bb39a/' style='color:#00FF66; text-decoration:none; font-weight:bold;'>🔗 LinkedIn</a>"
        )
        links_lbl.setStyleSheet("font-size: 14px; font-family: 'Segoe UI';")
        links_lbl.setOpenExternalLinks(True)
        dev_layout.addWidget(links_lbl)
        layout.addWidget(self.dev_frame)
        
        layout.addStretch()
        self.apply_theme_styles()
        self.retranslate_ui()

    def apply_theme_styles(self):
        if current_theme == "CYBER":
            self.title.setStyleSheet("font-size: 26px; font-weight: 800; color: #00E5FF; letter-spacing: 2px;")
            self.status_card.setStyleSheet("QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #101B2B, stop:1 #0A1220); border: 1px solid #00FF66; border-radius: 12px; padding: 25px;}")
            self.status_lbl.setStyleSheet("font-size: 20px; color: #00FF66; font-weight: bold; background: transparent;")
            self.scan_card.setStyleSheet("background-color: #111927; border: 1px solid #1F2937; border-radius: 12px; padding: 20px;")
            self.risk_card.setStyleSheet("background-color: #111927; border: 1px solid #1F2937; border-radius: 12px; padding: 20px;")
            self.total_scan_val.setStyleSheet("font-size: 42px; font-weight: 800; color: #ffffff;")
            self.risk_val.setStyleSheet("font-size: 42px; font-weight: 800; color: #00FF66;")
            self.log_box.setStyleSheet("background-color: #070D19; border: 1px solid #1F2937; border-radius: 10px; padding: 20px;")
            self.dev_frame.setStyleSheet("background-color: #111927; border: 1px solid #00E5FF; border-radius: 10px; padding: 16px;")
            self.lbl1.setStyleSheet("color: #9CA3AF; font-weight: bold; font-size: 14px; letter-spacing: 0.5px;")
            self.lbl2.setStyleSheet("color: #9CA3AF; font-weight: bold; font-size: 14px; letter-spacing: 0.5px;")
            self.event_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #9CA3AF;")
            for log in [self.log1, self.log2, self.log3]: log.setStyleSheet("font-family: 'Consolas'; color: #00FF66; font-size: 14px;")
        else: 
            self.title.setStyleSheet("font-size: 26px; font-weight: 800; color: #00FF00; letter-spacing: 2px; font-family: 'Courier New';")
            self.status_card.setStyleSheet("QFrame { background-color: #000000; border: 1px solid #00FF00; border-radius: 6px; padding: 25px;}")
            self.status_lbl.setStyleSheet("font-size: 20px; color: #00FF00; font-weight: bold; font-family: 'Courier New';")
            self.scan_card.setStyleSheet("background-color: #000000; border: 1px solid #00FF00; border-radius: 6px; padding: 20px;")
            self.risk_card.setStyleSheet("background-color: #000000; border: 1px solid #00FF00; border-radius: 6px; padding: 20px;")
            self.total_scan_val.setStyleSheet("font-size: 42px; font-weight: 800; color: #00FF00; font-family: 'Courier New';")
            self.risk_val.setStyleSheet("font-size: 42px; font-weight: 800; color: #00FF00; font-family: 'Courier New';")
            self.log_box.setStyleSheet("background-color: #000000; border: 1px solid #00FF00; border-radius: 6px; padding: 20px;")
            self.dev_frame.setStyleSheet("background-color: #000000; border: 1px solid #00FF00; border-radius: 6px; padding: 16px;")
            self.lbl1.setStyleSheet("color: #00FF00; font-family: 'Courier New'; font-size: 14px;")
            self.lbl2.setStyleSheet("color: #00FF00; font-family: 'Courier New'; font-size: 14px;")
            self.event_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #00FF00; font-family: 'Courier New';")
            for log in [self.log1, self.log2, self.log3]: log.setStyleSheet("font-family: 'Courier New'; color: #00FF00; font-size: 14px;")

    def update_scan_count(self):
        try:
            if os.path.exists("reports"):
                count = len([f for f in os.listdir("reports") if f.endswith(".txt")])
                self.total_scan_val.setText(str(count))
            else:
                self.total_scan_val.setText("0")
        except:
            self.total_scan_val.setText("0")

    def append_dynamic_log(self, message):
        self.log1.setText(self.log2.text())
        self.log2.setText(self.log3.text())
        self.log3.setText(message)

    def retranslate_ui(self):
        self.title.setText(tr("dash_title"))
        self.status_lbl.setText(tr("dash_status"))
        self.lbl1.setText(tr("dash_scans"))
        self.lbl2.setText(tr("dash_risk"))
        self.event_lbl.setText(tr("dash_events"))
        if not hasattr(self, 'initialized_logs'):
            self.log1.setText(tr("dash_log1"))
            self.log2.setText(tr("dash_log2"))
            self.log3.setText(tr("dash_log3"))
            self.initialized_logs = True
        self.update_scan_count()


class URLScannerView(QWidget):
    scan_completed = pyqtSignal()
    log_triggered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        self.title = QLabel()
        layout.addWidget(self.title)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)
        self.url_input = QLineEdit()
        self.scan_btn = QPushButton()
        self.scan_btn.setCursor(Qt.PointingHandCursor)
        self.scan_btn.clicked.connect(self.start_scan)

        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.scan_btn)
        layout.addLayout(input_layout)

        self.console_lbl = QLabel()
        self.console_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #9CA3AF;")
        layout.addWidget(self.console_lbl)
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)
        self.apply_theme_styles()
        self.retranslate_ui()

    def apply_theme_styles(self):
        if current_theme == "CYBER":
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00E5FF; letter-spacing: 1px;")
            self.url_input.setStyleSheet("QLineEdit { background-color: #111927; border: 1px solid #1F2937; border-radius: 8px; padding: 14px; color: #ffffff; font-size: 15px; } QLineEdit:focus { border: 1px solid #00E5FF; }")
            self.scan_btn.setStyleSheet("QPushButton { background-color: #00FF66; color: #0B0F19; font-weight: bold; font-size: 15px; border-radius: 8px; padding: 14px 28px; } QPushButton:hover { background-color: #00E5FF; } QPushButton:disabled { background-color: #1F2937; color: #4B5563; }")
            self.result_display.setStyleSheet("QTextEdit { background-color: #070D19; border: 1px solid #1F2937; border-radius: 10px; color: #00FF66; font-family: 'Consolas'; font-size: 15px; padding: 18px; line-height: 1.6;}")
        else:
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00FF00; font-family: 'Courier New';")
            self.url_input.setStyleSheet("QLineEdit { background-color: #000000; border: 1px solid #00FF00; border-radius: 4px; padding: 14px; color: #00FF00; font-family: 'Courier New'; }")
            self.scan_btn.setStyleSheet("QPushButton { background-color: #000000; border: 1px solid #00FF00; color: #00FF00; font-weight: bold; font-family: 'Courier New'; padding: 14px 28px; border-radius: 4px;} QPushButton:hover { background-color: #003300; }")
            self.result_display.setStyleSheet("QTextEdit { background-color: #000000; border: 1px solid #00FF00; border-radius: 4px; color: #00FF00; font-family: 'Courier New'; font-size: 15px; padding: 18px;}")

    def retranslate_ui(self):
        self.title.setText(tr("url_title"))
        self.url_input.setPlaceholderText(tr("url_placeholder"))
        self.scan_btn.setText(tr("url_btn"))
        self.console_lbl.setText(tr("url_console"))

    def start_scan(self):
        url = self.url_input.text().strip()
        if not url:
            self.result_display.setText(tr("url_err_empty"))
            return

        self.result_display.setText(tr("url_scanning").format(url))
        self.scan_btn.setEnabled(False)
        
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_triggered.emit(f"[{time_str}] [URL_SCAN] Querying connection state for {url[:25]}...")

        self.worker = URLScanWorker(url)
        self.worker.finished.connect(self.handle_results)
        self.worker.start()

    def handle_results(self, results):
        self.scan_btn.setEnabled(True)
        header = "ANALYSIS COMPLETE FOR" if current_lang == "EN" else "TARAMA TAMAMLANDI"
        ssl_lbl = "SSL Certificate Status" if current_lang == "EN" else "SSL Sertifika Durumu"
        age_lbl = "Domain Registration Age" if current_lang == "EN" else "Alan Adı Yaşı"
        risk_lbl = "CyberShield Risk Index" if current_lang == "EN" else "CyberShield Risk Endeksi"
        vt_lbl = "VirusTotal Intel Report" if current_lang == "EN" else "VirusTotal İstihbaratı"
        footer = "Diagnostics complete." if current_lang == "EN" else "Teşhis işlemi tamamlandı."

        border_color = "#00FF66" if current_theme == "CYBER" else "#00FF00"
        if "Low Risk" in results['risk_level'] or "Düşük Risk" in results['risk_level']:
            card_style = f"<div style='background-color: #0c2419; border: 1px solid {border_color}; border-radius: 8px; padding: 15px; margin-bottom: 15px;'><h2 style='color: {border_color}; margin: 0; font-size: 18px;'>🛡️ SYSTEM ASSESSMENT: SECURE (LOW RISK)</h2></div>"
        else:
            card_style = "<div style='background-color: #2d141a; border: 1px solid #ff3366; border-radius: 8px; padding: 15px; margin-bottom: 15px;'><h2 style='color: #ff3366; margin: 0; font-size: 18px;'>⚠️ ALERT: SUSPICIOUS ACTIVITY DETECTED</h2></div>"

        font_fam = "Consolas" if current_theme == "CYBER" else "Courier New"
        html_report = f"""{card_style}
        <div style="font-family: '{font_fam}', monospace; font-size: 14px; line-height: 1.5; color: #e5e7eb;">
            <b>[-] {header}:</b> <span style="color: #00E5FF;">{results['url']}</span><br>
            -----------------------------------------------------------------<br>
            <b>[>] {ssl_lbl} :</b> {results['ssl_status']}<br>
            <b>[>] {age_lbl} :</b> {results['domain_age']}<br>
            <b>[>] {risk_lbl} :</b> <span style="font-weight: bold; color: {'#00FF66' if 'Low' in results['risk_level'] or 'Düşük' in results['risk_level'] else '#ff3366'};">{results['risk_level']}</span><br>
            <b>[>] {vt_lbl} :</b> {results['vt_result']}<br>
            -----------------------------------------------------------------<br>
            <span style="color: #9CA3AF;">[STATUS] {footer}</span>
        </div>"""
        
        self.result_display.setHtml(html_report)

        text_report = f"[+] {header}: {results['url']}\n-------------------\n[>] {ssl_lbl} : {results['ssl_status']}\n[>] {age_lbl}: {results['domain_age']}\n[>] {risk_lbl} : {results['risk_level']}\n[>] {vt_lbl}: {results['vt_result']}\n-------------------\n[STATUS] {footer}"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_url = results['url'].replace("https://", "").replace("http://", "").replace("/", "_")
        filename = f"reports/url_{safe_url}_{timestamp}.txt"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text_report)
        except:
            pass
        
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_triggered.emit(f"[{time_str}] [SUCCESS] Report generated: {os.path.basename(filename)[:30]}")
        self.scan_completed.emit()


class PasswordAnalyzerView(QWidget):
    log_triggered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        self.title = QLabel()
        layout.addWidget(self.title)

        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.textChanged.connect(self.analyze_password)
        layout.addWidget(self.pwd_input)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.console_lbl = QLabel()
        self.console_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #9CA3AF;")
        layout.addWidget(self.console_lbl)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)
        
        self.vulnerability_dictionary = {"123456", "123456789", "password", "password123", "admin", "qwerty", "cybershield", "nmap_projem"}
        self.apply_theme_styles()
        self.retranslate_ui()

    def apply_theme_styles(self):
        if current_theme == "CYBER":
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00E5FF; letter-spacing: 1px;")
            self.pwd_input.setStyleSheet("QLineEdit { background-color: #111927; border: 1px solid #1F2937; border-radius: 8px; padding: 14px; color: #ffffff; font-size: 15px; } QLineEdit:focus { border: 1px solid #00E5FF; }")
            self.progress.setStyleSheet("QProgressBar { border: none; border-radius: 4px; background-color: #070D19; height: 8px; text-align: transparent;} QProgressBar::chunk { background-color: #00FF66; border-radius: 4px; }")
            self.result_display.setStyleSheet("QTextEdit { background-color: #070D19; border: 1px solid #1F2937; border-radius: 10px; color: #ffffff; font-family: 'Consolas'; font-size: 15px; padding: 18px; line-height: 1.6;}")
        else:
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00FF00; font-family: 'Courier New';")
            self.pwd_input.setStyleSheet("QLineEdit { background-color: #000000; border: 1px solid #00FF00; border-radius: 4px; padding: 14px; color: #00FF00; font-family: 'Courier New'; }")
            self.progress.setStyleSheet("QProgressBar { border: 1px solid #00FF00; background-color: #000000; height: 10px; text-align: transparent;} QProgressBar::chunk { background-color: #00FF00; }")
            self.result_display.setStyleSheet("QTextEdit { background-color: #000000; border: 1px solid #00FF00; border-radius: 4px; color: #00FF00; font-family: 'Courier New'; font-size: 15px; padding: 18px;}")

    def retranslate_ui(self):
        self.title.setText(tr("pwd_title"))
        self.pwd_input.setPlaceholderText(tr("pwd_placeholder"))
        self.console_lbl.setText(tr("url_console"))
        self.analyze_password(self.pwd_input.text())

    def analyze_password(self, text):
        if not text:
            self.progress.setValue(0)
            self.result_display.clear()
            return

        is_dictionary_match = text.lower() in self.vulnerability_dictionary

        pool = 0
        if any(c.islower() for c in text): pool += 26
        if any(c.isupper() for c in text): pool += 26
        if any(c.isdigit() for c in text): pool += 10
        if any(not c.isalnum() for c in text): pool += 32

        entropy = math.log2(pool) * len(text) if pool > 0 else 0
        score = min(100, int((entropy / 80) * 100))

        bg_color = "#070D19" if current_theme == "CYBER" else "#000000"
        border_style = "border:none;" if current_theme == "CYBER" else "border: 1px solid #00FF00;"
        border_color = "#00FF66" if current_theme == "CYBER" else "#00FF00"

        if is_dictionary_match:
            self.progress.setValue(15)
            self.progress.setStyleSheet(f"QProgressBar::chunk {{ background-color: #FF3366; }} QProgressBar {{ height: 8px; {border_style} background:{bg_color}; }}")
            card_style = "<div style='background-color: #2d141a; border: 1px solid #ff3366; border-radius: 8px; padding: 15px; margin-bottom: 15px;'><h2 style='color: #ff3366; margin: 0; font-size: 18px;'>⚠️ CRITICAL STATUS: COMPROMISED VECTOR</h2></div>"
            crack_time = tr("pwd_time_low")
            strategy = tr("pwd_sug_dict")
        else:
            self.progress.setValue(score)
            if score < 40:
                self.progress.setStyleSheet(f"QProgressBar::chunk {{ background-color: #FF3366; }} QProgressBar {{ height: 8px; {border_style} background:{bg_color}; }}")
                card_style = "<div style='background-color: #2d141a; border: 1px solid #ff3366; border-radius: 8px; padding: 15px; margin-bottom: 15px;'><h2 style='color: #ff3366; margin: 0; font-size: 18px;'>❌ ANALYSIS OUTCOME: WEAK COMPLEXITY</h2></div>"
                crack_time = tr("pwd_time_low")
                strategy = tr("pwd_sug_low")
            elif score < 75:
                orange_c = "#FFA500" if current_theme == "CYBER" else "#00FF00"
                self.progress.setStyleSheet(f"QProgressBar::chunk {{ background-color: {orange_c}; }} QProgressBar {{ height: 8px; {border_style} background:{bg_color}; }}")
                card_style = f"<div style='background-color: #3b2311; border: 1px solid {orange_c}; border-radius: 8px; padding: 15px; margin-bottom: 15px;'><h2 style='color: {orange_c}; margin: 0; font-size: 18px;'>⚠️ ANALYSIS OUTCOME: MEDIUM ENTROPY</h2></div>"
                crack_time = tr("pwd_time_med")
                strategy = tr("pwd_sug_med")
            else:
                green_c = "#00FF66" if current_theme == "CYBER" else "#00FF00"
                self.progress.setStyleSheet(f"QProgressBar::chunk {{ background-color: {green_c}; }} QProgressBar {{ height: 8px; {border_style} background:{bg_color}; }}")
                card_style = f"<div style='background-color: #0c2419; border: 1px solid {border_color}; border-radius: 8px; padding: 15px; margin-bottom: 15px;'><h2 style='color: {border_color}; margin: 0; font-size: 18px;'>🛡️ ANALYSIS OUTCOME: CRYPTOGRAPHICALLY RESILIENT</h2></div>"
                crack_time = tr("pwd_time_high")
                strategy = tr("pwd_sug_high")

        font_fam = "Consolas" if current_theme == "CYBER" else "Courier New"
        
        html_report = f"""{card_style}
        <div style="font-family: '{font_fam}', monospace; font-size: 14px; line-height: 1.6; color: #e5e7eb;">
            <b>[-] METRIC SEQUENCE COMPUTED</b><br>
            -----------------------------------------------------------------<br>
            <b>[SHANNON ENTROPY]</b>  : <span style="color: #00E5FF; font-weight: bold;">{round(entropy, 2)} Bits</span><br>
            <b>[CRACK TIME EST.]</b>  : {crack_time}<br>
            <b>[REMEDIATION STRAT]</b>: <span style="color: #FFA500;">{strategy}</span><br>
            -----------------------------------------------------------------<br>
            <span style="color: #9CA3AF;">[INFO] Strength weight based on unique mathematical pools & length.</span>
        </div>"""
        
        self.result_display.setHtml(html_report)


class FileAnalyzerView(QWidget):
    scan_completed = pyqtSignal()
    log_triggered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        self.title = QLabel()
        layout.addWidget(self.title)

        self.select_btn = QPushButton()
        self.select_btn.setCursor(Qt.PointingHandCursor)
        self.select_btn.clicked.connect(self.browse_file)
        layout.addWidget(self.select_btn)

        self.console_lbl = QLabel()
        self.console_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #9CA3AF;")
        layout.addWidget(self.console_lbl)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)
        self.apply_theme_styles()
        self.retranslate_ui()

    def apply_theme_styles(self):
        if current_theme == "CYBER":
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00E5FF; letter-spacing: 1px;")
            self.select_btn.setStyleSheet("QPushButton { background-color: transparent; border: 1px solid #00FF66; color: #00FF66; font-weight: bold; font-size: 15px; border-radius: 8px; padding: 15px; } QPushButton:hover { background-color: #00FF66; color: #0B0F19; }")
            self.result_display.setStyleSheet("QTextEdit { background-color: #070D19; border: 1px solid #1F2937; border-radius: 10px; color: #ffffff; font-family: 'Consolas'; font-size: 15px; padding: 18px; line-height: 1.6;}")
        else:
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00FF00; font-family: 'Courier New';")
            self.select_btn.setStyleSheet("QPushButton { background-color: #000000; border: 1px solid #00FF00; color: #00FF00; font-weight: bold; font-family: 'Courier New'; padding: 15px; border-radius: 4px; } QPushButton:hover { background-color: #003300; }")
            self.result_display.setStyleSheet("QTextEdit { background-color: #000000; border: 1px solid #00FF00; border-radius: 4px; color: #00FF00; font-family: 'Courier New'; font-size: 15px; padding: 18px;}")

    def retranslate_ui(self):
        self.title.setText(tr("file_title"))
        self.select_btn.setText(tr("file_btn"))
        self.console_lbl.setText(tr("url_console"))

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Target File", "", "All Files (*)")
        if file_path:
            self.result_display.setText(tr("file_reading").format(file_path))
            
            time_str = datetime.now().strftime("%H:%M:%S")
            self.log_triggered.emit(f"[{time_str}] [FILE] Analyzing local binary: {os.path.basename(file_path)[:20]}")

            self.worker = FileAnalyzeWorker(file_path)
            self.worker.finished.connect(self.display_report)
            self.worker.start()

    def display_report(self, results):
        if not results["success"]:
            self.result_display.setText(tr("file_err").format(results['error']))
            return

        h_report = "LIVE CLOUD THREAT INTELLIGENCE REPORT" if current_lang == "EN" else "CANLI BULUT TEHDİT İSTİHBARAT RAPORU"
        h_detect = "AV Engines flagged this signature" if current_lang == "EN" else "Antivirüs motoru bu imzayı zararlı olarak işaretledi"
        h_info = "Threat matrix lookup completed via external API secure tunnels." if current_lang == "EN" else "Tehdit matrisi sorgulaması dış API güvenli tünelleri üzerinden tamamlandı."
        h_vendors = "POPULAR AV VENDOR TELEMETRY" if current_lang == "EN" else "POPÜLER ANTİVİRÜS YAZILIMLARININ TELEMETRİSİ"

        border_color = "#00FF66" if current_theme == "CYBER" else "#00FF00"
        if results["is_clean"]:
            card_style = f"<div style='background-color: #0c2419; border: 1px solid {border_color}; border-radius: 8px; padding: 15px; margin-bottom: 15px;'><h2 style='color: {border_color}; margin: 0; font-size: 18px;'>🛡️ STATIC MATRIX: FILE IS VERIFIED CLEAN</h2></div>"
        else:
            card_style = "<div style='background-color: #2d141a; border: 1px solid #ff3366; border-radius: 8px; padding: 15px; margin-bottom: 15px;'><h2 style='color: #ff3366; margin: 0; font-size: 18px;'>⚠️ SECURITY BREAK: MALICIOUS PAYLOAD DETECTED</h2></div>"

        font_fam = "Consolas" if current_theme == "CYBER" else "Courier New"
        
        # Build AV engine badges
        av_badges_html = ""
        for eng in results['details']:
            if eng["malicious"]:
                icon = "🔴"
                color = "#ff3366"
                bg = "#2d141a"
                label = eng["result"]
            else:
                icon = "✅"
                color = "#00FF66" if current_theme == "CYBER" else "#00FF00"
                bg = "#0c2419"
                label = eng["result"]
            av_badges_html += (
                f"<div style='display:block; background:{bg}; border:1px solid {color}; "
                f"border-radius:8px; padding:10px 16px; margin:5px 0; font-size:16px; "
                f"font-weight:bold; font-family:\"{font_fam}\"; color:{color};'>"
                f"{icon} {eng['name']}</div>"
            )

        html_report = f"""{card_style}
        <div style="font-family: '{font_fam}', monospace; font-size: 14px; line-height: 1.6; color: #e5e7eb;">
            <b>[+] {h_report}</b><br>
            -----------------------------------------------------------------<br>
            <b>[FILE NAME]</b>       : <span style="color: #00E5FF;">{results['filename']}</span><br>
            <b>[SHA256 CHECKSUM]</b> : <span style="color: #FFA500;">{results['sha256']}</span><br>
            <b>[SHANNON ENTROPY]</b> : {results['entropy']} Bits/Byte<br>
            <b>[DETECTION RATIO]</b> : <span style="font-weight: bold; color: {'#00FF66' if results['is_clean'] else '#ff3366'};">{results['vt_result']} ({h_detect})</span><br>
            <b>[ASSESSMENT]</b>      : <span style="font-weight: bold; color: {'#00FF66' if results['is_clean'] else '#ff3366'};">{results['risk']}</span><br><br>
            
            <b>[=] {h_vendors}:</b><br>
            <div style="margin-top:8px; margin-bottom:8px;">{av_badges_html}</div>
            -----------------------------------------------------------------<br>
            <span style="color: #9CA3AF;">[INFO] {h_info}</span>
        </div>"""
        
        self.result_display.setHtml(html_report)

        details_text = "\n".join([f"   |- {e['name'].ljust(15)}: {'[MALICIOUS] ' + e['result'] if e['malicious'] else e['result']}" for e in results['details']])
        text_report = f"[+] {h_report}\n-------------------\n[FILENAME] : {results['filename']}\n[SHA256]   : {results['sha256']}\n[ENTROPY]  : {results['entropy']} Bits/Byte\n[DETECTION]: {results['vt_result']}\n[RISK]     : {results['risk']}\n\n[VENDORS]:\n{details_text}\n-------------------\n[INFO] {h_info}"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/file_{results['filename']}_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text_report)
        except:
            pass

        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_triggered.emit(f"[{time_str}] [SUCCESS] Report generated.")
        self.scan_completed.emit()


class ReportsView(QWidget):
    history_wiped = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        self.title = QLabel()
        layout.addWidget(self.title)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        list_pipe = QVBoxLayout()
        self.list_lbl = QLabel()
        self.list_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #9CA3AF;")
        list_pipe.addWidget(self.list_lbl)
        
        self.reports_list = QListWidget()
        self.reports_list.itemClicked.connect(self.load_report_details)
        list_pipe.addWidget(self.reports_list)
        content_layout.addLayout(list_pipe, stretch=2)

        details_pipe = QVBoxLayout()
        self.details_lbl = QLabel()
        self.details_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #9CA3AF;")
        details_pipe.addWidget(self.details_lbl)
        
        self.details_display = QTextEdit()
        self.details_display.setReadOnly(True)
        details_pipe.addWidget(self.details_display)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.download_btn = QPushButton()
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.clicked.connect(self.download_selected_report)
        
        self.delete_btn = QPushButton()
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.clicked.connect(self.delete_selected_report)
        
        self.clear_btn = QPushButton()
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_all_reports)
        
        buttons_layout.addWidget(self.download_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.clear_btn)
        details_pipe.addLayout(buttons_layout)
        
        content_layout.addLayout(details_pipe, stretch=3)
        layout.addLayout(content_layout)
        
        self.apply_theme_styles()
        self.refresh_reports_list()
        self.retranslate_ui()

    def apply_theme_styles(self):
        if current_theme == "CYBER":
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00E5FF; letter-spacing: 1px;")
            self.reports_list.setStyleSheet("QListWidget { background-color: #111927; border: 1px solid #1F2937; border-radius: 8px; color: #e5e7eb; padding: 6px; font-size: 14px; } QListWidget::item { padding: 12px; border-bottom: 1px solid #1F2937; border-radius: 4px;} QListWidget::item:hover { background-color: #1F2937; color: #00FF66; } QListWidget::item:selected { background-color: #1F2937; color: #00E5FF; font-weight: bold; }")
            self.details_display.setStyleSheet("QTextEdit { background-color: #070D19; border: 1px solid #1F2937; border-radius: 10px; color: #ffffff; font-family: 'Consolas'; font-size: 15px; padding: 18px; line-height: 1.6;}")
            self.download_btn.setStyleSheet("QPushButton { background-color: transparent; border: 1px solid #00E5FF; color: #00E5FF; font-weight: bold; font-size: 13px; border-radius: 8px; padding: 12px; margin-top: 5px;} QPushButton:hover { background-color: #00E5FF; color: #0B0F19; }")
            self.delete_btn.setStyleSheet("QPushButton { background-color: transparent; border: 1px solid #FF3366; color: #FF3366; font-weight: bold; font-size: 13px; border-radius: 8px; padding: 12px; margin-top: 5px;} QPushButton:hover { background-color: #FF3366; color: #ffffff; }")
            self.clear_btn.setStyleSheet("QPushButton { background-color: transparent; border: 1px solid #FFA500; color: #FFA500; font-weight: bold; font-size: 13px; border-radius: 8px; padding: 12px; margin-top: 5px;} QPushButton:hover { background-color: #FFA500; color: #0B0F19; }")
        else:
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00FF00; font-family: 'Courier New';")
            self.reports_list.setStyleSheet("QListWidget { background-color: #000000; border: 1px solid #00FF00; color: #00FF00; font-family: 'Courier New'; } QListWidget::item { border-bottom: 1px solid #003300; padding:10px; } QListWidget::item:selected { background-color: #003300; color: #00FF00; font-weight:bold; }")
            self.details_display.setStyleSheet("QTextEdit { background-color: #000000; border: 1px solid #00FF00; color: #00FF00; font-family: 'Courier New'; font-size: 15px; }")
            btn_base = "QPushButton { background-color: #000000; border: 1px solid #00FF00; color: #00FF00; font-family: 'Courier New'; font-weight: bold; padding: 12px; border-radius: 4px; } QPushButton:hover { background-color: #003300; }"
            self.download_btn.setStyleSheet(btn_base)
            self.delete_btn.setStyleSheet(btn_base)
            self.clear_btn.setStyleSheet(btn_base)

    def retranslate_ui(self):
        self.title.setText(tr("rep_title"))
        self.list_lbl.setText(tr("rep_list_lbl"))
        self.details_lbl.setText(tr("rep_details_lbl"))
        self.download_btn.setText(tr("rep_download_btn"))
        self.delete_btn.setText(tr("rep_delete_btn"))
        self.clear_btn.setText(tr("rep_clear_btn"))

    def refresh_reports_list(self):
        self.reports_list.clear()
        if not os.path.exists("reports"):
            return
            
        try:
            files = [f for f in os.listdir("reports") if f.endswith(".txt")]
            files.sort(reverse=True)
        except:
            files = []

        if not files:
            self.reports_list.addItem(tr("rep_empty"))
            self.reports_list.setEnabled(False)
            self.download_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            self.clear_btn.setEnabled(False)
            self.details_display.clear()
        else:
            self.reports_list.setEnabled(True)
            self.download_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            self.clear_btn.setEnabled(True)
            for file in files:
                self.reports_list.addItem(file)

    def load_report_details(self, item):
        filename = item.text()
        filepath = os.path.join("reports", filename)
        if not os.path.exists(filepath): return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.details_display.setText(content)
        except:
            self.details_display.setText(tr("rep_load_err"))

    def download_selected_report(self):
        selected_items = self.reports_list.selectedItems()
        if not selected_items or selected_items[0].text() == tr("rep_empty"):
            QMessageBox.warning(self, tr("rep_dl_err_title"), tr("rep_dl_err_no_select"))
            return
            
        filename = selected_items[0].text()
        report_content = self.details_display.toPlainText()
        
        options = QMessageBox.Options()
        dest_path, _ = QFileDialog.getSaveFileName(self, tr("rep_download_btn"), filename, "Text Files (*.txt);;All Files (*)")
        
        if dest_path:
            try:
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(report_content)
                QMessageBox.information(self, tr("rep_dl_success_title"), tr("rep_dl_success_msg").format(dest_path))
            except Exception as e:
                QMessageBox.critical(self, tr("rep_dl_err_title"), f"{tr('rep_dl_err_fail')}\nError: {str(e)}")

    def delete_selected_report(self):
        selected_items = self.reports_list.selectedItems()
        if not selected_items or selected_items[0].text() == tr("rep_empty"):
            return
            
        filename = selected_items[0].text()
        filepath = os.path.join("reports", filename)
        
        confirm = QMessageBox.question(self, tr("rep_del_confirm_title"), tr("rep_del_confirm_msg"), QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                self.refresh_reports_list()
                self.history_wiped.emit()
            except Exception as e:
                QMessageBox.critical(self, tr("rep_dl_err_title"), f"Error: {str(e)}")

    def clear_all_reports(self):
        if not os.path.exists("reports"): return
        
        confirm = QMessageBox.question(self, tr("rep_clear_confirm_title"), tr("rep_clear_confirm_msg"), QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                for file in os.listdir("reports"):
                    if file.endswith(".txt"):
                        os.remove(os.path.join("reports", file))
                self.refresh_reports_list()
                self.history_wiped.emit()
            except Exception as e:
                QMessageBox.critical(self, tr("rep_dl_err_title"), f"Error: {str(e)}")


class SettingsView(QWidget):
    language_changed = pyqtSignal()
    theme_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        self.title = QLabel()
        layout.addWidget(self.title)

        self.lang_lbl = QLabel()
        self.lang_lbl.setStyleSheet("font-size: 16px; margin-top: 10px; color: #9CA3AF;")
        layout.addWidget(self.lang_lbl)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English (EN)", "Türkçe (TR)"])
        self.lang_combo.setCurrentIndex(0 if current_lang == "EN" else 1)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.lang_combo)

        self.theme_lbl = QLabel()
        self.theme_lbl.setStyleSheet("font-size: 16px; margin-top: 20px; color: #9CA3AF;")
        layout.addWidget(self.theme_lbl)

        self.theme_combo = QComboBox()
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        layout.addWidget(self.theme_combo)

        layout.addStretch()
        self.apply_theme_styles()
        self.retranslate_ui()

    def apply_theme_styles(self):
        if current_theme == "CYBER":
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00E5FF; letter-spacing: 1px;")
            combo_style = "QComboBox { background-color: #111927; border: 1px solid #1F2937; border-radius: 8px; padding: 12px; color: #ffffff; font-size: 15px; min-width: 240px; } QComboBox::drop-down { border: none; } QComboBox QAbstractItemView { background-color: #111927; color: #ffffff; selection-background-color: #1F2937; selection-color: #00FF66; }"
            self.lang_combo.setStyleSheet(combo_style)
            self.theme_combo.setStyleSheet(combo_style)
        else:
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00FF00; font-family: 'Courier New';")
            combo_style = "QComboBox { background-color: #000000; border: 1px solid #00FF00; padding: 12px; color: #00FF00; font-family: 'Courier New'; min-width: 240px; } QComboBox QAbstractItemView { background-color: #000000; color: #00FF00; }"
            self.lang_combo.setStyleSheet(combo_style)
            self.theme_combo.setStyleSheet(combo_style)

    def retranslate_ui(self):
        self.title.setText(tr("set_title"))
        self.lang_lbl.setText(tr("set_lang_lbl"))
        self.theme_lbl.setText(tr("set_theme_lbl"))
        
        self.theme_combo.blockSignals(True)
        self.theme_combo.clear()
        self.theme_combo.addItems([tr("theme_cyber"), tr("theme_hacker")])
        self.theme_combo.setCurrentIndex(0 if current_theme == "CYBER" else 1)
        self.theme_combo.blockSignals(False)

    def change_language(self, index):
        global current_lang
        current_lang = "EN" if index == 0 else "TR"
        self.retranslate_ui()
        self.language_changed.emit()

    def change_theme(self, index):
        global current_theme
        current_theme = "CYBER" if index == 0 else "HACKER"
        self.apply_theme_styles()
        self.theme_changed.emit()


class DetectionTheoryView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        self.title = QLabel()
        layout.addWidget(self.title)

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)
        self.apply_theme_styles()
        self.retranslate_ui()

    def apply_theme_styles(self):
        if current_theme == "CYBER":
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00E5FF; letter-spacing: 1px;")
            self.text_display.setStyleSheet("QTextEdit { background-color: #070D19; border: 1px solid #1F2937; border-radius: 10px; color: #e5e7eb; font-family: 'Segoe UI'; font-size: 15px; padding: 22px; line-height: 1.6; }")
        else:
            self.title.setStyleSheet("font-size: 24px; font-weight: 800; color: #00FF00; font-family: 'Courier New';")
            self.text_display.setStyleSheet("QTextEdit { background-color: #000000; border: 1px solid #00FF00; color: #00FF00; font-family: 'Courier New'; font-size: 15px; padding: 22px; }")

    def retranslate_ui(self):
        self.title.setText(tr("about_title"))
        self.text_display.setText(tr("about_content"))


# =====================================================================
# 4. MAIN WINDOW & COCKPIT CONTROLLER (Ana Yönetim Merkezi)
# =====================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberShield OS v1.3")
        self.resize(1260, 820)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(14, 30, 14, 30)
        self.sidebar_layout.setSpacing(10)

        self.logo = QLabel()
        self.sidebar_layout.addWidget(self.logo)

        self.modules_meta = [
            ("menu_dashboard", 0), ("menu_url", 1), ("menu_pwd", 2),
            ("menu_file", 3), ("menu_reports", 4), ("menu_settings", 5), ("menu_about", 6)
        ]
        
        self.menu_buttons = {}

        for key_name, index in self.modules_meta:
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=index: self.switch_tab(idx))
            self.sidebar_layout.addWidget(btn)
            self.menu_buttons[index] = (btn, key_name)

        self.sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        
        self.dash_view = DashboardView()
        self.url_view = URLScannerView()
        self.pwd_view = PasswordAnalyzerView()
        self.file_view = FileAnalyzerView()
        self.reports_view = ReportsView()
        self.settings_view = SettingsView()
        self.about_view = DetectionTheoryView()
        
        self.url_view.scan_completed.connect(self.reports_view.refresh_reports_list)
        self.url_view.scan_completed.connect(self.dash_view.update_scan_count)
        self.url_view.log_triggered.connect(self.dash_view.append_dynamic_log)

        self.file_view.scan_completed.connect(self.reports_view.refresh_reports_list)
        self.file_view.scan_completed.connect(self.dash_view.update_scan_count)
        self.file_view.log_triggered.connect(self.dash_view.append_dynamic_log)

        self.pwd_view.log_triggered.connect(self.dash_view.append_dynamic_log)
        
        self.reports_view.history_wiped.connect(self.dash_view.update_scan_count)
        
        self.settings_view.language_changed.connect(self.reload_all_languages)
        self.settings_view.theme_changed.connect(self.reload_all_themes)

        self.stack.addWidget(self.dash_view)          
        self.stack.addWidget(self.url_view)           
        self.stack.addWidget(self.pwd_view)           
        self.stack.addWidget(self.file_view)          
        self.stack.addWidget(self.reports_view)       
        self.stack.addWidget(self.settings_view)       
        self.stack.addWidget(self.about_view)

        self.main_layout.addWidget(self.stack)
        
        self.reload_all_themes()
        self.reload_all_languages()
        self.menu_buttons[0][0].setChecked(True)

    def switch_tab(self, index):
        self.stack.setCurrentIndex(index)
        if index == 4:
            self.reports_view.refresh_reports_list()
        elif index == 0:
            self.dash_view.update_scan_count()

    def reload_all_themes(self):
        if current_theme == "CYBER":
            self.setStyleSheet("QMainWindow { background-color: #0B0F19; } QWidget { background-color: #0B0F19; color: #E5E7EB; font-family: 'Segoe UI'; font-size: 14px; }")
            self.sidebar.setStyleSheet("QFrame#Sidebar { background-color: #090D14; border-right: 1px solid #111927; max-width: 260px; min-width: 260px; }")
            self.logo.setStyleSheet("color: #00FF66; font-size: 24px; font-weight: 800; margin-bottom: 40px; padding-left: 12px; font-family: 'Courier New'; letter-spacing: 1px;")
            btn_style = "QPushButton { background-color: transparent; color: #9CA3AF; border: none; border-radius: 8px; padding: 15px; text-align: left; font-size: 15px; font-weight: 500; } QPushButton:hover { background-color: #111927; color: #00E5FF; } QPushButton:checked { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #112235, stop:1 #090D14); color: #00FF66; font-weight: bold; }"
        else: 
            self.setStyleSheet("QMainWindow { background-color: #000000; } QWidget { background-color: #000000; color: #00FF00; font-family: 'Courier New'; font-size: 14px; }")
            self.sidebar.setStyleSheet("QFrame#Sidebar { background-color: #000000; border-right: 1px solid #00FF00; max-width: 260px; min-width: 260px; }")
            self.logo.setStyleSheet("color: #00FF00; font-size: 24px; font-weight: 800; margin-bottom: 40px; padding-left: 12px; font-family: 'Courier New'; letter-spacing: 2px;")
            btn_style = "QPushButton { background-color: transparent; color: #00FF00; border: none; padding: 15px; text-align: left; font-size: 15px; font-family: 'Courier New'; } QPushButton:hover { background-color: #002200; } QPushButton:checked { background-color: #003300; color: #00FF00; font-weight: bold; border-left: 3px solid #00FF00; }"

        for index, (btn, _) in self.menu_buttons.items():
            btn.setStyleSheet(btn_style)

        self.dash_view.apply_theme_styles()
        self.url_view.apply_theme_styles()
        self.pwd_view.apply_theme_styles()
        self.file_view.apply_theme_styles()
        self.reports_view.apply_theme_styles()
        self.settings_view.apply_theme_styles()
        self.about_view.apply_theme_styles()

    def reload_all_languages(self):
        self.logo.setText(tr("app_title"))
        for index, (btn, key_name) in self.menu_buttons.items():
            btn.setText(tr(key_name))
            
        self.dash_view.retranslate_ui()
        self.url_view.retranslate_ui()
        self.pwd_view.retranslate_ui()
        self.file_view.retranslate_ui()
        self.reports_view.retranslate_ui()
        self.settings_view.retranslate_ui()
        self.about_view.retranslate_ui()
        
        time_str = datetime.now().strftime("%H:%M:%S")
        self.dash_view.append_dynamic_log(f"[{time_str}] [SYSTEM] Settings/Environment matrices updated.")


# =====================================================================
# 5. MODERN SPLASH SCREEN & PIPELINE (Açılış Sistemi)
# =====================================================================

class CyberSplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setFixedSize(550, 320)
        
        # AttributeError veren pencereleri engellemek adına doğrudan yalın bitwise flag kullandık.
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 40, 30, 40)
        
        self.setStyleSheet("QSplashScreen { background-color: #090D14; border: 2px solid #00E5FF; border-radius: 12px; }")
        
        title = QLabel("🛡️ CYBERSHIELD OS")
        title.setStyleSheet("color: #00FF66; font-size: 26px; font-weight: 800; font-family: 'Courier New'; letter-spacing: 3px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        self.status_msg = QLabel("Initializing security kernel cores...")
        self.status_msg.setStyleSheet("color: #9CA3AF; font-size: 14px; font-family: 'Segoe UI'; margin-top: 10px;")
        layout.addWidget(self.status_msg, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("QProgressBar { border: none; background-color: #111927; height: 6px; border-radius: 3px; text-align: transparent; } QProgressBar::chunk { background-color: #00E5FF; border-radius: 3px; }")
        layout.addWidget(self.progress_bar)
        
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading_simulation)
        self.timer.start(15)

    def loading_simulation(self):
        self.counter += 1
        self.progress_bar.setValue(self.counter)
        
        if self.counter == 25:
            self.status_msg.setText("Connecting VirusTotal API secure tunnels...")
        elif self.counter == 55:
            self.status_msg.setText("Synchronizing localized cryptography indices...")
        elif self.counter == 80:
            self.status_msg.setText("Booting interface cockpit matrix...")
        elif self.counter >= 100:
            self.timer.stop()
            self.close()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    splash = CyberSplashScreen()
    splash.show()
    
    while splash.counter < 100:
        app.processEvents()
        time.sleep(0.01)
        
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()