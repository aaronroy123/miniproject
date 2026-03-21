import base64
import json
import os
from cryptography.hazmat.primitives.asymmetric import ec

def encode_base64_url(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def generate_vapid_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    private_numbers = private_key.private_numbers()
    d = private_numbers.private_value
    private_key_bytes = d.to_bytes((d.bit_length() + 7) // 8, byteorder='big')
    
    public_key = private_key.public_key()
    public_numbers = public_key.public_numbers()
    x = public_numbers.x.to_bytes(32, byteorder='big')
    y = public_numbers.y.to_bytes(32, byteorder='big')
    public_key_bytes = b'\x04' + x + y
    
    return {
        "private_key": encode_base64_url(private_key_bytes),
        "public_key": encode_base64_url(public_key_bytes)
    }

if __name__ == "__main__":
    keys = generate_vapid_keys()
    os.makedirs('data', exist_ok=True)
    with open('data/vapid.json', 'w') as f:
        json.dump(keys, f, indent=4)
    print("VAPID keys saved to data/vapid.json!")
