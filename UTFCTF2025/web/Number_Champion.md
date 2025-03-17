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
Bằng cách nào đó lên được gần 3000 
