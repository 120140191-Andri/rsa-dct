from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

# Buat Kunci RSA
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

print("Public key:", public_key.decode('utf-8'))
print("Private key:", private_key.decode('utf-8'))

# Enkripsi Pesan
pesan = "Kelompok 4"
public_key = RSA.import_key(public_key)
cipher_rsa = PKCS1_OAEP.new(public_key)
pesan_enkripsi = cipher_rsa.encrypt(pesan.encode('utf-8'))

print("Encrypted pesan:", pesan_enkripsi)

# Dekripsi pesan
private_key = RSA.import_key(private_key)
cipher_rsa = PKCS1_OAEP.new(private_key)
pesan_dekripsi = cipher_rsa.decrypt(pesan_enkripsi)

print("Decrypted pesan:", pesan_dekripsi.decode('utf-8'))
