Đề bài:

![Screenshot (342)](https://github.com/ductohno/ctf_wup/assets/152991010/3fc1aea9-fc22-436a-a4fa-26b6f8d1f198)

Truy cập vô link thôi:


![Screenshot (343)](https://github.com/ductohno/ctf_wup/assets/152991010/bc69872d-f6c1-4467-8ebf-2d0d4866d132)

I don't see anything boi :)

Có vẻ như khi ta bấm vào 1 mục bất kì, chả hạn home, thì url trả về /#home

Đầu bài ko cho bruteforce, cụ thể là xích DIRBUSTER, 1 tool bruteforce các thư mục trong server

=> Từ 2 giữ kiện trên, ta có thể đoán phần nào đó là ta sẽ ơhải làm cách nào đó để biết toàn bộ thư mục trong server, có vẻ như command injection là khả thi nhất.

Thử tiếp tục khai thác xem sao, ta thấy có 3 bức ảnh, nếu dán vô url sẽ dẫn đến bức ảnh đó

![Screenshot (344)](https://github.com/ductohno/ctf_wup/assets/152991010/d7c9e3ed-52e5-4137-9c74-4cca6efea114)

Ta có thể điều chỉnh kích thước thông qua url, ở đây kích thước ảnh là 300x494, nếu bạn thử thay đổi ảnh theo kích thước khác thì kích thước sẽ thay đổi theo ý muốn của bạn.

Thử làm gì đó với parameter này xem

Thay vì nhập 1 giá trị bình thường ví dụ như 300x494, hãy thử thêm 7749 râu ria xem, sau khi thử rất nhiều thì nó xuất hiện ra 1 bảng lỗi khá là đáng nghi:

![Screenshot (345)](https://github.com/ductohno/ctf_wup/assets/152991010/a9b520b4-4eb9-4a5c-aea2-356a20de9176)

bin/sh ư, có vẻ như là 1 lệnh hệ thống, command injection riel, nhưng có vẻ đã bị filter bởi 1 dấu !, vậy hãy thêm 1 dấu ; vào sau, giả sử như 300x494;ls; thì ta có

![Screenshot (347)](https://github.com/ductohno/ctf_wup/assets/152991010/c3d7787b-5566-4417-9ae8-9c66506eeeb6)

Vậy là đã rõ, sửa ls thành cat flag.txt mà lấy flag thôi

![Screenshot (339)](https://github.com/ductohno/ctf_wup/assets/152991010/5cde3f6a-5d4e-4f64-be9e-a9bb9baa7ac6)

Flag là: UMASS{B4S1C_CMD_INJ3CTI0N}

Cách khác: có thể thử dán: ls%20%3E%262%3Bpp ( tương đương là ls >%2;pp ) => nó sẽ hiện đáp án ko cần f12

![Screenshot (349)](https://github.com/ductohno/ctf_wup/assets/152991010/71f1405e-2a67-4dcd-b921-508e0fe55bc2)


