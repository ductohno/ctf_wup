# Đề bài: 
![Screenshot (413)](https://github.com/ductohno/ctf_wup/assets/152991010/23a68e00-237a-4586-bf1f-e19cc27df23d)

Bài cho 2 suộc, cơ bản thì tải C về và xem thôi
# Source:
```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <time.h>
// --------------------------------------------------- SETUP

void ignore_me_init_buffering() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void kill_on_timeout(int sig) {
  if (sig == SIGALRM) {
  	printf("[!] Anti DoS Signal. Patch me out for testing.");
    _exit(0);
  }
}

void ignore_me_init_signal() {
	signal(SIGALRM, kill_on_timeout);
	alarm(60);
}

// --------------------------------------------------- MENU

int get_int(){
    char buf[16];
    read(0,buf,16);
    buf[15]='\0';
    int res=atoi(buf);
    return res;
}
long long current_gold=100;
void print_menu()
{
    puts("Hi i'm @nghiadt1098 and I'm rich as f*ck.");
    puts("If you correctly guess the total score of the cards in my hand, I will reward you alot of VND");
    puts("1. Play");
    puts("2. Buy flag");
    printf("Your money :%lld VND\n",current_gold);
    printf("Your choice: >");
}
// --------------------------------------------------- MAIN
void play()
{
    puts("How many cards you want me to suffle?");
    int cards =get_int();
    if (cards>10)
    {
        puts("Hell nope...");
        return;
    }
    int total=0;
    puts("How much gold you want to bet?");
    int bet=get_int();
    if (cards*bet>current_gold)
    {
        puts("Not enough $$$...");
        return;
    }
    printf("Careful!!! You will lost %d VND if lose\n",cards*bet);
    puts("Can you guess total score of the cards?");
    int guess_score =get_int();
    
    for (int i=0;i<cards;++i)
    {
        total+=rand()%13+1;//From A to K
    }
    if(total==guess_score)
    {
        current_gold+=cards*bet;
        printf("Correct!!! Here your money %d VND\n",cards*bet);
    } else
    {
        current_gold-=cards*bet;
        printf("Incorrect!!! I will take %d VND\n",cards*bet);
    }
    
}
void buy_flag()
{
    puts("This flag cost 1 billion VND");
    if (current_gold>=1000000000)
    {
        current_gold-=1000000000;
        system("cat flag");
        exit(0);
        
    } else
    {
    puts("Tien it ma doi hit fl** thom");
    exit(-1);
    }
    
}
void main(int argc, char* argv[]) {
	ignore_me_init_buffering();
	ignore_me_init_signal();
    srand(time(0));
    while(1)
    {
    	print_menu();
    	int choice =get_int();
    	switch (choice)
        {
            case 1:
                play();
                break;
            case 2:
                buy_flag();
                break;
            default:
                break;
        }
    }
  	
}
```
# Phân tích:
- Có vẻ như đây là 1 trò chơi, nhiệm vụ của chúng ta là cược với máy trong 1 trò chơi dell công bằng tý nào, gần như 100 sẽ thua
- Đầu tiên là 1 hàm giới hạn thời gian, có vẻ như vậy: kill_on_timeout
- Tiếp theo, ta có menu các thứ, ta có 2 lựa chọn, 1 chơi 2 mua flag
- Nếu chơi, hệ thống sẽ bảo ta chọn số card muốn xào, nếu nó lớn hơn 10 thì cook luôn
- Tiếp theo là đặt cược, bạn muốn đặt bao nhiêu, sau đó nó nhân với số bài để ra tổng số tiền cược, ko đủ thì nó sẽ báo ko đủ
- Sau đó, nó sẽ thông báo số tiền sẽ mất nếu thua
- Tiếp theo tùy vào số card bạn chọn, với mỗi card thì nó sẽ random từ 1 đến 13, nếu bạn đoán dính thì ăn tiền, còn sai thì cook
- Flag giá 1 tỷ gold, lmao
- Cuối cùng là mấy hàm swich case để chọn lựa thôi

# Lỗ hổng và hướng giải:
- Chắc chắn for sure là buffer overflow, parameter dính vuln là bet, lý do thì nó sử dụng hàm get_int()
- get_int() thì đúng như cái tên rồi, do đó nếu giá trị >2147483647 thì sẽ dính buffer overflow
- Hướng làm: Sử dụng buffer overflow để làm số tiền trở thành tiền âm, ở đây ta sẽ cho biến bet giá trị là 2147483648 để số tiền bet đạt cực đại âm, sau đó gần nhưu chắc chắn ta sẽ đủ tiền mua flag

# Khai thác:

![Screenshot (414)](https://github.com/ductohno/ctf_wup/assets/152991010/8313494d-7468-47dd-834e-5c5836b93772)

## Flag:
FUSec{th1s_1s_3x4ctly_h0w_my_pwn2own_l00k_l1k3!!}


