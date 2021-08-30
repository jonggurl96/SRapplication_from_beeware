import os, glob, cv2
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform.pyramids import pyramid_expand

gt_paths = ['images\\GroundTruth\\test', 'images\\GroundTruth\\train', 'images\\GroundTruth\\val']
input_paths = ['images\\Inputs\\test', 'images\\Inputs\\train', 'images\\Inputs\\val']

for i, gp in enumerate(gt_paths):
  imgs_paths = sorted(glob.glob(os.path.join(gp, '*.jpg')))
  for img_path in tqdm(imgs_paths):
    # 0 ~ 255 사이의 정수 값 RGB 이미지
    img = cv2.imread(img_path)
    height, width = img.shape[:2]

    # 이미지 축소 후 확장으로 GroundTruth와 크기가 같은 Input 이미지 생성
    img = cv2.resize(img, (width//4, height//4), interpolation=cv2.INTER_CUBIC)
    img = pyramid_expand(img, upscale=4, multichannel=True)
    img = (img*255).astype("uint8")

    # Input Image 저장 경로
    input_path = os.path.join(input_paths[i], img_path.split('\\')[-1])

    # 이미지 저장
    cv2.imwrite(input_path, img)

