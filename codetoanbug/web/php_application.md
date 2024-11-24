# Đề bài: 
![Screenshot 2024-10-14 075705](https://github.com/user-attachments/assets/6941666f-bbeb-43b5-86af-fa8d17c8c4e1)

# Phân tích:
- Nhìn vào source code, ta thấy được 1 vài điều:

### Debug:
```
if (isset($_GET['debug'])) {
    highlight_file(__FILE__);
}
```
- Đây là đoạn code nếu parameter debug có tồn tại trên url, thì show source ra. Cơ mà do author khi lấy bài từ bluecyber về đã cho cả source nên đoạn này ko cần lắm
### Filter:
```
function fil($str)
{
    return str_replace("BlueCyber", "BC", $str);
}
```
- Đoạn này là 1 đoạn filter nhìn có vẻ rất vô thường vô phạt, tuy nhiên nó lại là vấn đề của đoạn code này, 1 chút nữa chúng ta sẽ tận dụng nó.
### Class x:
- #### Public parameter:
  - Class có 3 public parameter, đó là:
    
    ```
      public $username;
      public $password;
      public $isAdmin = false;
    ```
- #### Function _contruct:

   ```
        public function __construct($username, $password)
      {
          $this->username = $username;
          $this->password = $password;
      }
   ```

  - Khi 1 đối tượng được khởi tạo, hàm này sẽ được gọi và gắn $username và $password cho các thuộc tính tương ứng của đối tượng đó.
- #### Function _wakeup và serialized:

   ```
          public function __wakeup()
      {
          if ($this->isAdmin) {
              // Ensure the file inclusion is controlled and safe
              if (file_exists("flag.php")) {
                  include "flag.php";
                  echo 'Awesome! Here is your flag: ' . htmlspecialchars($flag, ENT_QUOTES, 'UTF-8');
              } else {
                  echo 'Flag file not found.';
              }
          } else {
              echo 'Incorrect credentials.<br>';
          }
      }

         $username = isset($_GET['username']) ? $_GET['username'] : '';
         $password = isset($_GET['password']) ? $_GET['password'] : '';
      
         $ser = fil(serialize(new x($username, $password)));
         $o = @unserialize($ser);
   ```

   - Khi nhập parameter thì sẽ tiến hành serialized, khi 1 đối tượng được deserialized, hàm _wakeup sẽ được gọi, nó sẽ kiểm tra thuộc tính isAdmin xem có là true hay không, nếu True thì in ra flag, còn false thì in ra Incorrect credentials.
### Nhiệm vụ:
   - Dựa vào đoạn code trên, chúng ta có thể hoàn toàn kiểm soát 2 parameter username và password. Nhiệm vụ của chúng ta là thay đổi 2 parameter này để đổi thuộc tính isAdmin thành true, thì ta sẽ có flag.
# Khai thác:
  **Hướng khai thác**:
   -  Trước tiên ta sẽ test thử, khi nhập username và password ngẫu nhiên thì ta nhận được thông báo Invalid credentials vì thuộc tính isAdmin vẫn bằng False.
      ![Screenshot 2024-10-14 084809](https://github.com/user-attachments/assets/62364644-4fd1-43f0-8212-a25f74d835ca)

   - Tiêp theo, khi thử nhập BlueCyber vào username hoặc password thì ta lại ko nhận được bất cứ thông báo nào cả.
      ![Screenshot 2024-10-14 085009](https://github.com/user-attachments/assets/42cf11b8-186a-457c-8da6-930e23fed8fb)

   - Vậy điều gì đã xảy ra, liệu có phải đoạn code đã bị lỗi không?
   - Để hiểu rõ vấn đề thì chúng ta sẽ dựng local và echo ra $ser và var_dump ra $o để xem điều gì đã xảy ra
      ![Screenshot 2024-10-14 090218](https://github.com/user-attachments/assets/94ec75a1-319b-48fe-a3de-4a7f14350be9)
   - Ta nhận thấy var_dump trả về false, tức là đoạn mã serialize không hợp lệ:
       - Đoạn ban đầu là: ```O:1:"x":3:{s:8:"username";s:9:"BlueCyber";s:8:"password";s:3:"123";s:7:"isAdmin";b:0;}``` (hợp lệ)
       - Sau khi bị filter BlueCyber -> BC, ta có: ```O:1:"x":3:{s:8:"username";s:9:"BC";s:8:"password";s:3:"123";s:7:"isAdmin";b:0;}``` ( không hợp lệ )
   - Ta sẽ thử debug trên php online compiler, dùng đoạn code sau:
     ```
     <?php
          $ser='O:1:"x":3:{s:8:"username";s:9:"BC";s:8:"password";s:3:"123";s:7:"isAdmin";b:0;}';
          $o = unserialize($ser);
          var_dump($o);
          echo strlen('password";s:1:"1";s:7:"isAdmin');
          echo $ser[26]
     ?>
     ```
  - Chạy đoạn code trên ta thấy báo false và báo lỗi offset, đúng như những gì local đã trả về. Filter tưởng chừng như vô hại kia đã gây ra unexpected behavior, do đó rất có khả năng đó sẽ là mấu chốt của bài
  - Sau 1 khoảng thời gian lượn trên mạng, cụ thể là 2 ngày, tôi đã tìm được hướng làm: https://dyn20.gitbook.io/writeup-ctf/root-me/root-me-php-unserialize-overflow
  - Dựa vào writeup trên, hướng làm là ta sẽ sử dụng hàm fil để "nuốt" thuộc tính password, sau đó tạo ra thuộc tính isAdmin bằng true và điều chỉnh sao cho serialize đó hợp lệ
## Debug:
  - Chúng ta sẽ tính spam BlueCyber ở username, và password sẽ viết payload để đảm bảo 'nuốt' được password, password có dạng: ```";";s:7:"isAdmin";b:1;s:8:"password";s:10:```
  - Để tính toán được chúng ta cần bao nhiêu chữ BlueCyber, ta sẽ đếm xem độ dài của thuộc tính username là bao nhiêu, chạy đoạn code php trên ta có: 
      ![Screenshot 2024-10-14 093737](https://github.com/user-attachments/assets/86185305-0142-4c37-9682-089feaa69abd)



