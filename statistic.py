import os
import prettytable as pt
from colorama import Fore,Style
import pandas as pd
import csv
class FileAnalysis:
    def __init__(self):
        self.TLine=0 # 总代码行
        self.CLine=0 # 总命令行
        self.BLine=0 # 总空行
        # 美化打印存储到list中
        self.file_list=[] # 文件名list
        self.total_list=[] # 每个文件总代码list
        self.comment_list=[] # 每个文件总注释list
        self.blank_list=[] # 每个文件总空行list
        self.actual_list=[] # 每个文件实际代码量list
        self.actual_rate=[] # 每个文件实际代码比率list
        self.comment_rate=[] # 每个文件实际注释比率list
        self.black_rate=[] # 每个文件空行比率list
        self.isOne=True # 是否第一次写入csv
    def coutLines(self,file):
        comment_line = 0
        blank_line = 0
        with open(file, encoding='utf-8', errors='ignore') as f:
            # 返回每一个列表，包含每一行代码
            lines = f.readlines()
            # 总行数
            total_line = len(lines)
            # 遍历每一行
            for i in range(total_line):
                line = lines[i]
                # 检查是否为注释
                if line.startswith("#"):
                    comment_line += 1
                elif line.strip().startswith("'''") or line.strip().startswith('"""'):
                    comment_line += 1
                    if line.count('"""') == 1 or line.count("'''") == 1:
                        while True:
                            line = lines[i]
                            comment_line += 1
                            i+=1
                            if ("'''" in line) or ('"""' in line):
                                break
                # 检查是否为空行
                elif line == '\n':
                    blank_line += 1
        # 输出每个文件结果
        print("在%s中:" % file)
        print("代码行数：", total_line)
        print("注释行数:", comment_line)
        print("空行数:", blank_line)
        actual_line=total_line - comment_line - blank_line
        print("实际总行数:",actual_line)
        # 实际代码比率
        actual_ra=0
        # 注释比率
        comment_ra=0
        # 空行比率
        black_ra=0
        try:
            actual_ra=actual_line/total_line
            print("实际总行数占比率:",actual_ra)
        except Exception as e:
            print("实际总行数占比率:", 0)
        try:
            comment_ra=comment_line/total_line
            print("注释行数占比率:",comment_ra)
        except Exception as e:
            print("注释行数占比率:", 0)
        try:
            black_ra=blank_line/total_line
            print("空行数占比率:",black_ra)
        except Exception as e:
            print("空行数占比率:", 0)
        # 往list中添加数据
        self.actual_list.append(actual_line)
        # 格式化添加输出比率百分百
        self.actual_rate.append(format(actual_ra,'0.1%'))
        self.comment_rate.append(format(comment_ra,'0.1%'))
        self.black_rate.append(format(black_ra,'0.1%'))
        # 取xx.py
        self.file_list.append(Fore.GREEN+file.split('\\')[-1])
        self.total_list.append(total_line)
        self.comment_list.append(comment_line)
        self.blank_list.append(blank_line)

        # 存储csv数据格式化
        # list添加多个数据
        data_list = [file.split('\\')[-1],total_line,comment_line,blank_line,actual_line,actual_ra,comment_ra,black_ra]
        if self.isOne:
            # 存储head
            self.saveCSV(data_list,self.isOne)
            self.isOne=False
        # 存储
        self.saveCSV(data_list)
        return total_line, comment_line, blank_line
    def fileAnalysis(self,dir):
        # 列出目录下的所有文件和目录
        list_files = os.listdir(dir)
        for file in list_files:
            filepath = os.path.join(dir, file)
            # 目录：递归遍历子目录
            if os.path.isdir(filepath):
                self.fileAnalysis(filepath)
            # 文件：直接统计行数
            elif os.path:
                if os.path.splitext(file)[1] == '.py':
                    total_line, comment_line, blank_line=self.coutLines(filepath)
                    self.TLine+=total_line
                    self.CLine+=comment_line
                    self.BLine+=blank_line

    # 输出打印
    def output(self):
        # 添加总统计
        self.file_list.insert(0,Fore.LIGHTRED_EX+'总统计结果'+Fore.RESET)
        self.total_list.insert(0,Fore.LIGHTRED_EX + str(self.TLine) + Fore.RESET)
        self.comment_list.insert(0,Fore.LIGHTRED_EX + str(self.CLine) + Fore.RESET)
        self.blank_list.insert(0,Fore.LIGHTRED_EX + str(self.BLine) + Fore.RESET)
        actual_line = self.TLine-self.CLine-self.BLine
        self.actual_list.insert(0,Fore.LIGHTRED_EX + str(actual_line) + Fore.RESET)
        self.actual_rate.insert(0,Fore.LIGHTRED_EX +str(format((self.TLine-self.CLine-self.BLine)/self.TLine,'0.1%'))+Fore.RESET)
        self.comment_rate.insert(0,Fore.LIGHTRED_EX+str(format(self.CLine/self.TLine,'0.1%'))+Fore.RESET)
        self.black_rate.insert(0,Fore.LIGHTRED_EX+str(format(self.BLine/self.TLine,'0.1%'))+Fore.RESET)

        # 美化打印输出
        tb = pt.PrettyTable()
        tb.add_column(Fore.LIGHTMAGENTA_EX+"文件"+Fore.RESET,self.file_list)
        tb.add_column(Fore.LIGHTMAGENTA_EX+'总代码量'+Fore.RESET,self.total_list)
        tb.add_column(Fore.LIGHTMAGENTA_EX+'总注释量'+Fore.RESET,self.comment_list)
        tb.add_column(Fore.LIGHTMAGENTA_EX+'总空行量'+Fore.RESET,self.blank_list)
        tb.add_column(Fore.LIGHTMAGENTA_EX+'实际代码量'+Fore.RESET,self.actual_list)
        tb.add_column(Fore.LIGHTMAGENTA_EX+'实际代码比率'+Fore.RESET,self.actual_rate)
        tb.add_column(Fore.LIGHTMAGENTA_EX+'总注释比率'+Fore.RESET,self.comment_rate)
        tb.add_column(Fore.LIGHTMAGENTA_EX+'总空行比率'+Fore.RESET,self.black_rate)
        print(Fore.RED+"-----------------------------------------------光城18年9月份以后部分python代码统计结果-----------------------------------------------")
        print(Style.RESET_ALL)
        print(tb)
        print(Style.RESET_ALL)
    def saveCSV(self, data_list, isOne=False):
        # newline=''防止写入留空行问题
        # 追加写入
        with open("data.csv", "a+", encoding='utf_8_sig',newline='') as cf:
            writer = csv.writer(cf)
            # 如果是第一次写入，就写head,后面就正常写入
            if isOne:
                data_list = ['文件', '总代码量', '总注释量', '总空行量', '实际代码量', '实际代码比率', '总注释比率', '总空行比率']
            writer.writerow(data_list)
    # 排序
    def codeSort(self,c_name='实际代码量'):
        df = pd.DataFrame(pd.read_csv('./data.csv',encoding='utf_8_sig'))
        # print(df)
        # lc.sort(["loan_amnt"], ascending=True).head(10)
        print(df.sort_values(c_name,ascending=False,inplace=True))
        print(df.head(10))
        print(df.describe())
        print(df.sum())
        df.to_csv('./sort_data.csv',encoding='utf_8_sig',index=False)

dir = './code_dir'
fa = FileAnalysis()
fa.fileAnalysis(dir)
print(fa.TLine)
print(fa.CLine)
print(fa.BLine)
fa.output()
fa.codeSort('总代码量')
