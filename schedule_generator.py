import argparse
import os
import math
from datetime import datetime, timedelta
import shutil
import random

vocab_dir = ""

review_frequency = [1,2,4,7,10,15,20]
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def generate_schedule(vocab):
    # determine daily amount
    amount = 0
    while True:
        print("\n------------------计划数据生成------------------")
        # get user input
        usr_input = input(f"请输入每日新增单词数量(1 ~ {len(vocab)})： ")
        try:
            amount = int(usr_input)
        except:
            print(f"{bcolors.FAIL}Only numeric input accepted{bcolors.ENDC}")
        if amount < 1 or amount > len(vocab):
            print(f"{bcolors.FAIL}Index Out of Bound Error: daily amount {amount} exceeds range [1, {len(vocab)}]{bcolors.ENDC}")
            continue
        # calculate stats
        days = math.ceil(len(vocab) / amount)
        last_amount = len(vocab) - amount * (days - 1)
        daily_amount = [0] * (days + max(review_frequency))
        for i in range(days):
            temp_amount = amount if i != days - 1 else last_amount
                    
            daily_amount[i] += temp_amount
            for freq in review_frequency:
                daily_amount[i + freq] += temp_amount
        
        # get start date
        date_input = None
        while True:
            date_input = input("请输入开始日期（YYYY-mm-dd): ")
            try:
                date_input = date_input.strip().replace("\n","")
                date_input = datetime.strptime(date_input, '%Y-%m-%d')
            except Exception as e:
                print(f"{bcolors.FAIL}日期格式错误 {e}{bcolors.ENDC}")
                continue
            break

        # print stats
        finish_date = date_input + timedelta(days = len(daily_amount) - 1)
        print(f"\n从 {bcolors.OKCYAN}{date_input.strftime('%Y-%m-%d')}{bcolors.ENDC} 开始至 {bcolors.OKCYAN}{finish_date.strftime('%Y-%m-%d')}{bcolors.ENDC} 结束，一共 {bcolors.OKCYAN}{len(daily_amount)}{bcolors.ENDC} 天完成，单日最大复习词汇量 {bcolors.OKCYAN}{max(daily_amount) - amount}{bcolors.ENDC} ")
        confirm = input("确认[y] / n ? ")
        confirm = True if confirm in ['Y','y'] else False
        print("---------------------------------------------")
        if not confirm:
            continue
        break
        
    # generate daily list
    days = math.ceil(len(vocab) / amount)
    result = []
    for i in range(days):
        result.append(vocab[amount * i : min(len(vocab) + 1, amount * (i + 1))])
    return result, date_input

def remove_duplicate(vocab):
    vocab_set = set()
    new_vocab = []
    for w in vocab:
        separator = w.find("-")
        word = w[:separator]
        if word not in vocab_set:
            new_vocab.append(w)
            vocab_set.add(word)
    print(f"remove {len(vocab) - len(new_vocab)}")
    return new_vocab

def main():
    for root, dir, files in os.walk("."):
        if len(dir) == 0:
            continue
        dir = [i for i in dir if "每日任务" not in i]
        # print available choices
        print(f"已读取单词书:")
        counter = 1
        for cur_dir in dir:
            print(f"\t({counter}) {cur_dir}")
            counter += 1
        
        # parse input
        choices = input("请选择单词书编号(逗号分割编号)： ")
        choices = choices.replace(" ","").split(",")
        output_info = f"已选择单词书： "
        for choice in choices:
            choice = int(choice)
            if choice > len(dir) or choice < 1:
                print(f"{bcolors.FAIL}Index Out of Bound Error: find input {choice} exceeds range [1, {len(dir)}]{bcolors.ENDC}")
                exit(1)
            output_info += dir[choice - 1] + " "
        print(output_info)

        # build vocab list
        vocab = []
        for choice in choices:
            print(f"checking {vocab_dir}/{dir[int(choice) - 1]}")
            for root_, dir_, files_ in os.walk(f"{vocab_dir}/{dir[int(choice) - 1]}"):
                files_ = [i for i in files_ if ".txt" in i]
                for file in files_:
                    with open(os.path.join(root_, file)) as f:
                        whole_file = ""
                        for line in f:
                            whole_file += line
                        lines = whole_file.split("\n\n")
                        for line in lines:
                            if len(line) > 0:
                                vocab.append(line) 

        # remove duplicate, shuffle
        vocab = remove_duplicate(vocab)
        vocab.sort()
        random.Random(340).shuffle(vocab)

        # create or clean existing result dir
        if os.path.isdir(f"{vocab_dir}/每日任务"):
            shutil.rmtree(f"{vocab_dir}/每日任务")
        os.system(f"mkdir {vocab_dir}/每日任务")

        daily_list, start_date = generate_schedule(vocab)
        # generate new list
        for i in range(len(daily_list)):
            cur_list = daily_list[i]
            with open(f"{vocab_dir}/每日任务/list_{i+1}.txt","w") as f:
                for word in cur_list:
                    f.write(f"{word}\n\n")
        # generate task list
        review_list = [""] * (len(daily_list) + max(review_frequency))
        for i in range(len(daily_list)):
            for freq in review_frequency:
                review_list[i + freq] += f"{i+1},"

        # write schedule
        with open(f"{vocab_dir}/每日任务/schedule.md","w") as f:
            f.write("| day     | new list    | review_list    |\n")
            f.write("| ---- | ---- | ---- |\n")
            for i in range(len(review_list)):
                new_list = f"list {i + 1}" if i < len(daily_list) else ""
                review_str = review_list[i].replace(",",", ")
                review_str = review_str[:-2] if len(review_str) > 0  else ""
                review_str = f"list {review_str}" if len(review_str) > 0 else ""
                cur_date = start_date + timedelta(days = i)
                f.write(f"| {cur_date.strftime('%Y-%m-%d')}   | {new_list}    | {review_str}    |\n")
        print(f"背单词计划以生成至路径{vocab_dir}/每日任务")


if __name__ == "__main__":
    vocab_dir = "."
    main()