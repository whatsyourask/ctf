import sys
import cv2

# https://www.geeksforgeeks.org/arithmetic-operations-on-images-using-opencv-set-2-bitwise-operations-on-binary-images/
lemur = sys.argv[1]
flag = sys.argv[2]
lemur_img = cv2.imread(lemur)
flag_img = cv2.imread(flag)
xored_flag = cv2.bitwise_xor(lemur_img, flag_img)
cv2.imwrite('flag.png', xored_flag)
