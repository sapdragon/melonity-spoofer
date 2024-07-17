import os
from pathlib import Path
import zlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


key = b"00000000qwemelox"
header = b"\xA7\x0D\x0D\x0A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

def decrypt_file(input_path: Path, output_path: Path) -> None:
    with input_path.open("rb") as en_f, output_path.open("wb") as de_f:
        encrypted_data = en_f.read()
        iv, ciphertext = encrypted_data[:16], encrypted_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

        plaintext = zlib.decompress(decrypted_data)
        de_f.write(header + plaintext)

def process_directory(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_path in input_dir.glob("*.encrypted"):
        output_path = output_dir / file_path.stem
        print(f"Decrypting {file_path.name}...")
        decrypt_file(file_path, output_path)

    print("Decryption completed.")

if __name__ == "__main__":
    input_directory = Path(r"MelonitySpoofer.exe_extracted\PYZ-01.pyz_extracted")
    output_directory = Path(r"decrypted_files")
    process_directory(input_directory, output_directory)