import time

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

import cv2
import numpy as np
import scipy.fftpack
import base64

#Fungsi Enkripsi Dan Deskripsi--------------------------------------------------------------------

# Buat Kunci RSA
def buat_kunci():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open('private.pem', 'wb') as f:
        f.write(private_key)
    with open('public.pem', 'wb') as f:
        f.write(public_key)

    # print("Public key:", public_key.decode('utf-8'))
    # print("Private key:", private_key.decode('utf-8'))

# Enkripsi Pesan
def enkripsi(pesan):
    buat_kunci()

    start_time = time.time()
    public_key = RSA.import_key(open('public.pem').read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    pesan_enkripsi = cipher_rsa.encrypt(pesan.encode('utf-8'))

    end_time = time.time()
    waktu_enkripsi = end_time - start_time

    print("Encrypted pesan:", pesan_enkripsi)
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

    print("Decrypted pesan:", pesan_dekripsi.decode('utf-8'))
    print("Waktu Komputasi Deskripsi:", waktu_deskripsi)

#Fungsi Steganografi -------------------------------------------------------------------------------------

def embed_message(image_path, message, output_path):

    # Baca gambar
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError("Gambar tidak ditemukan atau format tidak didukung")
    
    # Konversi pesan menjadi biner
    message_bin = ''.join(format(ord(i), '08b') for i in message) + '1111111111111110'
    
    # Dapatkan ukuran gambar
    rows, cols, _ = image.shape
    
    # Variabel untuk melacak posisi pesan
    message_index = 0
    message_length = len(message_bin)
    
    # Sisipkan pesan ke dalam gambar
    for i in range(0, rows, 8):
        for j in range(0, cols, 8):
            if message_index >= message_length:
                break
            
            for k in range(3): # Iterasi melalui setiap channel warna
                if message_index >= message_length:
                    break
                
                # Ambil blok 8x8
                block = image[i:i+8, j:j+8, k]
                if block.shape[0] != 8 or block.shape[1] != 8:
                    continue
                
                # Lakukan DCT pada blok
                dct_block = scipy.fftpack.dct(scipy.fftpack.dct(block.T, norm='ortho').T, norm='ortho')
                
                # Sisipkan bit pesan ke dalam koefisien DCT
                bit = int(message_bin[message_index])
                if (int(dct_block[4, 4]) % 2) != bit:
                    dct_block[4, 4] += (bit - int(dct_block[4, 4]) % 2)
                
                # Lakukan inverse DCT untuk mendapatkan kembali blok gambar
                idct_block = scipy.fftpack.idct(scipy.fftpack.idct(dct_block.T, norm='ortho').T, norm='ortho')
                
                # Klip nilai agar berada dalam rentang [0, 255]
                image[i:i+8, j:j+8, k] = np.clip(idct_block, 0, 255).astype(np.uint8)
                
                message_index += 1

    # Simpan gambar dengan pesan tersembunyi
    cv2.imwrite(output_path, image)

def extract_message(image_path):
    # Baca gambar
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError("Gambar tidak ditemukan atau format tidak didukung")
    
    # Dapatkan ukuran gambar
    rows, cols, _ = image.shape
    
    # Variabel untuk menyimpan pesan dalam bentuk biner
    message_bin = ''
    
    # Ekstrak pesan dari gambar
    for i in range(0, rows, 8):
        for j in range(0, cols, 8):
            for k in range(3): # Iterasi melalui setiap channel warna
                # Ambil blok 8x8
                block = image[i:i+8, j:j+8, k]
                if block.shape[0] != 8 or block.shape[1] != 8:
                    continue
                
                # Lakukan DCT pada blok
                dct_block = scipy.fftpack.dct(scipy.fftpack.dct(block.T, norm='ortho').T, norm='ortho')
                
                # Ekstrak bit dari koefisien DCT
                bit = int(dct_block[4, 4]) % 2
                message_bin += str(bit)
                
                # Periksa akhir pesan
                if message_bin[-16:] == '1111111111111110':
                    break
            else:
                continue
            break
        else:
            continue
        break
    
    # Hapus penanda akhir pesan
    message_bin = message_bin[:-16]
    
    # Konversi biner menjadi string
    message = ''
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i+8]
        if len(byte) == 8:
            message += chr(int(byte, 2))
    
    return message

#eksekusi fungsi------------------------------------------------------------------------------------------

input_gambar = "image.png"
pesan = "Kelompok 4"
output_gambar = "gambar_stegano.png"

pesan_enkripsi = str(enkripsi(pesan))

print("--------------------------------------------")

embed_message(input_gambar, pesan, output_gambar)
pesan_stegano = extract_message(output_gambar)
print("--------------------------------------------")
print(pesan_stegano)
# dekripsi(pesan_stegano)


