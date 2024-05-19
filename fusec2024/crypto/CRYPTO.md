# Đề bài:
![Screenshot (408)](https://github.com/ductohno/ctf_wup/assets/152991010/ec275eca-87d1-4462-a0c2-fcc6d6bba5e9)
## Chuỗi mã hóa:
```
['159.96.34.204', '136.182.188.58', '155.20.31.30', '12.234.113.15', '153.170.118.69', '189.152.240.17', '180.27.111.161', '87.205.101.118', '45.1.136.2', '122.3.3.3']
```
## Code:
```
import socket
import struct

def cipher(k, d):
    S = list(range(256))
    j = 0
    o = []
    for i in range(256):
        j = (j + S[i] + k[i % len(k)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for c in d:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        o.append(c ^ S[(S[i] + S[j]) % 256])
    return bytearray(o)

def encr(pt, k):
    ed = cipher(k, pt.encode('utf-8'))
    padding_length = (4 - len(ed) % 4) % 4
    ed += bytes([padding_length] * padding_length)
    ipa = d2ip(ed)
    return ipa

def d2ip(d):
    ipa = []
    for i in range(0, len(d), 4):
        pd = d[i:i+4]
        if len(pd) < 4:
            pd += b'\x00' * (4 - len(pd))
        ip = socket.inet_ntoa(struct.pack('!I', int.from_bytes(pd, byteorder='big')))
        ipa.append(ip)
    return ipa

def main():
    key = bytearray('supersecretkey', 'utf-8')
    plaintext = "hiyou"
    ipa = encr(plaintext, key)
    print("IPv4 Encoded Data:", ipa)

if __name__ == "__main__":
    main()
```
Let chatgpt do it for u
# Decode by chatgpt:
```
import socket
import struct

def cipher(k, d):
    S = list(range(256))
    j = 0
    o = []
    for i in range(256):
        j = (j + S[i] + k[i % len(k)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for c in d:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        o.append(c ^ S[(S[i] + S[j]) % 256])
    return bytearray(o)

def ip2d(ip_list):
    d = bytearray()
    for ip in ip_list:
        packed_ip = socket.inet_aton(ip)
        d.extend(packed_ip)
    padding_length = d[-1]
    if padding_length < 4:
        d = d[:-padding_length]
    return d

def decr(ipa, k):
    ed = ip2d(ipa)
    pt = cipher(k, ed).decode('utf-8')
    return pt

def main():
    key = bytearray('supersecretkey', 'utf-8')
    ipa = ['159.96.34.204', '136.182.188.58', '155.20.31.30', '12.234.113.15', '153.170.118.69', '189.152.240.17', '180.27.111.161', '87.205.101.118', '45.1.136.2', '122.3.3.3']  # example of encoded IPs
    plaintext = decr(ipa, key)
    print("Decrypted plaintext:", plaintext)

if __name__ == "__main__":
    main()
```
## Flag:
```
FUSec{howdyiamnowinyourhanddecrypted}
```

