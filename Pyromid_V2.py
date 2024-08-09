# Install cryptofuzz & colorthon
# pip install pycryptodome
# pip install colorthon

import os
import random
import time
import threading
from Crypto.Hash import RIPEMD160
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Util import number
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
    """Compute RIPEMD-160 hash of the given data."""
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
    # Convert hex private key to integer
    priv_key = number.bytes_to_long(bytes.fromhex(hexed))

    # Create ECC key object
    key = ECC.construct(curve='P-256', d=priv_key)
    pub_key = key.public_key().export_key(format='DER')[4:]  # Remove the first byte

    # Perform SHA256 followed by RIPEMD160 hashing
    sha256_hash = SHA256.new(pub_key)
    ripemd160_hash = RIPEMD160.new()
    ripemd160_hash.update(sha256_hash.digest())
    addr = ripemd160_hash.digest()

    # Return address based on compression choice
    if compress:
        # Convert to Ethereum address (prepend with '0x' and pad to 40 hex chars)
        return '0x' + addr.hex()[:40]
    else:
        # Uncompressed address (not standard in Ethereum, but here for completeness)
        return '0x' + addr.hex()

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
            print(f"[{tm}][Total: {z} Check: {z * 2}] #Found: {wf} ", end="\r")

if __name__ == '__main__':
    t = threading.Thread(target=main_check)
    t.start()
    t.join()
