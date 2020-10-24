Open data.pcap in `wireshark`:

![wireshark](screenshots/wireshark.png)

Then i decided to look at data from application to network layer:

![http](screenshots/http.png)

And i saw in there js function ass() that users would probably login through. In one of the packages i found the creds:

![creds](screenshots/creds.png)

You can see that it is the base64 encoded password.
