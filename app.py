import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

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

    print("Public key:", public_key.decode('utf-8'))
    print("Private key:", private_key.decode('utf-8'))

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
    dekripsi(pesan_enkripsi)

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



enkripsi('hello 123')
