import shutil
import os 
import requests
import tkinter as tk
import threading 
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import logging
import re
import json
from datetime import datetime
import time
from typing import Optional
import hmac
import hashlib
import base64
import uuid
import mimetypes 

# --- Application Version ---
APP_VERSION = "3.3.0" 

# -------------------------
# TRANSLATIONS (DA
# -------------------------

LANGUAGES = {
    "English": {
        "settings": "Settings", "theme": "Theme", "bg_col": "Background", "about": "About", 
        "user": "User / Token", "lang": "Language", "clear": "Clear", "upload": "📂 Upload (OCR)", 
        "get_cid": "🔑 Get CID", "check_key": "🔍 Check Key", "copy": "📋 Copy", "bulk": "📁 BULK TXT", 
        "clear_out": "🧹 Clear Output", "refresh": "Refresh", "order_id": "Order ID:", 
        "add": "Add", "balance": "Balance:", "price": "Price:", "input_ph": "Enter IID or Key(s)", 
        "user_lbl": "User:", "msg_input": "Please enter input.", "msg_limit": "Limit Exceeded", 
        "msg_daily": "Daily limit reached", "msg_done": "Done", "msg_copy": "Output copied.", 
        "msg_ocr_up": "Uploading...", "msg_req_cid": "Requesting CID...", "msg_check_key": "Checking..."
    },
    "Chinese (Simplified)": {
        "settings": "设置", "theme": "主题", "bg_col": "背景颜色", "about": "关于", 
        "user": "用户/令牌", "lang": "语言", "clear": "清除", "upload": "📂 上传 (OCR)", 
        "get_cid": "🔑 获取 CID", "check_key": "🔍 查 Key", "copy": "📋 复制", "bulk": "📁 批量 TXT", 
        "clear_out": "🧹 清除输出", "refresh": "刷新", "order_id": "订单号:", 
        "add": "充值", "balance": "余额:", "price": "价格:", "input_ph": "输入 IID 或 Key", 
        "user_lbl": "用户:", "msg_input": "请输入内容。", "msg_limit": "超出限制", 
        "msg_daily": "达到每日限制", "msg_done": "完成", "msg_copy": "已复制。", 
        "msg_ocr_up": "正在上传...", "msg_req_cid": "正在获取 CID...", "msg_check_key": "正在检查..."
    },
    "Vietnamese": {
        "settings": "Cài đặt", "theme": "Chủ đề", "bg_col": "Màu nền", "about": "Giới thiệu", 
        "user": "Người dùng", "lang": "Ngôn ngữ", "clear": "Xóa", "upload": "📂 Tải ảnh (OCR)", 
        "get_cid": "🔑 Lấy CID", "check_key": "🔍 Check Key", "copy": "📋 Sao chép", "bulk": "📁 Hàng loạt", 
        "clear_out": "🧹 Xóa Output", "refresh": "Làm mới", "order_id": "Mã đơn:", 
        "add": "Nạp", "balance": "Số dư:", "price": "Giá:", "input_ph": "Nhập IID hoặc Key", 
        "user_lbl": "Người dùng:", "msg_input": "Vui lòng nhập.", "msg_limit": "Quá giới hạn", 
        "msg_daily": "Đạt giới hạn ngày", "msg_done": "Hoàn tất", "msg_copy": "Đã sao chép.", 
        "msg_ocr_up": "Đang tải lên...", "msg_req_cid": "Đang lấy CID...", "msg_check_key": "Đang kiểm tra..."
    },
    "Thai": {
        "settings": "การตั้งค่า", "theme": "ธีม", "bg_col": "สีพื้นหลัง", "about": "เกี่ยวกับ", 
        "user": "ผู้ใช้", "lang": "ภาษา", "clear": "ล้าง", "upload": "📂 อัปโหลด", 
        "get_cid": "🔑 รับ CID", "check_key": "🔍 ตรวจสอบ", "copy": "📋 คัดลอก", "bulk": "📁 แบบกลุ่ม", 
        "clear_out": "🧹 ล้างผลลัพธ์", "refresh": "รีเฟรช", "order_id": "รหัสคำสั่งซื้อ:", 
        "add": "เพิ่ม", "balance": "ยอดคงเหลือ:", "price": "ราคา:", "input_ph": "ป้อน IID หรือคีย์", 
        "user_lbl": "ผู้ใช้:", "msg_input": "กรุณาป้อนข้อมูล", "msg_limit": "เกินขีดจำกัด", 
        "msg_daily": "ครบกำหนดรายวัน", "msg_done": "เสร็จสิ้น", "msg_copy": "คัดลอกแล้ว", 
        "msg_ocr_up": "กำลังอัปโหลด...", "msg_req_cid": "กำลังขอ CID...", "msg_check_key": "กำลังตรวจสอบ..."
    },
    "Russian": {
        "settings": "Настройки", "theme": "Тема", "bg_col": "Фон", "about": "О нас", 
        "user": "Аккаунт", "lang": "Язык", "clear": "Очистить", "upload": "📂 Скан (OCR)", 
        "get_cid": "🔑 CID", "check_key": "🔍 Проверка", "copy": "📋 Копия", "bulk": "📁 Массово", 
        "clear_out": "🧹 Очистить", "refresh": "Обновить", "order_id": "ID заказа:", 
        "add": "Пополнить", "balance": "Баланс:", "price": "Цена:", "input_ph": "Введите IID или Key", 
        "user_lbl": "Юзер:", "msg_input": "Введите данные.", "msg_limit": "Лимит", 
        "msg_daily": "Дневной лимит", "msg_done": "Готово", "msg_copy": "Скопировано.", 
        "msg_ocr_up": "Загрузка...", "msg_req_cid": "Запрос CID...", "msg_check_key": "Проверка..."
    },
    "Spanish": {
        "settings": "Ajustes", "theme": "Tema", "bg_col": "Fondo", "about": "Info", 
        "user": "Usuario", "lang": "Idioma", "clear": "Borrar", "upload": "📂 Subir", 
        "get_cid": "🔑 CID", "check_key": "🔍 Verificar", "copy": "📋 Copiar", "bulk": "📁 Masivo", 
        "clear_out": "🧹 Limpiar", "refresh": "Actualizar", "order_id": "ID Pedido:", 
        "add": "Añadir", "balance": "Saldo:", "price": "Precio:", "input_ph": "IID o Clave", 
        "user_lbl": "Usuario:", "msg_input": "Entrada inválida.", "msg_limit": "Límite", 
        "msg_daily": "Límite diario", "msg_done": "Hecho", "msg_copy": "Copiado.", 
        "msg_ocr_up": "Subiendo...", "msg_req_cid": "Solicitando...", "msg_check_key": "Verificando..."
    },
    "Portuguese (Brazil)": {
        "settings": "Config", "theme": "Tema", "bg_col": "Fundo", "about": "Sobre", 
        "user": "Usuário", "lang": "Idioma", "clear": "Limpar", "upload": "📂 Upload", 
        "get_cid": "🔑 CID", "check_key": "🔍 Checar", "copy": "📋 Copiar", "bulk": "📁 Massa", 
        "clear_out": "🧹 Limpar", "refresh": "Atualizar", "order_id": "ID Pedido:", 
        "add": "Adic.", "balance": "Saldo:", "price": "Preço:", "input_ph": "IID ou Chave", 
        "user_lbl": "Usuário:", "msg_input": "Entrada inválida.", "msg_limit": "Limite", 
        "msg_daily": "Limite diário", "msg_done": "Feito", "msg_copy": "Copiado.", 
        "msg_ocr_up": "Enviando...", "msg_req_cid": "Solicitando...", "msg_check_key": "Verificando..."
    },
    "Indonesian": {
        "settings": "Pengaturan", "theme": "Tema", "bg_col": "Latar", "about": "Tentang", 
        "user": "Akun", "lang": "Bahasa", "clear": "Hapus", "upload": "📂 Unggah", 
        "get_cid": "🔑 CID", "check_key": "🔍 Cek Key", "copy": "📋 Salin", "bulk": "📁 Massal", 
        "clear_out": "🧹 Bersihkan", "refresh": "Segarkan", "order_id": "ID Pesanan:", 
        "add": "Tambah", "balance": "Saldo:", "price": "Harga:", "input_ph": "Masukan IID/Key", 
        "user_lbl": "User:", "msg_input": "Input tidak valid.", "msg_limit": "Batas", 
        "msg_daily": "Batas harian", "msg_done": "Selesai", "msg_copy": "Disalin.", 
        "msg_ocr_up": "Mengunggah...", "msg_req_cid": "Meminta CID...", "msg_check_key": "Memeriksa..."
    },
    "French": {
        "settings": "Réglages", "theme": "Thème", "bg_col": "Fond", "about": "Info", 
        "user": "Utilisateur", "lang": "Langue", "clear": "Effacer", "upload": "📂 Uploader", 
        "get_cid": "🔑 CID", "check_key": "🔍 Vérifier", "copy": "📋 Copier", "bulk": "📁 Masse", 
        "clear_out": "🧹 Nettoyer", "refresh": "Actualiser", "order_id": "ID Commande:", 
        "add": "Ajouter", "balance": "Solde:", "price": "Prix:", "input_ph": "Entrer IID/Clé", 
        "user_lbl": "User:", "msg_input": "Entrée invalide.", "msg_limit": "Limite", 
        "msg_daily": "Limite jour", "msg_done": "Fait", "msg_copy": "Copié.", 
        "msg_ocr_up": "Envoi...", "msg_req_cid": "Demande CID...", "msg_check_key": "Vérification..."
    },
    "German": {
        "settings": "Einst.", "theme": "Thema", "bg_col": "Hintergr.", "about": "Info", 
        "user": "Benutzer", "lang": "Sprache", "clear": "Löschen", "upload": "📂 Hochladen", 
        "get_cid": "🔑 CID", "check_key": "🔍 Prüfen", "copy": "📋 Kopieren", "bulk": "📁 Massen", 
        "clear_out": "🧹 Leeren", "refresh": "Neu laden", "order_id": "Bestell-ID:", 
        "add": "Laden", "balance": "Guthaben:", "price": "Preis:", "input_ph": "IID oder Key", 
        "user_lbl": "User:", "msg_input": "Ungültig.", "msg_limit": "Limit", 
        "msg_daily": "Tageslimit", "msg_done": "Fertig", "msg_copy": "Kopiert.", 
        "msg_ocr_up": "Hochladen...", "msg_req_cid": "Frage CID...", "msg_check_key": "Prüfung..."
    },
    "Japanese": {
        "settings": "設定", "theme": "テーマ", "bg_col": "背景", "about": "情報", 
        "user": "ユーザー", "lang": "言語", "clear": "クリア", "upload": "📂 アップロード", 
        "get_cid": "🔑 CID取得", "check_key": "🔍 キー確認", "copy": "📋 コピー", "bulk": "📁 一括", 
        "clear_out": "🧹 出力消去", "refresh": "更新", "order_id": "注文ID:", 
        "add": "追加", "balance": "残高:", "price": "価格:", "input_ph": "IIDまたはキー", 
        "user_lbl": "ユーザー:", "msg_input": "入力してください", "msg_limit": "制限超過", 
        "msg_daily": "1日の制限", "msg_done": "完了", "msg_copy": "コピー済", 
        "msg_ocr_up": "アップロード中...", "msg_req_cid": "CID要求中...", "msg_check_key": "確認中..."
    },
    "Korean": {
        "settings": "설정", "theme": "테마", "bg_col": "배경", "about": "정보", 
        "user": "사용자", "lang": "언어", "clear": "지우기", "upload": "📂 업로드", 
        "get_cid": "🔑 CID 받기", "check_key": "🔍 키 확인", "copy": "📋 복사", "bulk": "📁 일괄", 
        "clear_out": "🧹 지우기", "refresh": "새로고침", "order_id": "주문 ID:", 
        "add": "추가", "balance": "잔액:", "price": "가격:", "input_ph": "IID 또는 키", 
        "user_lbl": "사용자:", "msg_input": "입력하세요.", "msg_limit": "초과", 
        "msg_daily": "일일 한도", "msg_done": "완료", "msg_copy": "복사됨", 
        "msg_ocr_up": "업로드 중...", "msg_req_cid": "요청 중...", "msg_check_key": "확인 중..."
    },
    "Turkish": {
        "settings": "Ayarlar", "theme": "Tema", "bg_col": "Arkaplan", "about": "Hakkında", 
        "user": "Hesap", "lang": "Dil", "clear": "Temizle", "upload": "📂 Yükle", 
        "get_cid": "🔑 CID", "check_key": "🔍 Kontrol", "copy": "📋 Kopyala", "bulk": "📁 Toplu", 
        "clear_out": "🧹 Sil", "refresh": "Yenile", "order_id": "Sipariş ID:", 
        "add": "Ekle", "balance": "Bakiye:", "price": "Fiyat:", "input_ph": "IID veya Key", 
        "user_lbl": "Kullanıcı:", "msg_input": "Giriş yapın.", "msg_limit": "Limit", 
        "msg_daily": "Günlük limit", "msg_done": "Tamam", "msg_copy": "Kopyalandı.", 
        "msg_ocr_up": "Yükleniyor...", "msg_req_cid": "İsteniyor...", "msg_check_key": "Kontrol..."
    },
    "Italian": {
        "settings": "Impostazioni", "theme": "Tema", "bg_col": "Sfondo", "about": "Info", 
        "user": "Utente", "lang": "Lingua", "clear": "Pulisci", "upload": "📂 Carica", 
        "get_cid": "🔑 CID", "check_key": "🔍 Verifica", "copy": "📋 Copia", "bulk": "📁 Massa", 
        "clear_out": "🧹 Pulisci", "refresh": "Aggiorna", "order_id": "ID Ordine:", 
        "add": "Agg.", "balance": "Saldo:", "price": "Prezzo:", "input_ph": "IID o Chiave", 
        "user_lbl": "Utente:", "msg_input": "Input non valido.", "msg_limit": "Limite", 
        "msg_daily": "Limite giur.", "msg_done": "Fatto", "msg_copy": "Copiato.", 
        "msg_ocr_up": "Caricamento...", "msg_req_cid": "Richiesta...", "msg_check_key": "Verifica..."
    }
}

# -------------------------
# CONFIGURATION
# -------------------------

GETCID_TOKEN = "" 

# --- FILES ---
LOG_FILE = "cid_app.log"
IID_CACHE_FILE = "last_iid.txt"
IID_CID_SAVE_FILE = "iid_cid_log.txt"
LIMIT_FILE = "key_usage.json" 
TOKEN_FILE = "api_token.txt"      
LICENSE_FILE = "license.key"

# --- API URLS ---
API_GETCID_URL = "http://api.get-cid.com/api/getcid?token={token}&iid={iid}"
API_BALANCE_URL = "http://api.get-cid.com/api/getUserInfo?token={token}"
API_RECHARGE_URL = "http://api.get-cid.com/api/recharge?token={token}&orderid={orderid}"
API_OCR_URL = 'http://api.get-cid.com/api/ocr'
API_KEY_CHECK_URL = "http://api.get-cid.com/api/checkkey?key={key}&token={token}"

OPERATOR_NAME = "Admin"
DAILY_CHECK_LIMIT = 100
MAX_KEYS_PER_PASTE = 10
SALT = b"98813e95123c732fd6e4123584ddc4fe"
DEFAULT_THEME = "Copilot Blue Dark" 
DEFAULT_LANG = "English"

# --- THEMES & COLORS ---
THEMES = {
    "Blue": { "bg": "#e6f0ff", "title_fg": "#003399", "text_bg": "#ffffff", "text_fg": "#000000", "balance_fg": "#006600", "user_fg": "#003399" },
    "Dark": { "bg": "#202020", "title_fg": "#ffffff", "text_bg": "#2b2b2b", "text_fg": "#f0f0f0", "balance_fg": "#66ff66", "user_fg": "#aaaaaa" },
    "Light": { "bg": "#f9f9f9", "title_fg": "#003366", "text_bg": "#ffffff", "text_fg": "#000000", "balance_fg": "#008000", "user_fg": "#333333" },
    "Copilot Blue Dark": { "bg": "#0D253D", "title_fg": "#FFFFFF", "text_bg": "#1D1D2B", "text_fg": "#FFFFFF", "balance_fg": "#D6BCFA", "user_fg": "#E0E0E0" },
}

BG_COLORS = {
    "Default": "Default", "Black": "#000000", "White": "#FFFFFF", "Red (Dark)": "#4a0000",
    "Green (Dark)": "#003300", "Blue (Dark)": "#000033", "Purple": "#2d004d",
    "Orange": "#663300", "Grey": "#333333", "Navy": "#001f3f", "Teal": "#004d40"
}

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# -------------------------
# HELPER FUNCTIONS
# -------------------------

def get_hwid(): return hex(uuid.getnode()).upper().lstrip('0X')

def load_api_token():
    global GETCID_TOKEN
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as f:
                encrypted = f.read().strip()
                hwid = get_hwid()
                # Decrypt using the same HWID
                decrypted = "".join(chr(ord(l) ^ ord(hwid[i % len(hwid)])) for i, l in enumerate(encrypted))
                if decrypted: 
                    GETCID_TOKEN = decrypted
                    return True
        except: 
            pass
    return False

def save_api_token(token):
    global GETCID_TOKEN
    try:
        hwid = get_hwid()
        # Encrypt token using HWID as a XOR key
        encrypted = "".join(chr(ord(l) ^ ord(hwid[i % len(hwid)])) for i, l in enumerate(token.strip()))
        with open(TOKEN_FILE, 'w') as f: 
            f.write(encrypted)
        GETCID_TOKEN = token.strip()
        return True
    except: 
        return False

def get_daily_usage():
    today = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(LIMIT_FILE): return 0
    try:
        with open(LIMIT_FILE, 'r') as f:
            data = json.load(f)
            if data.get("date") == today: return data.get("count", 0)
    except: pass
    return 0

def increment_daily_usage(count=1):
    today = datetime.now().strftime("%Y-%m-%d")
    current = 0
    if os.path.exists(LIMIT_FILE):
        try:
            with open(LIMIT_FILE, 'r') as f:
                data = json.load(f)
                if data.get("date") == today: current = data.get("count", 0)
        except: pass
    new_c = current + count
    try:
        with open(LIMIT_FILE, 'w') as f: json.dump({"date": today, "count": new_c}, f)
    except: pass
    return new_c

def extract_iid_from_image(path):
    if not os.path.exists(path): return None, None, None
    try:
        with open(path, "rb") as f: enc = base64.b64encode(f.read()).decode('utf-8')
        mime, _ = mimetypes.guess_type(path)
        if not mime: mime = "image/jpeg"
        resp = requests.post(API_OCR_URL, json={"token": GETCID_TOKEN, "mime_type": mime, "image_base64": enc}, timeout=50)
        d = resp.json()
        if d.get("status") == "success":
            return re.sub(r"[^0-9\s]", "", d.get("extracted_text", "")).strip(), str(d.get("deduction", "")), str(d.get("api_balance", ""))
        else: raise Exception(d.get("message", "Error"))
    except Exception as e: raise e

def format_iid_blocks(t):
    d = re.sub(r"\D", "", t or "")
    if not d: return ""
    return "-".join([d[i:i+7] for i in range(0, len(d), 7)][:9])

def format_cid_blocks(t):
    d = re.sub(r"\D", "", t or "")
    if not d: return ""
    return "-".join([d[i:i+6] for i in range(0, len(d), 6)][:8])

def check_key_single(key_text):
    try:
        clean = key_text.strip()
        resp = requests.get(API_KEY_CHECK_URL.format(key=clean, token=GETCID_TOKEN), timeout=25)
        if resp.status_code != 200: return f"❌ HTTP {resp.status_code}", None
        d = json.loads(resp.text)
        desc = d.get("prd") or d.get("desc") or "Unknown"
        pid = d.get("PID") or "N/A"
        err = d.get("errorcode") or "N/A"
        time = d.get("check_time") or datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return f"🔑 {clean}\n📝 {desc}\n🆔 {pid}\n⚠️ {err}\n⏰ {time}", d.get("api_balance")
    except Exception as e: return f"❌ {str(e)}", None

def get_cid_formatted(iid):
    try:
        clean = re.sub(r"\D", "", iid or "")
        resp = requests.get(API_GETCID_URL.format(token=GETCID_TOKEN, iid=clean), timeout=20)
        d = resp.json()
        iid_fmt = format_iid_blocks(d.get("iid", clean))
        cid_fmt = format_cid_blocks(d.get("cid", ""))
        stat = d.get("status", "").lower()
        err = d.get("errormsg") or d.get("message")
        cid_line = (err or "Invalid") if stat == "failed" else cid_fmt
        out = []
        if iid_fmt: out.append(f"🔢 IID\n{iid_fmt}")
        if cid_line: out.append(f"🆔 CID\n{cid_line}")
        if d.get("pid"): out.append(f"PID: {d.get('pid')}\nName: {d.get('productName')}")
        return "\n".join(out), iid_fmt, cid_line, d.get("pid"), d.get("productName"), d.get("deduction"), d.get("api_balance"), (err if stat=="failed" else None)
    except Exception as e: return None,None,None,None,None,None,None,str(e)

def get_balance(custom_token=None):
    t = custom_token if custom_token else GETCID_TOKEN
    try:
        r = requests.get(API_BALANCE_URL.format(token=t), timeout=15)
        d = r.json()
        return str(d.get("api_balance","")), str(d.get("api_cid_price","")), str(d.get("user_guid","")), str(d.get("TelegramID","")), None
    except Exception as e: return None,None,None,None,str(e)

def recharge_api_balance(order_id):
    try:
        url = f"http://api.get-cid.com/api/recharge?token={GETCID_TOKEN}&orderid={order_id}"
        resp = requests.get(url, timeout=15)
        return resp.json() # Returns dict like {"status": "success", "message": "..."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def validate_license(enc_key):
    try:
        raw = base64.b64decode(enc_key).decode('utf-8')
        fmt, exp, h_recv = raw.split('|')
        hwid = get_hwid()
        h_calc = hmac.new(SALT, f"{fmt}|{exp}".encode(), hashlib.sha256).hexdigest().upper()
        if h_calc != h_recv: return False, "Integrity Check Failed", None
        h_hwid = hmac.new(SALT, f"{hwid}|{exp}".encode(), hashlib.sha256).hexdigest().upper()
        expect_fmt = "-".join(h_hwid[i:i+4] for i in range(0, 20, 4))
        if fmt != expect_fmt: return False, "HWID Mismatch", None
        if datetime.strptime(exp, "%Y-%m-%d") < datetime.now(): return False, "Expired", exp
        return True, f"Valid until {exp}", exp
    except: return False, "Invalid Format", None

def get_days_remaining():
    """Helper to calculate days left on license"""
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, 'r') as f:
                key = f.read().strip()
                v, _, exp_str = validate_license(key)
                if v and exp_str:
                    exp_date = datetime.strptime(exp_str, "%Y-%m-%d")
                    delta = exp_date - datetime.now()
                    return delta.days
        except:
            pass
    return None

# -------------------------------------
# GUI CLASSES
# -------------------------------------                                             

class LicenseScreen:
    def __init__(self, master):
        self.master = master
        master.title("Activation")
        master.geometry("400x320")
        master.configure(bg="#202B50")
        self.valid = False
        self.hwid = get_hwid()
        tk.Label(master, text="🔐 Activation", font=("Segoe UI", 16, "bold"), bg="#202B50", fg="#66ff66").pack(pady=10)
        tk.Label(master, text="Hardware ID:",bg="#202B50", fg="white",font=("Segoe UI", 12,"bold")).pack()
        tk.Label(master, text=self.hwid, font=("Consolas", 11, "bold"), bg="#333333", fg="white", padx=10, pady=5).pack(pady=5)
        tk.Button(master, text="Copy HWID",font=("Segoe UI", 10,"bold"), bg="#124281", fg="white", command=lambda: [master.clipboard_clear(), master.clipboard_append(self.hwid), messagebox.showinfo("Copied","HWID Copied")]).pack(pady=5, ipadx=10)
        tk.Label(master, text="License Key:", bg="#202B50", fg="white",font=("Segoe UI", 12,"bold")).pack(pady=(15,0))
        self.entry = tk.Entry(master, font=("Consolas", 10), width=45)
        self.entry.pack(pady=5)
        tk.Button(master, text="Activate", font=("Segoe UI", 10, "bold"), bg="#006600", fg="white", command=self.check, width=20).pack(pady=15)

    def check(self):        
        v, m, _ = validate_license(self.entry.get().strip())
        if v:
            with open(LICENSE_FILE, 'w') as f: f.write(self.entry.get().strip())
            self.valid = True
            messagebox.showinfo("Success", m); self.master.destroy()
        else: messagebox.showerror("Error", m)

class TokenLoginScreen:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        master.geometry("400x250")
        master.configure(bg="#202020")
        self.authenticated = False
        tk.Label(master, text="☁️ API Login", font=("Segoe UI", 16, "bold"), bg="#005580", fg="#4da6ff").pack(pady=15)
        tk.Label(master, text="API Token:", font=("Segoe UI", 10), bg="#202020", fg="white").pack(pady=5)
        self.token_entry = tk.Entry(master, font=("Consolas", 11), width=40, show="*")
        self.token_entry.pack(pady=5)
        tk.Button(master, text="Connect", font=("Segoe UI", 10, "bold"), bg="#005580", fg="white", command=self.verify_token, width=20).pack(pady=20)

    def verify_token(self):
        token = self.token_entry.get().strip()
        if not token: return messagebox.showwarning("Input", "Enter token.")
        bal, _, _, _, err = get_balance(token)
        if err: messagebox.showerror("Error", f"Invalid Token.\n{err}")
        else:
            save_api_token(token)
            self.authenticated = True
            messagebox.showinfo("Success", f"Connected!\nBal: {bal}")
            self.master.destroy()

class CIDApp:
    def __init__(self, root):
        self.root = root
        self.init = False
        self.current_lang = DEFAULT_LANG
        self.current_bg = "Default"
        self.current_theme = DEFAULT_THEME
        
    def build(self):
        # --- TITLE BAR UPDATE: Added Days Remaining ---
        days_left = get_days_remaining()
        title_text = f"GET-CID TOOL v{APP_VERSION}"
        if days_left is not None:
            title_text += f" | Days Left: {days_left}"
        self.root.title(title_text)
        
        self.root.geometry("800x600")
        
        # TOP BAR
        self.top = tk.Frame(self.root); self.top.pack(fill="x", padx=10, pady=5)
        self.dt_lbl = tk.Label(self.top, font=("Segoe UI", 10, "bold")); self.dt_lbl.pack(side="left")
        
        # SETTINGS MENU (The "Gear" Icon Button)
        self.btn_settings = tk.Menubutton(self.top, text="⚙", font=("Segoe UI", 14), direction='below')
        self.btn_settings.pack(side="right", padx=10)
        
        # Create Menu Structure
        self.menu_settings = tk.Menu(self.btn_settings, tearoff=0)
        self.btn_settings.config(menu=self.menu_settings)
        
        self.update_settings_menu() # Initial build of menu items

        # TITLE
        self.t_fr = tk.Frame(self.root); self.t_fr.pack(fill="x", pady=5)
        self.t_lbl = tk.Label(self.t_fr, text="GET-CID TOOL", font=("Segoe UI", 20, "bold")); self.t_lbl.pack()
        
        # INPUT
        self.i_fr = tk.Frame(self.root); self.i_fr.pack(pady=5)
        self.entry = tk.Entry(self.i_fr, font=("Segoe UI", 14), width=45, justify="center")
        self.entry.pack(side="left", padx=10)
        self.entry.insert(0, "")
        self.btn_clear_input = ttk.Button(self.i_fr, text="Clear", command=lambda: self.entry.delete(0, tk.END))
        self.btn_clear_input.pack(side="left")
        self.load_iid(); self.ctx_menu(self.entry)
        
        # BUTTONS
        self.b_fr = tk.Frame(self.root); self.b_fr.pack(pady=5)
        ttk.Style().configure("B.TButton", font=("Segoe UI", 10, "bold"))
        
        self.btn_ocr = ttk.Button(self.b_fr, text="Upload", style="B.TButton", command=self.ocr)
        self.btn_ocr.grid(row=0, column=0, padx=5)
        
        self.btn_cid = ttk.Button(self.b_fr, text="Get CID", style="B.TButton", command=self.cid)
        self.btn_cid.grid(row=0, column=1, padx=5)
        
        self.btn_check = ttk.Button(self.b_fr, text="Check Key", style="B.TButton", command=self.check_key)
        self.btn_check.grid(row=0, column=2, padx=5)
        
        self.btn_copy = ttk.Button(self.b_fr, text="Copy", style="B.TButton", command=self.copy)
        self.btn_copy.grid(row=0, column=3, padx=5)
        
        self.btn_bulk = ttk.Button(self.b_fr, text="Bulk", style="B.TButton", command=self.bulk)
        self.btn_bulk.grid(row=0, column=4, padx=5)
        
        # OUTPUT
        self.o_fr = tk.Frame(self.root); self.o_fr.pack(fill="both", expand=True, padx=15, pady=10)
        self.u_lbl = tk.Label(self.o_fr, text=f"User: {OPERATOR_NAME}", font=("Segoe UI", 10, "bold"), anchor="w"); self.u_lbl.pack(fill="x")
        self.txt = tk.Text(self.o_fr, font=("Consolas", 11), height=12); self.txt.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(self.o_fr, command=self.txt.yview); sb.pack(side="right", fill="y"); self.txt.config(yscrollcommand=sb.set)
        self.ctx_menu(self.txt)
        
        # BOTTOM (Footer) - UPDATED SPACING
        self.btm = tk.Frame(self.root); self.btm.pack(fill="x", padx=15, pady=5)
        
        self.btn_clear_out = ttk.Button(self.btm, text="Clear Output", command=lambda: self.txt.delete("1.0", tk.END))
        self.btn_clear_out.pack(side="left")
        
        self.bal = tk.StringVar(value="Balance: --")
        self.lbl_bal = tk.Label(self.btm, textvariable=self.bal, font=("Segoe UI", 10, "bold"))
        self.lbl_bal.pack(side="left", padx=(15, 5))

        self.ded_var = tk.StringVar(value="Price: --")
        self.ded_lbl = tk.Label(self.btm, textvariable=self.ded_var, font=("Segoe UI", 10, "bold"))
        self.ded_lbl.pack(side="left", padx=(0, 10))

        self.btn_refresh = ttk.Button(self.btm, text="Refresh", command=self.refresh_bal)
        self.btn_refresh.pack(side="left")
        
        # --- CHANGED: Removed empty expanding label ---
        # --- CHANGED: Added padx=40 to give it a "slight" gap from the left cluster ---
        self.lbl_oid = tk.Label(self.btm, text="Order ID:")
        self.lbl_oid.pack(side="left", padx=(40, 5))
        
        self.oid = tk.Entry(self.btm, width=25); self.oid.pack(side="left", padx=(0, 5))
        
        self.btn_add = ttk.Button(self.btm, text="Add", command=self.recharge)
        self.btn_add.pack(side="left")
        
        self.apply_theme(None)
        self.update_texts() 
        self.update_time()
        self.refresh_bal(True)
        self.init = True

    # --- MENU HELPERS ---
    def update_settings_menu(self):
        # Clears and rebuilds the menu (useful if language changes)
        L = LANGUAGES[self.current_lang]
        self.menu_settings.delete(0, tk.END)
        
        # Language Submenu
        lang_menu = tk.Menu(self.menu_settings, tearoff=0)
        self.menu_settings.add_cascade(label=L["lang"], menu=lang_menu)
        for lang_key in LANGUAGES.keys():
            lang_menu.add_command(label=lang_key, command=lambda l=lang_key: self.change_language(l))
            
        # Theme Submenu
        theme_menu = tk.Menu(self.menu_settings, tearoff=0)
        self.menu_settings.add_cascade(label=L["theme"], menu=theme_menu)
        for theme_key in THEMES.keys():
            theme_menu.add_command(label=theme_key, command=lambda t=theme_key: self.change_theme(t))
            
        # Background Submenu
        bg_menu = tk.Menu(self.menu_settings, tearoff=0)
        self.menu_settings.add_cascade(label=L["bg_col"], menu=bg_menu)
        for bg_key in BG_COLORS.keys():
            bg_menu.add_command(label=bg_key, command=lambda b=bg_key: self.change_bg(b))
            
        self.menu_settings.add_separator()
        
        # Direct Commands
        self.menu_settings.add_command(label=L["user"], command=self.user_info)
        self.menu_settings.add_command(label=L["about"], command=self.about)

    def change_language(self, lang_name):
        self.current_lang = lang_name
        self.update_texts()
        self.update_settings_menu() # Rebuild menu to update labels inside it

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme(None)

    def change_bg(self, bg_name):
        self.current_bg = bg_name
        self.apply_theme(None)

    def update_texts(self):
        L = LANGUAGES[self.current_lang]
        
        self.btn_clear_input.config(text=L["clear"])
        self.u_lbl.config(text=f"{L['user_lbl']} {OPERATOR_NAME}")
        self.btn_clear_out.config(text=L["clear_out"])
        self.btn_refresh.config(text=L["refresh"])
        self.lbl_oid.config(text=L["order_id"])
        self.btn_add.config(text=L["add"])
        
        self.btn_ocr.config(text=L["upload"])
        self.btn_cid.config(text=L["get_cid"])
        self.btn_check.config(text=L["check_key"])
        self.btn_copy.config(text=L["copy"])
        self.btn_bulk.config(text=L["bulk"])
        
        current = self.entry.get()
        # Reset placeholder if it matches any known placeholder
        for lang in LANGUAGES.values():
            if current == lang["input_ph"]:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, L["input_ph"])
                break
        if not current: self.entry.insert(0, L["input_ph"])
             
        self.refresh_bal(silent=True)

    def about(self):
        messagebox.showinfo("About", f"GET-CID Tool\nVersion {APP_VERSION}\nDeveloped for valid IID activation.")

    # --- ACTIONS ---

    def update_check_log(self, res, bal, index, total):
        # Helper to update UI from main thread
        self.txt.insert(tk.END, f"--- {index+1}/{total} ---\n")
        self.txt.insert(tk.END, res + "\n\n")
        if bal: 
            L = LANGUAGES[self.current_lang]
            self.bal.set(f"{L['balance']} {bal}")

    def check_key(self):
        L = LANGUAGES[self.current_lang]
        raw = self.entry.get().strip()
        if not raw or L["input_ph"] in raw: return messagebox.showwarning("Input", L["msg_input"])

        keys = re.findall(r'[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}', raw)
        if not keys: keys = raw.replace(',', ' ').split()

        if len(keys) == 0: return messagebox.showwarning("Input", L["msg_input"])
        if len(keys) > MAX_KEYS_PER_PASTE: return messagebox.showerror("Error", f"{L['msg_limit']}: {MAX_KEYS_PER_PASTE}")
        
        cur = get_daily_usage()
        if cur + len(keys) > DAILY_CHECK_LIMIT: return messagebox.showerror("Error", f"{L['msg_daily']} ({cur}/{DAILY_CHECK_LIMIT})")

        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, f"{L['msg_check_key']} ({len(keys)})\n\n")
        self.btn_check.config(state="disabled")

        # Background thread function
        def run_check():
            cnt = 0
            for i, key in enumerate(keys):
                res, bal = check_key_single(key)
                # Thread-safe UI update
                self.root.after(0, lambda r=res, b=bal, idx=i: self.update_check_log(r, b, idx, len(keys)))
                cnt += 1
                time.sleep(0.5)
            
            # Final updates on main thread
            self.root.after(0, lambda: self.btn_check.config(state="normal"))
            tot = increment_daily_usage(cnt)
            final_msg = f"*** {L['msg_done']} ({tot}/{DAILY_CHECK_LIMIT}) ***"
            self.root.after(0, lambda: self.txt.insert(tk.END, final_msg))
            self.root.after(0, lambda: self.save_iid(raw))

        threading.Thread(target=run_check, daemon=True).start()

    def cid(self):
        L = LANGUAGES[self.current_lang]
        t = self.entry.get().strip()
        if not t or L["input_ph"] in t: return messagebox.showwarning("Input", L["msg_input"])
        self.txt.delete("1.0", tk.END); self.txt.insert(tk.END, f"{L['msg_req_cid']}\n"); self.root.update()
        r, iid, cid, pid, n, d, b, e = get_cid_formatted(t)
        if e: self.txt.insert(tk.END, f"❌ {e}")
        else:
            self.txt.delete("1.0", tk.END); self.txt.insert(tk.END, r + "\n")
            if b: self.bal.set(f"{L['balance']} {b}")
            if d: self.ded_var.set(f"{L['price']} {d}") 
            if iid and cid:
                with open(IID_CID_SAVE_FILE, "a", encoding="utf-8") as f: f.write(f"🔢 IID\n{iid}\n🆔 CID\n{cid}\nPID: {pid}\n---\n")
        self.save_iid(t)

    def ocr(self):
        L = LANGUAGES[self.current_lang]
        p = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if not p: return
        self.txt.delete("1.0", tk.END); self.txt.insert(tk.END, f"{L['msg_ocr_up']}\n"); self.root.update()
        try:
            iid, d, b = extract_iid_from_image(p)
            self.txt.insert(tk.END, f"✅ IID: {iid}\n")
            if b: self.bal.set(f"{L['balance']} {b}")
            if d: self.ded_var.set(f"{L['price']} {d}")
            self.entry.delete(0, tk.END); self.entry.insert(0, iid); self.save_iid(iid); self.cid()
        except Exception as e: self.txt.insert(tk.END, f"❌ Error: {e}")

    def bulk(self):
        L = LANGUAGES[self.current_lang]
        p = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if not p: return
        with open(p, "r") as f: items = [re.sub(r'\D','',x) for x in f.read().split() if re.sub(r'\D','',x)]
        self.txt.delete("1.0", tk.END); self.txt.insert(tk.END, f"Processing {len(items)} items...\n\n")
        for i, it in enumerate(items):
            self.txt.insert(tk.END, f"--- {i+1}/{len(items)}: {it} ---\n"); self.root.update()
            r, _, _, _, _, d, b, e = get_cid_formatted(it)
            if e: self.txt.insert(tk.END, f"❌ {e}\n\n")
            else: self.txt.insert(tk.END, r + "\n\n")
            if b: self.bal.set(f"{L['balance']} {b}")
            if d: self.ded_var.set(f"{L['price']} {d}")
        messagebox.showinfo(L["msg_done"], "Bulk Complete")

    # --- UI HELPERS ---
    def copy(self): 
        L = LANGUAGES[self.current_lang]
        self.root.clipboard_clear(); self.root.clipboard_append(self.txt.get("1.0", tk.END))
        messagebox.showinfo("Copy", L["msg_copy"])

    def refresh_bal(self, silent=False): 
        L = LANGUAGES[self.current_lang]
        b, d, _, _, e = get_balance()
        if not e: 
            self.bal.set(f"{L['balance']} {b}")
            if d: self.ded_var.set(f"{L['price']} {d}")
        elif not silent: messagebox.showerror("Error", e)

    def user_info(self): 
        # Method to display user balance and GUID
        b, d, g, t, e = get_balance() 
        msg = f"ID: {t}\nGUID: {g}\nBal: {b}" if not e else e 
        if messagebox.askyesno("User Info", f"{msg}\n\nLogout / Change Token?"): 
            if os.path.exists(TOKEN_FILE): 
                os.remove(TOKEN_FILE) 
            self.root.destroy() 

    def recharge(self):
        # Get the Order ID
        oid_txt = self.oid.get().strip()
        if not oid_txt:
            messagebox.showwarning("Input", "Please enter Order ID")
            return

        # Call the API
        resp = recharge_api_balance(oid_txt) 
        
        # Check status
        if resp.get("status") == "success": 
            msg = resp.get("message", "Success")
            deposited = resp.get("deposited", "0")
            new_bal = resp.get("new_api_balance", "")
            
            # Show Success Message with Amount
            full_msg = f"{msg}\n💰 Deposited: {deposited}"
            messagebox.showinfo("Success", full_msg)
            
            # Update Balance in UI immediately
            if new_bal:
                L = LANGUAGES[self.current_lang]
                self.bal.set(f"{L['balance']} {new_bal}")
            else:
                self.refresh_bal() # Fallback refresh
                
            # Clear the input box
            self.oid.delete(0, tk.END)
        else: 
            # Show Error
            err_msg = resp.get("message", "Unknown Error")
            messagebox.showerror("Error", err_msg)
            
    def setup_chart(self):
        pass

    def load_iid(self): 
        if os.path.exists(IID_CACHE_FILE): 
            with open(IID_CACHE_FILE) as f: self.entry.delete(0, tk.END); self.entry.insert(0, f.read().strip())
    def save_iid(self, t): 
        L = LANGUAGES[self.current_lang]
        if L["input_ph"] not in t: 
            with open(IID_CACHE_FILE, "w") as f: f.write(t.strip())
            
    def apply_theme(self, e):
        # Apply theme first
        t = THEMES[self.current_theme]
        
        # Override bg if selected
        final_bg = t["bg"]
        if self.current_bg != "Default" and self.current_bg in BG_COLORS:
            final_bg = BG_COLORS[self.current_bg]

        self.root.config(bg=final_bg); self.top.config(bg=final_bg); self.t_fr.config(bg=final_bg); self.i_fr.config(bg=final_bg)
        self.b_fr.config(bg=final_bg); self.o_fr.config(bg=final_bg); self.btm.config(bg=final_bg)
        
        self.t_lbl.config(bg=final_bg, fg=t["title_fg"])
        self.dt_lbl.config(bg=final_bg, fg=t["balance_fg"])
        self.u_lbl.config(bg=final_bg, fg=t["user_fg"])
        self.txt.config(bg=t["text_bg"], fg=t["text_fg"])
        self.ded_lbl.config(bg=final_bg, fg=t["balance_fg"])
        
        self.lbl_oid.config(bg=final_bg, fg=t["title_fg"])
        self.lbl_bal.config(bg=final_bg, fg=t["balance_fg"])
        self.btn_settings.config(bg=final_bg, fg=t["title_fg"], activebackground=final_bg)

    def update_time(self): self.dt_lbl.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S")); self.root.after(1000, self.update_time)
    def ctx_menu(self, w):
        m = tk.Menu(w, tearoff=0); m.add_command(label="Copy", command=lambda: w.event_generate("<<Copy>>"))
        m.add_command(label="Paste", command=lambda: w.event_generate("<<Paste>>"))
        w.bind("<Button-3>", lambda e: m.tk_popup(e.x_root, e.y_root))

    def run(self):
        if self.init: self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk(); root.withdraw()
    auth = False
    if os.path.exists(LICENSE_FILE):
        try: 
            if validate_license(open(LICENSE_FILE).read().strip())[0]: auth = True
        except: pass
    if not auth:
        w = tk.Toplevel(root); l = LicenseScreen(w); root.wait_window(w)
        if l.valid: auth = True
    if auth:
        tok_auth = False
        if load_api_token(): tok_auth = True
        else:
            wt = tk.Toplevel(root); ts = TokenLoginScreen(wt); root.wait_window(wt)
            if ts.authenticated: tok_auth = True
        if tok_auth: app = CIDApp(root); app.build(); root.deiconify(); app.run()
        else: root.destroy()
    else: root.destroy()