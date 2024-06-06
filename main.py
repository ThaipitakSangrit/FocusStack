import os
import cv2
import time
import FocusStack
from collections import defaultdict

"""

    Focus stack driver program

    This program looks for a series of files of type .jpg, .jpeg, or .png
    in a subdirectory "input" and then merges them together using the
    FocusStack module.  The output is put in the file merged.png


    Author:     Charles McGuinness (charles@mcguinness.us)
    Copyright:  Copyright 2015 Charles McGuinness
    License:    Apache License 2.0

"""

def stackHDRs(image_files, output_filename):
    focusimages = []
    for img in image_files:
        print ("Reading in file {}".format(img))
        focusimages.append(cv2.imread("input/{}".format(img)))

    merged = FocusStack.focus_stack(focusimages)
    cv2.imwrite(output_filename, merged)


if __name__ == "__main__":
    start_time = time.time()

    image_files = sorted(os.listdir("input"))

    for img in image_files:
        if img.split(".")[-1].lower() not in ["jpg", "jpeg", "png", "bmp"]:
            image_files.remove(img)

    groups = defaultdict(list)
    for img in image_files:
        prefix = "_".join(img.split("_")[:2])
        groups[prefix].append(img)

    for idx, (prefix, group_files) in enumerate(groups.items(), start=1):
        output_filename = f"merged{idx}.bmp"
        stackHDRs(group_files, output_filename)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"All Time Process: {elapsed_time:.2f} sec")
    print ("That's All Folks!")
