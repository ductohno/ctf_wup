# Description
```
The number 1 player in this game, geopy hit 3000 elo last week. I want to figure out where they train to be the best.

Flag is the address of this player (according to google maps), in the following format all lowercase:

utflag{<street-address>-<city>-<zip-code>}

For example, if the address is 110 Inner Campus Drive, Austin, TX 78705, the flag would be utflag{110-inner-campus-drive-austin-78705}

By Samintell (@Samintell on discord)

https://numberchamp-challenge.utctf.live/
```

# Analyze

![image](https://github.com/user-attachments/assets/f73c616b-02d1-42b2-a075-48d6dfe87c57)

Khi ta vào web, trong phần `<script>`, 1 vài endpoint đã lộ ra, cụ thể mình sẽ trình bày chi tiết dưới đây:

- `/match?uuid=${userUUID}&lat=${lat}&lon=${lon}`: endpoint này cho phép mình tìm kiếm đối thủ có elo tương đương, và đo khoảng cách dựa trên kinh độ (lat), và vĩ độ (lon)

- `/battle?uuid=${userUUID}&opponent=${opponentUUID}&number=${e}`: endpoint cho phép thực hiện đối đầu. Mình sẽ đưa ra số dự đoán, nếu điểm bên nào cao hơn thì bên đó thắng. Khi dùng endpoint này, mình sẽ chắc chắn thua do đối thủ luôn lấy số dự đoán của mình cộng thêm 1 số nào đó, để trở thành số dự đoán của bot.

- `/register?lat=${lat}&lon=${lon}`: 1 profile với uuid ngẫu nhiên sẽ được gen ra cho mình

Lúc này, hãy chú ý vào description. Ta cần tìm được user tên là `geopy` với mức elo là 3000. Do đó, ta cần phải đạt được elo tiệm cận 3000 thì mới tìm được geopy. 

Tiếp theo, nhìn vào `/battle`, ta thấy rằng mình hoàn toàn có thể thao túng vị trí uuid của mình và đối thủ hoặc có thể sử dụng luôn uuid của đối thủ. Vậy idea sẽ là rút sạch elo 1 bên, sau đó là ta lấy uuid của bên thắng. Cứ như vậy là có 1 uuid tiệm cận 3000 elo.

Khi dùng match, server sẽ hiển thị ra khoảng cách giữa mình và đối thủ bao xa, dựa trên kinh độ và vĩ độ mình nhập. Do đó, ta hoàn toàn có thể bruteforce ra vị trí chính xác của 1 user nào đó mà ta muốn.

### Idea: 
Dựa vào ý tưởng trên, lên được 3000 điểm, sau đó bruteforce địa điểm của người chơi geopy để ra kinh độ, vĩ độ. Tìm kiếm trên google map và nhập flag.

# Exploit

Trước tiên ta chọn 1 người chơi gen ra từ `/register`:

![image](https://github.com/user-attachments/assets/dd08e0e1-32e3-4762-a51c-dc504cfab3e7)

Tiếp theo chọn 1 đối thủ:

![image](https://github.com/user-attachments/assets/4316fa60-dbbb-42d1-9c01-c42b546733a2)

Như đã nói, ta sẽ thua và luôn tụt elo:

![image](https://github.com/user-attachments/assets/0132b09f-f603-4967-85ed-060f0234e71b)

Giờ thì buff cho opponent thôi

![image](https://github.com/user-attachments/assets/87a1bb7a-1e2b-4b5c-9e60-0890a1b686ca)

Đối thủ đã được cộng thêm 1000 elo, cứ làm như thế cho đến khi ta tìm được người chơi geopy

![image](https://github.com/user-attachments/assets/145f081d-5c22-4054-9b99-51fff94ab4a5)

Here we go, bây giờ ta chỉ việc bruteforce kinh độ với vĩ độ thôi

Sau khi hồi bruteforce chán chê, mình đã tìm được gần như là chính xác tọa độ cần tìm

![image](https://github.com/user-attachments/assets/507b9cc3-f0d9-4e05-ac78-a4530db21748)

Đây là tọa độ trên gg map:

https://www.google.com/maps/place/39%C2%B056'25.4%22N+82%C2%B059'48.1%22W/@39.9404133,-82.99695,21z/data=!4m5!3m4!4b1!8m2!3d39.9403889!4d-82.9966944?hl=vi-VN&entry=ttu&g_ep=EgoyMDI1MDMxMi4wIKXMDSoASAFQAw%3D%3D


Từ đó ta có flag là

# Flag:
utflag{1059-s-high-st-columbus-43206}
