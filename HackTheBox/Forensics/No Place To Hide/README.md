# No Place To Hide

Completed: Yes
Platform: HackTheBox

Extracted the files with 7z.

I didn't know what the matter with the Cache.bin file, it is just a binary, but later I found this article, which has a solution to solve the challenge: [https://www.security-hive.com/post/rdp-forensics-logging-detection-and-forensics](https://www.security-hive.com/post/rdp-forensics-logging-detection-and-forensics). It said, that windows takes screenshots and stores them in these files like Cache.bin. To restore the screenshots the article advises to use bmc-tools which I did: [https://github.com/ANSSI-FR/bmc-tools](https://github.com/ANSSI-FR/bmc-tools). After that, I checked the given screenshots and found the flag on a screenshot with cmd.