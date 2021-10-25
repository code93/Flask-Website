from os import path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
import pickle
import cv2
import os
from flask import current_app


# Loading all the models
haar = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')
# pickle files
mean = pickle.load(open('./model/mean_preprocess.pickle','rb'))
model_svm = pickle.load(open('./model/model_svm.pickle','rb'))
model_pca = pickle.load(open('./model/pca_50.pickle','rb'))

print('Model loaded sucessfully')

# settings
gender_pre = ['Male','Female']
font = cv2.FONT_HERSHEY_SIMPLEX

def pipeline_model(path,filename, color='bgr'):
    #step-1: read image in cv2
    img = cv2.imread(path)

    #step 2: convert into grayscale
    if color == 'bgr':
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    else:
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    # step-3: crop the face (using haar cascade classifier)
    faces = haar.detectMultiScale(gray,1.5,3)
    for x,y,w,h in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2) #drawing rectangle
        roi = gray[y:y+h,x:x+w] #crop image
        # step 4: normalization
        roi = roi / 255.0
        # step-5: resize image (100,100)
        if roi.shape[1] > 100:
            roi_resize = cv2.resize(roi,(100,100),cv2.INTER_AREA)
        else:
            roi_resize = cv2.resize(roi,(100,100),cv2.INTER_CUBIC)

        # step-6: flattening (1x10000)
        roi_reshape = roi_resize.reshape(1,10000) # 1,-1

        # step-7: subtract with mean
        roi_mean = roi_reshape - mean

        # step-8: get eigen image
        eigen_image = model_pca.transform(roi_mean)

        # step-9: pass to ml model (svm)
        results = model_svm.predict_proba(eigen_image)[0]

        # step-10:
        predict = results.argmax() # 0 or 1
        score = results[predict]

        # step-11:
        text = "%s : %0.2f"%(gender_pre[predict],score)
        cv2.putText(img,text,(x,y),font,1,(255,255,0),2)
    path = os.path.join(current_app.root_path,'static/predict/{}'.format(filename))
    cv2.imwrite(path,img)
    
        