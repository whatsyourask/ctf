# MarketDump

Completed: Yes
Date: July 2, 2021 → July 2, 2021
Platform: HackTheBox

Firstly, I just went through the pcap file with wireshark. Then, I saw the next protocols: `MySQL, SSH, Telnet, PSQL, HTTP`. Task said that the hacker made pivoting and stolen the database. Then, he targeted one of the customers. 

I install http filter and found this request:

```bash
2718	985.569074742	10.0.2.15	10.0.2.3	HTTP	207	GET /costumers.sql HTTP/1.1
```

That's it. Seeing the response:

```bash
'ÅRT5ETµÔ£@9

'è	õ°R6ØªwPÿÿl¹82
American Express,341949175783899
American Express,375689679496296
.................................
```

Okay, just follow HTTP stream and list the entire response, You will find very different from the others string. This is the key and flag. But it is encoded. To decode it you have to try to decode as some encoded string by base encoding family. Also, I found the commands where you can see how exactly the hacker got the database. He did some OS injection in the program and started a bind shell from it. After he connected, he executed the python HTTP server and request the database.