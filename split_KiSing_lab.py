"""Copyright [2021] [Lei Li].
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import numpy as np
import os


def pack_zero(number, length=4):
    number = str(number)
    return "0" * (length - len(number)) + number


lab_paths = "/jimmy/SVS_system/egs/self_collected/KiSing/downloads/segmented-label"
lab_list = os.listdir(lab_paths)
lab_list.sort()

for lab in lab_list:
    # get path
    lab_dir_path = os.path.join(lab_paths, lab[1:4])
    lab_file = os.path.join(lab_paths, lab)
    if not os.path.exists(lab_dir_path):
        os.mkdir(lab_dir_path)

    print(lab_file)

    # cut
    sub = 1
    sub_data = []
    start = "0"

    lab_data = open(lab_file, "r")
    lab_data = lab_data.read().split("\n")
    
    for label in lab_data:

        label = label.split("\t")

        if len(label) < 3:
            continue

        if start == "0" and float(label[0]) > 1.5:
            begin = "1.500000"
            sub_data.append(begin + "\t" + label[0] + "\tsil\n")

        if float(label[0]) - float(start) >= 3.0:
            gap = (float(label[0]) - float(start) - 3) / 2
            end = round(float(start) + gap, 6)
            sub_data.append(str(start) + "\t" + str(end) + "\tsil\n")
            
            # write to the text
            txt_name = os.path.join(lab_dir_path, pack_zero(sub) + ".txt")
            fileObject = open(txt_name, 'w')
            for data in sub_data:
                fileObject.write(data)
            fileObject.close()

            sub_data = []
            sub += 1
            begin = round(float(label[0]) - gap, 6)
            sub_data.append(str(begin) + "\t" + label[0] + "\tsil\n")

        sub_data.append(label[0] + "\t" + label[1] + "\t" + label[2] + "\n")
        start = label[1]

    if len(sub_data) != 0:
        # write to the text
        txt_name = os.path.join(lab_dir_path, pack_zero(sub) + ".txt")
        fileObject = open(txt_name, 'w')
        for data in sub_data:
            fileObject.write(data)
        fileObject.close()
    