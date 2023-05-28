import cv2
import numpy as np
import pytesseract

class imgToText:

    def cropImage(self,car_image):
        #try:
             # Read input image
             img = cv2.imread(car_image)
             # convert input image to grayscale
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
             # read haarcascade for number plate detection
             cascade = cv2.CascadeClassifier('support/haarcascade_russian_plate_number.xml')
             # Detect license number plates
             plates = cascade.detectMultiScale(gray, 1.2, 5)
             print('Number of detected license plates:', len(plates))
             # loop over all plates
             loop=0
             for (x, y, w, h) in plates:
                 # draw bounding rectangle around the license number plate
                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                 gray_plates = gray[y:y + h, x:x + w]
                 color_plates = img[y:y + h, x:x + w]
                 cropped_image='images/cropped_images/crop_numberplate'+str(loop)+'.jpg'
                 # save number plate detected
                 cv2.imwrite(cropped_image, gray_plates)
                 car_number_as_plate=self.extractText(cropped_image)
                 print(car_number_as_plate)
                 #cv2.waitKey(0)
                 loop=loop+1
             return car_number_as_plate
        #except:
             print("Unable to detect license plates from Video")
        #finally:
             cv2.destroyAllWindows()

    # Extract text from image.
    def extractText(self,croppedImg):

        image = cv2.imread(croppedImg)
        # Preprocess the image for improved OCR accuracy
        # Increasing the image size & converting to gray for better reading
        resized_image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # Set Tesseract configuration options
        # whitelist has to ignore unwanter characters coming from tesseract
        custom_config = r'--oem 3 --psm 3 -l eng -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        # Extract text from the preprcessed image
        text = pytesseract.image_to_string(gray_image, config=custom_config)
        filter_text = "".join(text.split()).replace(":", "").replace("-", "")
        return filter_text


