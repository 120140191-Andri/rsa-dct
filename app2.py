import time
import cv2
import numpy as np
import scipy.fftpack
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Fungsi Enkripsi Dan Deskripsi--------------------------------------------------------------------

# Buat Kunci RSA
def buat_kunci():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open('private.pem', 'wb') as f:
        f.write(private_key)
    with open('public.pem', 'wb') as f:
        f.write(public_key)

# Enkripsi Pesan
def enkripsi(pesan):
    buat_kunci()

    start_time = time.time()
    public_key = RSA.import_key(open('public.pem').read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    pesan_enkripsi = cipher_rsa.encrypt(pesan.encode('utf-8'))

    end_time = time.time()
    waktu_enkripsi = end_time - start_time

    print("Enkripsi pesan:", pesan_enkripsi)
    print("Waktu Komputasi Enkripsi:", waktu_enkripsi)

    return pesan_enkripsi

# Dekripsi pesan
def dekripsi(pesan_enkripsi):
    start_time = time.time()

    private_key = RSA.import_key(open('private.pem').read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    pesan_dekripsi = cipher_rsa.decrypt(pesan_enkripsi)

    end_time = time.time()
    waktu_deskripsi = end_time - start_time

    print("Dekripsi pesan:", pesan_dekripsi.decode('utf-8'))
    print("Waktu Komputasi Deskripsi:", waktu_deskripsi)

    return pesan_dekripsi.decode('utf-8')

# Fungsi Steganografi -------------------------------------------------------------------------------------

# Fungsi untuk mengubah byte menjadi representasi biner
def byte_to_bin(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)

# Fungsi untuk mengubah biner menjadi byte
def bin_to_byte(bin_data):
    return bytes(int(bin_data[i:i+8], 2) for i in range(0, len(bin_data), 8))

# Embed pesan ke dalam gambar
def embed_message(image_path, message, output_path):
    # Baca gambar
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError("Gambar tidak ditemukan atau format tidak didukung")

    # Konversi pesan menjadi biner
    message_bin = byte_to_bin(message) + '1111111111111110'  # Tambahkan penanda akhir pesan
    
    # Dapatkan ukuran gambar
    rows, cols, _ = image.shape
    
    # Variabel untuk melacak posisi pesan
    message_index = 0
    message_length = len(message_bin)
    
    # Sisipkan pesan ke dalam gambar
    for i in range(rows):
        for j in range(cols):
            if message_index >= message_length:
                break
            
            pixel = image[i, j]
            for k in range(3):  # Iterasi melalui setiap channel warna
                if message_index >= message_length:
                    break
                pixel[k] = (pixel[k] & 0xFE) | int(message_bin[message_index])
                message_index += 1
            image[i, j] = pixel
        if message_index >= message_length:
            break

    # Simpan gambar dengan pesan tersembunyi
    cv2.imwrite(output_path, image)

# Ekstrak pesan dari gambar
def extract_message(image_path):
    # Baca gambar
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError("Gambar tidak ditemukan atau format tidak didukung")

    # Variabel untuk menyimpan pesan dalam bentuk biner
    message_bin = ''
    
    # Dapatkan ukuran gambar
    rows, cols, _ = image.shape
    
    # Ekstrak pesan dari gambar
    for i in range(rows):
        for j in range(cols):
            pixel = image[i, j]
            for k in range(3):  # Iterasi melalui setiap channel warna
                message_bin += str(pixel[k] & 1)
                if message_bin[-16:] == '1111111111111110':
                    break
            if message_bin[-16:] == '1111111111111110':
                break
        if message_bin[-16:] == '1111111111111110':
            break

    # Hapus penanda akhir pesan
    message_bin = message_bin[:-16]

    # Konversi biner menjadi byte
    message_bytes = bin_to_byte(message_bin)
    
    return message_bytes

# Eksekusi fungsi------------------------------------------------------------------------------------------

input_gambar = "image.png"
pesan = "Kelompok 45"
output_gambar = "gambar_stegano.png"

print("--------------------------------------------")

pesan_enkripsi = enkripsi(pesan)
print("--------------------------------------------")
embed_message(input_gambar, pesan_enkripsi, output_gambar)
pesan_stegano = extract_message(output_gambar)
dekripsi(pesan_stegano)
