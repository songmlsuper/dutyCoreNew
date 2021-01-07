# coding=utf-8
#!/usr/bin/python3
####################################################
#    date      editor                        action
# 20180707  李松健                     发布1.0版本
# 20180816  李松健  将节日前一天特殊处理，白班人员可以参加下一日的值班
# 20180904  李松健  将选过6个人后的值班表打乱顺序，避免后续职责选人时的固定顺序现象，例如之前河口都是优先选择新人
# 20180919  李松健  增加3个主岗霍伟、丁肇町、宋鹏程，每日值班主岗人数限制为2人以内
# 20180920  李松健  增加主岗张宁
# 20180927  李松健  将输入参数变为年、月，初始参数全部转移至config.py文件
# 20180928  李松健  人员变化，删除于林立、李沛衡，其他人员重新排序，数据独立存储
# 20181009  李松健  增加日期判断，提示错误的日期输入，生成的csv文件存在D:\\dutyInfo；每日主岗在特殊情况可以为4人
# 20181017  李松健  增加周一小夜班计数器，节假日后第一天的小夜班采用计数器，周一小夜班的多的人值大夜班
# 20181024  李松健  周一小夜班计数器数据补充至2017年7月，增加李松健至值班人员表
# 20190127  宋明霖  读取的duty_schedule.csv,读取日期从倒数第8行读取（添加了一个周五计数器），原来是倒数第7行，111

import calendar
import datetime
import csv
import calculation_edition2
import config2
import sys

# 调用外部参数
StartDate_input = str(sys.argv[1])
EndDate_input = str(sys.argv[2])

#StartDate_input="201812"
#EndDate_input="201902"

#起始日期
StartDate_year = int(StartDate_input[0:4])
StartDate_month = int(StartDate_input[4:6])
StartDate_day = 1
StartDate = StartDate_input + "01"
print("StartDate", StartDate)

# 终止日期
EndDate_year = int(EndDate_input[0:4])
EndDate_month = int(EndDate_input[4:6])
# ########计算每个月第一天是星期几、每个月几天##########
firstDayWeekDay, monthRange = calendar.monthrange(EndDate_year,EndDate_month)
print(firstDayWeekDay, monthRange)
# 每个月的最后一天
EndDate_day = monthRange

EndDate=EndDate_input+str(EndDate_day)
print("EndDate",EndDate)

# 起始日期转日期格式
StartDate_date = datetime.datetime(StartDate_year, StartDate_month, StartDate_day)
print("起始日期:", StartDate_date)
print("起始日期的类型:", type(StartDate_date))
# 终止日期转日期格式
EndDate_date = datetime.datetime(EndDate_year, EndDate_month, EndDate_day)

#########################
# 从配置文件初始化节假日
holiday = config2.holiday
holiday_lastday = config2.holiday_lastday
holiday_nextday = config2.holiday_nextday

##################################历史数据最后一天############################
with open("D:\\dutyInfo\\duty_counter.csv")  as csvfile:
    reader = csv.reader(csvfile)
    TotalLines = csvfile.readlines()
# modified by songml 20190127
# 由于添加了一个周五计数器，时期变为倒数第8行了，即-8
# 原来为-7
# 由于添加了一个河口白班首日计数器，时期变为倒数第9行了，即-9
# 原来为-8
# targetLine = TotalLines[-7]
targetLine = TotalLines[-9]
targetLine = "".join(targetLine.split())  # 去掉无效字符
print("targetLine:", targetLine)
Lastday = targetLine.split(',')[1]
print("历史排班最后一个日期:", Lastday)
csvfile.close()

# 转为时间格式
Lastday_year = int(Lastday[0:4])
Lastday_month = int(Lastday[4:6])
Lastday_day = int(Lastday[6:8])
Lastday_date = datetime.datetime(Lastday_year, Lastday_month, Lastday_day)


a=(StartDate_date - Lastday_date).days
print("起始日期和历史日期的天数差值：", a)
# ########################################################################

# 日期需要满足：1、起始日期在历史时期之后1~15天内；2、终止日期在起始日期后。否则报“输入日期错误”
if ((StartDate_date - Lastday_date).days >= 1) and ((StartDate_date - Lastday_date).days < 15) and ((EndDate_date - StartDate_date).days >= 0):
    print("日期正确")
    # NextDay为排班日
    NextDay = StartDate
    print("StartDate",StartDate)
    # 只要排班日小于排班截至日期就继续执行计算
    while NextDay <= EndDate:
        # 如果排班日是假日，排班日推迟到下一天，直至下一天不是假日跳出
        while NextDay in holiday:
            NextDay_year = int(NextDay[0:4])
            NextDay_month = int(NextDay[4:6])
            NextDay_day = int(NextDay[6:8])

            NextDay_date = datetime.datetime(NextDay_year, NextDay_month, NextDay_day)
            NextDay = (NextDay_date + datetime.timedelta(days=1)).strftime('%Y%m%d')
        if NextDay <= EndDate:
            NextDay_year = int(NextDay[0:4])
            NextDay_month = int(NextDay[4:6])
            NextDay_day = int(NextDay[6:8])
            # 排班日是周几
            Weekday = calendar.weekday(NextDay_year, NextDay_month, NextDay_day) + 1
            # 节日前一天
            if NextDay in holiday_lastday:
                Specialday = 1
            # 节日后一天
            elif NextDay in holiday_nextday:
                Specialday = 2
            # 其他日期
            else:
                Specialday = 0

            NextDay_date = datetime.datetime(NextDay_year, NextDay_month, NextDay_day)

            if Weekday == 6:
                NextDay = (NextDay_date + datetime.timedelta(days=2)).strftime('%Y%m%d')
                continue
            elif Weekday == 7:
                NextDay = (NextDay_date + datetime.timedelta(days=1)).strftime('%Y%m%d')
                continue
            else:
                print("NextDay,Weekday,Specialday:", NextDay, Weekday, Specialday)
                # 进入主排班程序
                calculation_edition2.PaiBan(NextDay, Weekday, Specialday)
                # 如果排班日是周五，下一个排班日就是周一，其他天的排班日为下一天
                if Weekday == 5:
                    NextDay = (NextDay_date + datetime.timedelta(days=3)).strftime('%Y%m%d')
                else:
                    NextDay = (NextDay_date + datetime.timedelta(days=1)).strftime('%Y%m%d')
        else:
            break

else:
    print("输入日期有误")
