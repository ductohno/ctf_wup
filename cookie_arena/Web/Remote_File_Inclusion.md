# Dựa vào write up:
https://forum.cookiearena.org/t/web-upload-file-via-url-remote-file-inclusion-rfi-lfi/171
# Đề Bài:
![Screenshot (421)](https://github.com/ductohno/ctf_wup/assets/152991010/9a35ee3f-1a3d-40c3-8b7a-37ed97c716b0)

Ta có 1 link web, vào thì ta thấy:

![Screenshot (423)](https://github.com/ductohno/ctf_wup/assets/152991010/238c79ca-30d2-45ab-a33e-9adef6d3570a)

## Phân tích
- Ta có 1 parameter là file, thay dổi giá trị của nó sẽ nhảy sang file khác trong server
- Đầu bài yêu cầu ta tìm ra phpinfo trước, vậy nên ta sẽ sử dụng dirsearch để xác định làm cách nào để vô được phpinfo()
- Ta cần check xem liệu allow_url_include liệu có bật hay không, nếu bật tức là sẽ có vuln
- Tác giả bài wup trên bảo nhớ check thêm file_upload xem có bật ko, nếu bật ta có thể dùng nó để RCE

Tiếp theo ta cần tìm hiểu về Remote File Inclusion
# Remote File Inclusion (RFI):
- Vuln này xảy ra khi có parameter hệ thống ko lọc trước khi upload lên, dẫn đến kẻ xấu có tận dụng điều đó để gửi những url độc hại, từ đó chiếm quyền kiểm soát server
- Do đó ta hoàn toàn có thể làm như CSRF, sử dụng file:///etc/passwd để test vuln
- Thường được so sánh với Local File Inclusion, 1 lỗ hổng khá tương tự
- Còn gì sau này tìm dc maybe viết vô đây
- Khi khai thác RFI, nên tập trung tìm các file url của hệ thống
- Hiện tại ta biết 2 loại chính là file+ địa chỉ file và data, data sẽ bắt đầu bằng loại data, thông thường là data://text/plain; xong đó là loại data, dễ nhất thì base64 và cuối cùng là câu lệnh cần thực thi ở dạng base64
- Ví dụ 1 payload cho data: data://text/plain;base64,PD9waHAgZWNobyBgY2QgLi47bHMgLWxhYDsgPz4=
# Exploit:
Trước hết ta sử dụng dirsearch để truy ra url của phpinfo() theo như hint:

![Screenshot (424)](https://github.com/ductohno/ctf_wup/assets/152991010/10f5ff7f-90fd-456a-bfd2-5d1530b37950)

Chính xác thứ ta cần tìm rồi, tiếp theo thì đọc thông tin, và thấy rằng giống như trên phân tích

Exploit time, trước tiên hãy thử payload: ?file=file:///etc/passwd

![Screenshot (425)](https://github.com/ductohno/ctf_wup/assets/152991010/6545fb54-eb1e-49de-abb8-8c1abc66a275)

Đến lúc dùng payload trong wup rồi: data://text/plain;base64,PD9waHAgZWNobyBgY2QgLi47bHMgLWxhYDsgPz4= (có vẻ như server dùng phiên bản php cũ, do đó không nhận ${} )

![Screenshot (426)](https://github.com/ductohno/ctf_wup/assets/152991010/bd912c02-3733-4337-8fbf-55c7fe016fa5)

Cat the flag time:

![Screenshot (427)](https://github.com/ductohno/ctf_wup/assets/152991010/0ac16aa2-c68e-4360-8a0a-0e782a3535cd)

# Flag:
CHH{pHp_A11Ow_url_INCLud3_cb8aad5e79829ddb533274b086c2d2dc}


