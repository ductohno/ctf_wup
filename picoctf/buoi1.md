# 1. Binary search: (easy)
 - Thuật toán binary search, từ 1 day số có n phần tử chia tử, lấy phần tử 1+n rồi /2 , chọn từ phần từ đó, nếu hiện lower thì tiếp tục chọn từ 1 đến (1+n)/2 và ngược lại đến higher, cứ như thế cho đến lần thứ 10 ta sẽ ra được số chính xác.
 - Lần chạy này
500
250
248
247 <- kết quả: Congratulations! You guessed the correct number: 247
Here's your flag: picoCTF{g00d_gu355_6dcfb67c}
246
242
234
218
187
125

# 2. Verify: (easy)
- Bài này có cho hết tất cả các tool và gợi ý cách làm là xài hàm sha256sum tất cả các file và grep cái checksum.
- Payload: sha256sum * | grep "fba9f49bf22aa7188a155768ab0dfdc1f9b86c47976cd0f7c9003af2e20598f7"
- Kết quả: fba9f49bf22aa7188a155768ab0dfdc1f9b86c47976cd0f7c9003af2e20598f7  87590c24
- Sau đó chạy: ./decrypt.sh files/87590c24
- Flag: picoCTF{trust_but_verify_87590c24}
# 3. First grep: (easy)
- Bài cho ta 1 file+ tên first grep, tải về xong grep thôi.
- Payload: cat file | grep "pico"
- Flag: picoCTF{grep_is_good_to_find_things_f77e0797}
# 4. Obedient cat: (easy)
- Download file đầu bài cho về, cat file đó và ta có flag:
- Flag: picoCTF{s4n1ty_v3r1f13d_f28ac910}
# 5. nice netcat ...(easy)
- Bài cho ta 1 link netcat, khi vào link ta thấy 1 dãy các số và bài gợi ý cho ta đó là ascii
- Hướng làm: chuyển dãy số đó vào 1 file xong đó xài công cụ giải max ascii của Linux ( netcat < file ), xong đó lên cyberchef giải mã (to decimal).
- Flag: picoCTF{g00d_k1tty!_n1c3_k1tty!_5fb5e51d}

