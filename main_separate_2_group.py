import os
import cv2
import time
import FocusStack
from collections import defaultdict
import re

def natural_sort_key(s):
    # ฟังก์ชันสำหรับแยกตัวเลขออกจากชื่อไฟล์ เพื่อการเรียงลำดับตามตัวเลข
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]

def stackHDRs(image_files, output_filename, chunk_size=3):
    # เช็คว่ามีกี่กลุ่ม โดยเอาจำนวนรูปทั้งหมดหาร 4 (ถ้าเหลือเศษจากการหาร (เศษไม่เท่ากับ 0) จะเพิ่ม 1 เข้าไปที่ num_chunks)
    num_chunks = len(image_files) // chunk_size + (1 if len(image_files) % chunk_size != 0 else 0)
    merged_images = []

    for i in range(num_chunks):
        # ใน 1 กลุ่มย่อย มี 5 รูป เรียงแบบนี้ image_files[0:5] -> image_files[5:10] -> image_files[10:15]
        chunk_files = image_files[i * chunk_size:(i + 1) * chunk_size]
        focusimages = []

        for img in chunk_files:
            print("Reading in file {}".format(img))
            focusimages.append(cv2.imread("input/{}".format(img)))

        merged_chunk = FocusStack.focus_stack(focusimages)
        merged_images.append(merged_chunk)

        # ล้างหน่วยความจำ
        del focusimages
        del merged_chunk

    # แบ่งกลุ่มย่อยอีกชั้นนึงด้วย chunk_size = 2
    final_merged_images = []
    final_chunk_size = 3
    final_num_chunks = len(merged_images) // final_chunk_size + (1 if len(merged_images) % final_chunk_size != 0 else 0)

    for i in range(final_num_chunks):
        final_chunk = merged_images[i * final_chunk_size:(i + 1) * final_chunk_size]
        final_merged_chunk = FocusStack.focus_stack(final_chunk)
        final_merged_images.append(final_merged_chunk)

        # ล้างหน่วยความจำ
        del final_chunk
        del final_merged_chunk

    # ทำ FocusStack รอบสุดท้ายกับภาพที่รวมกันได้ทั้งหมด
    final_image = FocusStack.focus_stack(final_merged_images)
    cv2.imwrite(output_filename, final_image)

    # ล้างหน่วยความจำ
    del merged_images
    del final_merged_images
    del final_image

if __name__ == "__main__":
    start_time = time.time()

    image_files = sorted(os.listdir("input"))

    # กรองเฉพาะไฟล์ที่เป็นรูปภาพ
    image_files = [img for img in image_files if img.split(".")[-1].lower() in ["jpg", "jpeg", "png", "bmp"]]

    # เรียงไฟล์ตามลำดับตัวเลขในชื่อไฟล์
    image_files.sort(key=natural_sort_key)

    # จัดกลุ่มไฟล์ตาม prefix
    groups = defaultdict(list)
    for img in image_files:
        prefix = "_".join(img.split("_")[:2])
        groups[prefix].append(img)

    # ประมวลผลแต่ละกลุ่ม
    for idx, (prefix, group_files) in enumerate(groups.items(), start=1):
        output_filename = f"merged{idx}.bmp"
        stackHDRs(group_files, output_filename)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"All Time Process: {elapsed_time:.2f} sec")
    print("That's All Folks!")
