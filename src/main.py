from image_sizing import pixelate_with_cv2
import cv2

# from image_sizing import
img_path = "/Users/kim/Desktop/repos/PixelToThread/images/newyork.png"


_, low_preview = pixelate_with_cv2(img_path, preset="low")
_, med_preview = pixelate_with_cv2(img_path, preset="medium")
_, high_preview = pixelate_with_cv2(img_path, preset="high")

cv2.imshow("Low Resolution", low_preview)
cv2.imshow("Medium Resolution", med_preview)
cv2.imshow("High Resolution", high_preview)

cv2.waitKey(0)
cv2.destroyAllWindows()




