# Auto-Make-Deliver-Report
Just because of my laziness

**DISCLAIMER: this is just a play-around tools and the code IS-NOT refactored yet, feel free to use and if you want to contribute, god bless you when start reading the source**


### Latest Version by phuongnh
#### I. Environment
- Any linux distro support python 2.7
- Make sure your machine contains your private key suitable with your gerrit username.

#### II. Installation
Install dependencies

  `$ sudo pip install --proxy <proto://IP:port> -r requirements.txt`

Drop proxy part if you do not use proxy


#### III. How to use
- Run `./xdeliver.py -h` for usage

```bash
hieulq@pwner:~/$ ./xdeliver.py -h
Usage: xdeliver.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o OWNER, --owner=OWNER
                        gerrit pwner [default: hieulq]
  -s SERVER, --server=SERVER
                        gerrit server [default: review.openstack.org]
  -p PORT, --port=PORT  gerrit port [default: 29418]
  --start-time=STARTTIME
                        start time for querrying in gerrit, in format: YYYY-
                        MM-DD
  -k FILE, --keyfile=FILE
                        gerrit ssh keyfile [default: use local keyfile]
  -P PASS, --passphrase=PASS
                        passphrase in case of enrypting keyfile
  -u USER, --user=USER  gerrit user to querry [default: hieulq]
  -d OPTION, --del=OPTION
                        whether to delete delivery folder and loc file
                        [default: 0]
```

For example, if my username is `cap` and I want to query results of user `iron` from `2016-04-01`, before start querying it will delete the current output folder (default is `Delivery`). And note that default `xdeliver` will use my local private key (at `~/.ssh/id_rsa`), if you want to use another keyfile please use option `-k <key_path>` with passphrase along with `-P <pass>`:

   `$ ./xdeliver.py -o cap -u iron  --start-time=2016-04-01 -d 1`

- After that, you will have your `Deliver` folder containing all gerrit patch-set at PDF format. **Please restructure this folder and put another research documents.. into this folder.**

- Run `./gtree.py -h` for usage

```bash
hieulq@pwner:~/$ ./gtree.py -h
Usage: gtree.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PATH, --path=PATH  delivery folder path [default: ~/Deliver]

```

For example, I want to generate the tree file 'list_of_file_Container_20161205.txt' with LOC and page count from folder generate from `xdeliver`:
   
   `$ ./gtree.py -p Deliver >list_of_file_Container_20161205.txt`

- And the result is the file 'list_of_file_Container_20161205.txt' is created with the following content:

```bash
                                            [Page count (for documents)]   [Page count (for source code)]  [Page count (for both)]  [Line count (for source code)]
Total Pages count:------------------------------262 pages
Total Pages count:--------------------------------------------------------------19592 pages
Total Pages count:-----------------------------------------------------------------------------------------------19854 pages
Total Lines count:----------------------------------------------------------------------------------------------------------------------551160 insertion(+), 166573 deletions(-)

Folder PATH listing
|   List_of_files---------------------------------------------------------------------------38
|   
+---1. XXXXXXX
|   +---1.1. XXXXXX
|   |   +---1.1.1. XXXXXXXXXX
|   |   |   +---XXXXXXXXXXXXXXXX
|   |   |   |       XXXXXXXXXXXXXXXXXXXXXXXXXX.pdf------------------------------------------16
|   |   |   |       XXXXXXXXXXXXXXXXXXXXXXX.pdf---------------------------------------------20
|   |   |   |       
|   |   |   +---XXXXXXXXXXXX
|   |   |   |       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX----------1
|   |   |   |       
|   |   |   +---XX
|   |   |   |       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------21
|   |   |   |       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-------------------------20
|   |   |   |       
|   |   |   \---XXXXXXXXX
|   |   |           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX--------------------15
|   |   |  
|    .....
|
|       
\---2. XXXXXXXXX
    +---2.1. XXXXXXXXXXX
    +---2.2. XXXXXXX
    \---2.3. XXXXXXXXXXXXX
        +---2.3.1_XXXXXXXXXXXX
        |   \---XXXXXX
        |       +---XXXXXXXXXXXXXXXX
        |       |         - XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        |       |   \---XXXXXXXXXXXX
        |       |           XXXXXXXXXXXXXXXXXXXXXXXXXXX ------------------------------------------------------------58 insertions(+), 28 deletions(-)
        |       |           XXXXXXXXXXXXXXXXXXXXXXXXXXX ------------------------------------------------------------57 insertions(+), 28 deletions(-)
        |       |           XXXXXXXXXXXXXXXXXXXXXXXXXXX ------------------------------------------------------------62 insertions(+), 28 deletions(-)
        ......
```

### Legacy Version by trananhkma
#### I. Environment
-- Ubuntu 14.04 <br>
-- Mozilla Firefox 43.0.4

#### II. Installation
Install Xvfb – The X Virtual FrameBuffer (Need to run with selenium)

  `$ sudo apt-get install xvfb`

Install selenium - Need to get HTML of JS page. Because gerrit use JS to generate HTML.

  `$ sudo pip install -U selenium`

Install reportlab - A Python lib allow to work with PDF file.

  `$ sudo pip install -U reportlab`


#### III. How to use
1. Chuẩn bị trên FILE SERVER
  - Mở thư mục Knowhow
  - Lưu tại liệư dưới dạng PDF có kèm số trang
  - Mở thư mục IRC meeting & lưu tại liệư dưới dạng PDF có kèm số trang
  - Mở email research nhận được và lưu lại dưới dạng PDF
  - Mở thư mục Call for presentation và lưu lại dưới file PDF

2. Chạy lệnh trên máy Ubuntu
git clone https://github.com/hnwolf/Auto-Make-Deliver-Report.git
cd Auto-Make-Deliver-Report/

sudo apt-get update && sudo apt-get -y upgrade

sudo apt-get install python-pip
sudo -E pip install -r requirements.txt

3. Sửa ~/.ssh/config (chỉ áp dụng khi không connect đc đến gerrit)
$vi ~/.ssh/config
thay dòng 2 bằng dòng:
ProxyCommand connect -S rep.proxy.nic.fujitsu.com:1080 %h 29418
#ProxyCommand connect -S rep.proxy.nic.fujitsu.com:1080 %h %p

3a. Kiểm tra public key đã ở trên server hay chưa. (chỉ làm 1 lần)
https://review.openstack.org/#/settings/ssh-keys

4. Tạo file PDF patchset:
# time yyyy-mm-dd
$export starttime=2017-12-21
./xdeliver.py -o phuongnh -u phuongnh,tuanla,tiendc,cuongnq,hieuht,trungnv --start-time=$starttime -d 1
#./xdeliver.py -o phuongnh -u phuongnh,tuanla,tiendc,cuongnq,hieuht --start-time=$starttime -d 1

5. Copy thư mục Deliver dự án từ file server về thu muc Auto-Make-Deliver-Report, đổi tên để tránh bị nhầm với thư mục Delive vừa được tạo ra. Giữ nguyên tên thư mục 1.1. và 1.3...., 2.1. và 2.3....

6. Tạo thư mục con trong thư mục Deliver/1. Research report/1.2.Compute Baremetal/ (--1--)
         Vi du: 1.2.1 Hardware Inspection feature

7. Copy toàn bộ file pdf đã tạo ở bước 1 vào tung thư mục con của thư mục (--1--) tương ứng.

8. Tạo thư mục con trong thư mục Deliver/ . Ví dụ:
         2. Development report/2.2.Compute Baremetal/2.2.1. Hardware Inspection (x.2.x)

9. Tạo thư mục cho IRC meeting, Call for presentation ..., copy các file liên quan vào đó.

10. Copy thư mục Delivery tree trên server trở lại vào Ubuntu machine
     Xóa nội dung của các thư mục cua cac team khac (khong xoa ten thu muc gốc)
        Copy toàn bộ file pdf đã tạo ở bước 4 vào thư mục con của thư mục (x.2.x) tương ứng bằng cách:
         - Lọc theo tên dự án.
         - So với file Excel hoặc mở từng file xem thuộc thư mục con nào.
         - Copy vào thư mục con tương ứng

11. Tạo file tree
./gtree.py -p Deliver >list_of_file_Baremetal_2018302.txt

12. Sửa file text tạo ở bước 10:
  - Xóa thư mục của team khác tạo thừa
  - Copy 4 dòng đếm số trang lên đầu file và kiểm tra lại con số

13. Copy toàn bộ thư mục lên server vào thư mục 1.2 và 2.2 cho team Baremetal smb://10.164.177.149/

14. Tính tổng các con số

15. Gửi mail confirm cho nơi liên quan.
