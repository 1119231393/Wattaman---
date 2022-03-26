import json
from skimage import io, transform
import numpy as np
# 将img1填充进img2，boxes属于img2，box_a为图像位置，box_b为嵌入位置,stuffing为0时拉伸填充，为1时原比例填充
def imgStuffing(imgPath1, imgPath2, boxes2Path, stuffing):

    img1 = io.imread(imgPath1)
    img2 = io.imread(imgPath2)

    data = json.load(open(boxes2Path))
    rectangle_a_left_top, rectangle_a_right_bottom = [], []
    rectangle_b_left_top, rectangle_b_right_bottom = [], []
    for box in data['boxes']:
        if box.get('name') == 'box_a':
            rectangle_a_left_top = np.array(box.get('rectangle').get('left_top'))
            rectangle_a_right_bottom = np.array(box.get('rectangle').get('right_bottom'))
        elif box.get('name') == 'box_b':
            rectangle_b_left_top = np.array(box.get('rectangle').get('left_top'))
            rectangle_b_right_bottom = np.array(box.get('rectangle').get('right_bottom'))

    img2 = transform.resize(img2, (rectangle_a_right_bottom[0]-rectangle_a_left_top[0], rectangle_a_right_bottom[1]-rectangle_a_left_top[1]))

    #嵌入位置相对图像位置
    left_top_relative = rectangle_b_left_top - rectangle_a_left_top
    right_bottom_relative = rectangle_b_right_bottom - rectangle_a_left_top
    w = right_bottom_relative[0]-left_top_relative[0]
    h = right_bottom_relative[1]-left_top_relative[1]
    if stuffing == 0:
        img1 = transform.resize(img1, (w, h))
        img2[left_top_relative[0]:right_bottom_relative[0], left_top_relative[1]:right_bottom_relative[1]] = img1[:, :]

    else:
        temp = min(w/img1.shape[0], h/img1.shape[1])
        img1 = transform.resize(img1, (int(img1.shape[0]*temp), int(img1.shape[1]*temp)))
        img2[left_top_relative[0]:left_top_relative[0]+img1.shape[0], left_top_relative[1]:left_top_relative[1]+img1.shape[1]] = img1[:, :]

    io.imsave('.\img2_mew_stuffing' + str(stuffing) + '.jpg',img2)

imgPath1 = '.\img1.jpg'
imgPath2 = '.\img1.jpg'
boxes2Path = '.\\boxes.json'
imgStuffing(imgPath1, imgPath2, boxes2Path, 0)
