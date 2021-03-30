#!/usr/bin/env python3
# Copyright 2021 The Peking University (author: Lei Li)
import argparse
import os
import pandas as pd
import random
import shutil


def file_filter(wav_file_name):
    if wav_file_name[-4:] == ".wav":
        return True
    else:
        return False


def divide_list(wav_file_name_list):
    wav_file_name_gen = []
    wav_file_name_true = []
    for name in wav_file_name_list:
        if name[-9:] == "_true.wav":
            wav_file_name_true.append(name)
        else:
            wav_file_name_gen.append(name)

    return wav_file_name_gen, wav_file_name_true


def random_list(name_list, seed):
    random.seed(seed)
    random.shuffle(name_list)

    return name_list


def process_mos(args):
    setting_name_list = os.listdir(args.input_file_path)

    if len(setting_name_list) == 0:
        print("Input directory is empty")
        exit()

    for setting_name in setting_name_list:
        if setting_name[0] == ".":
            continue
        # load wav file name
        wav_file_name_list = os.listdir(args.input_file_path + "/" + setting_name)
        wav_file_name_list = list(filter(file_filter, wav_file_name_list))
        wav_file_name_list.sort()

        wav_file_name_gen, wav_file_name_true = divide_list(wav_file_name_list)

        # generate random file
        wav_file_name_gen = random_list(wav_file_name_gen, args.seed)
        wav_file_name_true = random_list(wav_file_name_true, args.seed)

        # generate output
        if not os.path.exists(args.output_file_path):
            os.mkdir(args.output_file_path)
        if not os.path.exists(args.output_file_path + "/mos"):
            os.mkdir(args.output_file_path + "/mos")
        if not os.path.exists(args.output_file_path + "/mos/" + setting_name):
            os.mkdir(args.output_file_path + "/mos/" + setting_name)
        if not os.path.exists(args.output_file_path + "/mos/" + setting_name + "/true"):
            os.mkdir(args.output_file_path + "/mos/" + setting_name + "/true")
        if not os.path.exists(args.output_file_path + "/mos/" + setting_name + "/gen"):
            os.mkdir(args.output_file_path + "/mos/" + setting_name + "/gen")

        if args.top_number > len(wav_file_name_gen):
            print("We don't have enough wav")
            exit()

        gen_name_list = []
        true_name_list = []
        for i in range(args.top_number):
            gen_name = args.output_file_path + "/mos/" + setting_name + "/gen/" + str(i) + "_gen.wav"
            shutil.copyfile(args.input_file_path + "/" + setting_name + "/" + wav_file_name_gen[i], gen_name)
            gen_name_list.append(str(i) + "_gen.wav")
            true_name = args.output_file_path + "/mos/" + setting_name + "/true/" + str(i) + "_true.wav"
            shutil.copyfile(args.input_file_path + "/" + setting_name + "/" + wav_file_name_true[i], true_name)
            true_name_list.append(str(i) + "_true.wav")

        df1 = pd.DataFrame(wav_file_name_gen[:args.top_number])
        df2 = pd.DataFrame(gen_name_list)
        df3 = pd.DataFrame(wav_file_name_true[:args.top_number])
        df4 = pd.DataFrame(true_name_list)

        df_file = pd.concat([df1, df2, df3, df4], axis=1, ignore_index=True)
        df_file.to_csv(args.output_file_path + "/mos/" + setting_name + "/mapping_file.csv", header=False, index=False)


def process_preference(args):

    setting_name_list = os.listdir(args.input_file_path)
    # remove bad file (e.g. .DS_Store)
    for setting_name in setting_name_list:
        if setting_name[0] == '.':
            setting_name_list.remove(setting_name)

    if len(setting_name_list) == 0:
        print("Input directory is empty")
        exit()

    gen_name_list = []
    ori_name_list = []
    gt_name_list = []

    # random get song name
    name_dir = os.listdir(args.input_file_path + "/" + setting_name_list[0])
    name_dir = list(filter(file_filter, name_dir))
    name_dir.sort()

    name_dir_gen, name_dir_true = divide_list(name_dir)
    name_dir_gen = random_list(name_dir_gen, args.seed)
    name_dir_true = random_list(name_dir_true, args.seed)
    name_dir_gen = name_dir_gen[:args.top_number]
    name_dir_true = name_dir_true[:args.top_number]

    # print(name_dir_gen)
    # print(name_dir_true)

    base_dir = args.output_file_path + "/preference"
    gen_dir = base_dir + "/gen"
    ori_dir = base_dir + "/ori"
    gt_dir = base_dir + "/gt"

    if not os.path.exists(args.output_file_path):
        os.mkdir(args.output_file_path)
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    if not os.path.exists(gen_dir):
        os.mkdir(gen_dir)
    if not os.path.exists(ori_dir):
        os.mkdir(ori_dir)
    if not os.path.exists(gt_dir):
        os.mkdir(gt_dir)

    # get all setting for every gen song
    for i, song_name in enumerate(name_dir_gen):
        # random sort setting list
        setting_name_list = random_list(setting_name_list, args.seed)
        for j, setting_name in enumerate(setting_name_list):
            # move gt to the gt_dir
            gt_name = setting_name + "_" + name_dir_true[i]
            shutil.copyfile(args.input_file_path + "/" + setting_name + "/" + name_dir_true[i], gt_dir + "/" + gt_name)
            # move gen to gen_dir
            gen_name = str(i) + "_" + str(j) + ".wav"
            shutil.copyfile(args.input_file_path + "/" + setting_name + "/" + name_dir_gen[i], gen_dir + "/" + gen_name)
            # move ori to ori_dir
            ori_name = setting_name + "_" + name_dir_gen[i]
            shutil.copyfile(args.input_file_path + "/" + setting_name + "/" + name_dir_gen[i], ori_dir + "/" + ori_name)

            gen_name_list.append(gen_name)
            ori_name_list.append(ori_name)
            gt_name_list.append(gt_name)

    # generate csv
    df1 = pd.DataFrame(gen_name_list)
    df2 = pd.DataFrame(ori_name_list)
    df3 = pd.DataFrame(gt_name_list)

    df_file = pd.concat([df1, df2, df3], axis=1, ignore_index=True)
    df_file.to_csv(base_dir + "/mapping_file.csv", header=False, index=False)


def process(args):
    # # here are the input and output data paths
    # args.input_file_path = "/Users/jimmyli/PycharmProjects/random_wav/input"
    # args.output_file_path = "/Users/jimmyli/PycharmProjects/random_wav/output"
    # # how many random wav you need
    # args.top_number = 10

    if args.option == "mos":
        process_mos(args)
    elif args.option == "preference":
        process_preference(args)
    else:
        print("Option is mos or preference")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file_path", type=str, help="input file directory")
    parser.add_argument("--output_file_path", type=str, help="output file directory")
    parser.add_argument("--option", type=str, default="mos", help="preference or mos")
    parser.add_argument("--top_number", type=int, default=10, help="How many random wav you need")
    parser.add_argument("--seed", type=int, default=777, help="Random seed")
    args = parser.parse_args()
    process(args)
