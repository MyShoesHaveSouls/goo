# Install cryptofuzz & colorthon
# pip install pycryptodome
# pip install colorthon

import os
import random
import time
import threading
from Crypto.Hash import RIPEMD160
from colorthon import Colors

# Define color codes
RED = Colors.RED
GREEN = Colors.GREEN
YELLOW = Colors.YELLOW
CYAN = Colors.CYAN
WHITE = Colors.WHITE
RESET = Colors.RESET

MAX_PRIVATE_KEY = 2**256 - 1  # Example maximum private key value

def ripemd160_hash(data):
    h = RIPEMD160.new()
    h.update(data)
    return h.digest()

def get_clear():
    """Clear the terminal screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def key_gen(size):
    """Generate a random private key of the specified size."""
    k = "".join(random.choice('0123456789abcdef') for _ in range(size))
    if int(k, 16) < MAX_PRIVATE_KEY:
        return k
    else:
        return key_gen(size)

def hex_to_addr(hexed, compress):
    """Convert a hexadecimal private key to an Ethereum address."""
    # Placeholder for address conversion using your own implementation
    pass

def rich_loader(filename):
    """Load addresses from a file into a set."""
    with open(filename, 'r') as file:
        return set(line.strip() for line in file)

def get_header(rich_file, loads, found):
    """Display the header and current status."""
    get_clear()
    output = f"""
{YELLOW}\t██████╗ ██╗   ██╗██████╗  ██████╗ ███╗   ███╗██╗██████╗ {RESET}
{YELLOW}\t██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗████╗ ████║██║██╔══██╗{RESET}
{YELLOW}\t██████╔╝ ╚████╔╝ ██████╔╝██║   ██║██╔████╔██║██║██║  ██║{RESET}
{YELLOW}\t██╔═══╝   ╚██╔╝  ██╔══██╗██║   ██║██║╚██╔╝██║██║██║  ██║{RESET}
{YELLOW}\t██║        ██║   ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║██████╔╝{RESET}
{YELLOW}\t╚═╝        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═════╝ {RESET}
{RED}╔═╗╦═╗╔═╗╔═╗╦═╗╔═╗╔╦╗╔╦╗╔═╗╦═╗{RESET}  {WHITE}╔╦╗╔╦╗╔╦╗╦═╗╔═╗╔═╗ ╔═╗╔═╗╔╦╗{RESET}
{RED}╠═╝╠╦╝║ ║║ ╦╠╦╝╠═╣║║║║║║║╣ ╠╦╝{RESET}  {WHITE}║║║║║║ ║║╠╦╝╔═╝╠═╣ ║  ║ ║║║║{RESET}
{RED}╩  ╩╚═╚═╝╚═╝╩╚═╩ ╩╩ ╩╩ ╩╚═╝╩╚═{RESET}  {WHITE}╩ ╩╩ ╩═╩╝╩╚═╚═╝╩ ╩o╚═╝╚═╝╩ ╩{RESET}
{RED}➜{RESET} {WHITE}BOOMBOX {RESET}{CYAN}v2 {RESET}Ⓟ{GREEN} Powered By CryptoFuzz - Exclusive MMDRZA.COM{RESET}
{RED}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬{RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Import Rich File :{RESET}{CYAN} {rich_file}                {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Method Generated :{RESET}{CYAN} Random Without Repeat.    {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Address Type     :{RESET}{CYAN} Compressed / Uncompressed.{RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Max Decimal (HEX):{RESET}{CYAN} {MAX_PRIVATE_KEY}         {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Result Checked   :{RESET}{CYAN} {loads}                   {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Matched Address  :{RESET}{CYAN} {found}                   {RESET}
"""
    print(output)

def main_check():
    global z, wf
    target_file = 'Rich.txt'
    targets = rich_loader(target_file)
    z = 0
    wf = 0
    lg = 0
    get_header(rich_file=target_file, loads=lg, found=wf)
    while True:
        z += 1
        private_key = key_gen(64)
        # Compress address
        compress_addr = hex_to_addr(private_key, True)
        # Uncompress address
        uncompress_addr = hex_to_addr(private_key, False)
        lct = time.localtime()
        if str(compress_addr) in targets:
            wf += 1
            with open('Found.txt', 'a') as file:
                file.write(f"Compressed Address: {compress_addr}\n"
                           f"Private Key: {private_key}\n"
                           f"DEC: {int(private_key, 16)}\n"
                           f"{'-' * 66}\n")
        elif str(uncompress_addr) in targets:
            wf += 1
            with open('Found.txt', 'a') as file:
                file.write(f"Uncompressed Address: {uncompress_addr}\n"
                           f"Private Key: {private_key}\n"
                           f"DEC: {int(private_key, 16)}\n"
                           f"{'-' * 66}\n")
        elif int(z % 100000) == 0:
            lg += 100000
            get_header(rich_file=target_file, loads=lg, found=wf)
            print(f"Generated: {lg} (SHA-256 - HEX) ...")
        else:
            tm = time.strftime("%Y-%m-%d %H:%M:%S", lct)
