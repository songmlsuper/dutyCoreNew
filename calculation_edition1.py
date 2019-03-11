#!/usr/bin/python3
####################################################
##    date      editor                        action
## 20180707  李松健                     发布1.0版本
## 20180816  李松健  将节日前一天特殊处理，白班人员可以参加下一日的值班
## 20180904  李松健  将选过6个人后的值班表打乱顺序，避免后续职责选人时的固定顺序现象，例如之前河口都是优先选择新人
## 20180919  李松健  增加3个主岗霍伟、丁肇町、宋鹏程，每日值班主岗人数限制为2人以内
## 20180920  李松健  增加主岗张宁
## 20180927  李松健  将输入参数变为年、月，初始参数全部转移至config.py文件
## 20180928  李松健  人员变化，删除于林立、李沛衡，其他人员重新排序，数据独立存储
## 20181009  李松健  增加日期判断，提示错误的日期输入，生成的csv文件存在D:\\dutyInfo；每日主岗在特殊情况可以为4人
## 20181017  李松健  增加周一小夜班计数器，节假日后第一天的小夜班采用计数器，周一小夜班的多的人值大夜班
## 20181024  李松健  周一小夜班计数器数据补充至2017年7月，增加李松健至值班人员表
## 20181214  宋明霖  夜班女生人数限制为最多2人
## 20190122  宋明霖  添加节假日后首日与周一合并作为【节假日后首日】进行计数，逻辑一并调整
## 20190125  宋明霖  添加周五计数器，CVS添加周五计数器，排完班后需要相应地计数。
## 20190126  宋明霖  组人员调整F5 李松健 <=> C3 范嵩  ==> C3 李松健, F5 范嵩，去掉I4
##                   相应的角色也调整 git test 5 1
import csv
import random
import config


SongDict=config.SongDict


#节假日的前一交易日
holiday_lastday = config.holiday_lastday

def PaiBan(StartDate, Weekday, Specialday):

    #日志文件
    f = open("D:\\dutyInfo\\test.log", 'a')
    f.write('#################################################################################################' )
    f.write('\n'+'日志日期：'+StartDate)
    #####################从历史数据中提取最后一次的值班人员###########
    LastMateList_1 = [0, 0, 0, 0, 0, 0]
    LastMateList_2 = [0, 0, 0, 0, 0, 0]
    LastMateList_3 = [0, 0, 0, 0, 0, 0]
    with open("D:\\dutyInfo\\duty_schedule_raw.csv")  as csvfile:
        reader = csv.reader(csvfile)
        TotalLines = csvfile.readlines()
    #倒数第1天的值班人员
    targetLine_1 = TotalLines[-1]
    #倒数第2天的值班人员
    targetLine_2 = TotalLines[-2]
    #倒数第3天的值班人员
    targetLine_3 = TotalLines[-3]

    targetLine_1 = "".join(targetLine_1.split())  # 去掉无效字符
    targetLine_2 = "".join(targetLine_2.split())  # 去掉无效字符
    targetLine_3 = "".join(targetLine_3.split())  # 去掉无效字符

    for i in range(1, len(targetLine_1.split(','))):
        LastMateList_1[i - 1] = targetLine_1.split(',')[i]
    Date_1=targetLine_1.split(',')[0]
    print("昨天的值班日期:", Date_1)
    print("昨天的值班人员:", LastMateList_1)
    f.write('\n' + '昨天的值班人员：' + str(LastMateList_1))

    for i in range(1, len(targetLine_2.split(','))):
        LastMateList_2[i - 1] = targetLine_2.split(',')[i]
    Date_2 = targetLine_2.split(',')[0]
    print("前天的值班日期:", Date_2)
    print("前天的值班人员", LastMateList_2)
    f.write('\n' + '2天前的值班人员：' + str(LastMateList_2))

    for i in range(1, len(targetLine_3.split(','))):
        LastMateList_3[i - 1] = targetLine_3.split(',')[i]
    Date_3 = targetLine_3.split(',')[0]
    print("大前天的值班日期:", Date_3)
    print("大前天的值班人员", LastMateList_3)
    f.write('\n' + '3天前的值班人员：' + str(LastMateList_3))

    if Date_1 in holiday_lastday:
        LastMateList =  LastMateList_2 + LastMateList_3
    elif Date_2 in holiday_lastday:
        LastMateList = LastMateList_1  + LastMateList_3
    elif Date_3 in holiday_lastday:
        LastMateList = LastMateList_1 + LastMateList_2
    else:
        LastMateList = LastMateList_1 + LastMateList_2 + LastMateList_3

    print("前3天的值班人员：",LastMateList)
    f.write('\n' + '前3天的值班人员：' + str(LastMateList))
    csvfile.close()
    #######################从历史数据中提取最后一次计数器###########
    with open("D:\\dutyInfo\\duty_counter.csv")  as csvfile:
        reader = csv.reader(csvfile)
        TotalLines = csvfile.readlines()

    # added by songml 20190126
    targetLine_small_fri = TotalLines[-7]  # 周五夜班
    # added by songml 20190126

    targetLine_small_mon = TotalLines[-6]  # 周一小夜班
    targetLine_hekou = TotalLines[-5]  # 河口值班计数器
    targetLine_manager = TotalLines[-4]  # 值班经理计数器
    targetLine_big = TotalLines[-3]  # 大夜班计数器
    targetLine_small = TotalLines[-2]  # 小夜班计数器

    # added by songml 20190126
    targetLine_small_fri = "".join(targetLine_small_fri.split())  # 去掉无效字符
    # added by songml 20190126

    targetLine_small_mon = "".join(targetLine_small_mon.split())  # 去掉无效字符
    targetLine_hekou = "".join(targetLine_hekou.split())  # 去掉无效字符
    targetLine_manager = "".join(targetLine_manager.split())  # 去掉无效字符
    targetLine_big = "".join(targetLine_big.split())  # 去掉无效字符
    targetLine_small = "".join(targetLine_small.split())  # 去掉无效字符

    csvfile.close()

    ##########################初始化员工列表#####################
    # 主岗列表
    list_main = config.list_main
    # 主岗人数
    main_amount = len(list_main)
    # 新人列表
    list_new = config.list_new
    # 新人人数
    new_amount = len(list_new)

    # 女员工列表
    list_women = config.list_women
    # 女员工人数
    women_amount = len(list_women)
    # 非主岗老员工
    list_group_A = config.list_group_A
    list_group_B = config.list_group_B
    list_group_C = config.list_group_C
    list_group_D = config.list_group_D
    list_group_E = config.list_group_E
    list_group_F = config.list_group_F
    list_group_G = config.list_group_G

    # 老员工总人数
    old_amount = len(list_group_A) + len(list_group_B) + len(list_group_C) + len(list_group_D) + \
                 len(list_group_E) + len(list_group_F) +  len(list_group_G)
    # 除去网络和应用的老员工数量
    old_other_amount = len(list_group_A) + len(list_group_D) + len(list_group_E) + len(list_group_F) + \
                       len(list_group_G)
    # 所有员工数量
    total = old_amount + main_amount + new_amount
    print("参与排班人员总数：", total)
    f.write('\n' + '参与排班人员总数：' + str(total))

    # 初始化每天的值班名单
    duty = []
    # 初始化每天的值班名单
    duty_group = [0, 0, 0, 0, 0, 0]
    # 初始化每天按顺序导出到csv的值班名单
    duty_result = [0, 0, 0, 0, 0, 0, 0]
    #每天主岗的人数
    chief_amout=1

    ############################计数器###########################

    ######人员列表####
    map = config.map

    # 自2018年9月新版排班上线以来，每个人夜盘交易日周五的计数器，VBA统计了6个月的
    # 从2019年3月开始，正式纳入周五夜班计数
    staff_small_fri = {}
    HistoryDate_small_fri = []
    for i in range(1, total + 1):
        HistoryDate_small_fri.append(int(targetLine_small_fri.split(',')[i]))
        staff_small_fri.update({map[i - 1]: HistoryDate_small_fri[i - 1]})
    print("周五夜班值班的历史计数器:", staff_small_fri)
    f.write('\n' + '周五夜班值班的历史计数器：' + str(staff_small_fri))

    # 每个人大夜班的计数器,从历史数据中导入，作为此次排班的依据
    staff_full_night = {}
    HistoryDate_full_night = []
    f.write('\n' + 'test=====' + str(targetLine_big))
    for i in range(1, total + 1):
        HistoryDate_full_night.append(int(targetLine_big.split(',')[i]))
        staff_full_night.update({map[i - 1]: HistoryDate_full_night[i - 1]})
    print("大夜班的历史计数器:", staff_full_night)
    f.write('\n' + '大夜班的历史计数器：' + str(staff_full_night))

    # 值班经理计数器
    staff_manager = {}
    HistoryDate_manager = []
    for i in range(1, total + 1):
        HistoryDate_manager.append(int(targetLine_manager.split(',')[i]))
        staff_manager.update({map[i - 1]: HistoryDate_manager[i - 1]})
    print("值班经理的历史计数器:", staff_manager)
    f.write('\n' + '值班经理的历史计数器：' + str(staff_manager))

    # 河口值班计数器
    staff_hekou = {}
    HistoryDate_hekou = []
    for i in range(1, total + 1):
        HistoryDate_hekou.append(int(targetLine_hekou.split(',')[i]))
        staff_hekou.update({map[i - 1]: HistoryDate_hekou[i - 1]})
    print("河口值班的历史计数器:", staff_hekou)
    f.write('\n' + '河口值班的历史计数器：' + str(staff_hekou))

    # 周一小夜班值班计数器
    # 此计数器也即节假日后首日计数器，by songml 20190122
    staff_small_mon = {}
    HistoryDate_small_mon = []
    for i in range(1, total + 1):
        HistoryDate_small_mon.append(int(targetLine_small_mon.split(',')[i]))
        staff_small_mon.update({map[i - 1]: HistoryDate_small_mon[i - 1]})
    print("周一小夜班值班的历史计数器:", staff_small_mon)
    f.write('\n' + '周一小夜班值班的历史计数器：' + str(staff_small_mon))

    # 小夜班值班计数器
    staff_small = {}
    HistoryDate_small = []
    for i in range(1, total + 1):
        HistoryDate_small.append(int(targetLine_small.split(',')[i]))
        staff_small.update({map[i - 1]: HistoryDate_small[i - 1]})
    print("小夜班的历史计数器:", staff_small)
    f.write('\n' + '小夜班的历史计数器：' + str(staff_small))



    # 主岗的夜班总数量
    staff_chief_night = {
                         'A1': staff_small.get('A1') + staff_full_night.get('A1'), \
                         'A2': staff_small.get('A2') + staff_full_night.get('A2'), \
                         'B1': staff_small.get('B1') + staff_full_night.get('B1'), \
                         'C1': staff_small.get('C1') + staff_full_night.get('C1'), \
                         'D1': staff_small.get('D1') + staff_full_night.get('D1'), \
                         'D2': staff_small.get('D2') + staff_full_night.get('D2'), \
                         'E1': staff_small.get('E1') + staff_full_night.get('E1'), \
                         'F1': staff_small.get('F1') + staff_full_night.get('F1'), \
                         'G1': staff_small.get('G1') + staff_full_night.get('G1'), \
                         'H1': staff_small.get('H1') + staff_full_night.get('H1'), \
                         'I1': staff_small.get('I1') + staff_full_night.get('I1'), \
                         'J1': staff_small.get('J1') + staff_full_night.get('J1')
    }
    # 随机排列
    staff_chief_night_random={}
    staff_chief_night_list = list(staff_chief_night.keys())
    random.shuffle(staff_chief_night_list)
    for i in staff_chief_night_list:
        staff_chief_night_random.update({i: staff_chief_night.get(i)})

    print("主岗夜班总数量：",staff_chief_night)
    f.write('\n' + '主岗夜班总数量：' + str(staff_chief_night))
    print("主岗夜班总数量,乱序：", staff_chief_night_random)
    f.write('\n' + '主岗夜班总数量,乱序：' + str(staff_chief_night_random))

    # 非主岗老员工的夜班总数量,单独列出网络和应用岗位
    # 网络岗位的非主岗老员工的夜班总数量
    staff_old_night_B = {
                         'B2': staff_small.get('B2') + staff_full_night.get('B2'), \
                         'B3': staff_small.get('B3') + staff_full_night.get('B3'), \
                         'B4': staff_small.get('B4') + staff_full_night.get('B4'), \
                         'B5': staff_small.get('B5') + staff_full_night.get('B5'), \
                         'B6': staff_small.get('B6') + staff_full_night.get('B6')
                                }
    # 随机排列
    staff_old_night_B_random={}
    staff_old_night_B_list = list(staff_old_night_B.keys())
    random.shuffle(staff_old_night_B_list)
    for i in staff_old_night_B_list:
        staff_old_night_B_random.update({i: staff_old_night_B.get(i)})

    print("网络夜班总数量：", staff_old_night_B)
    f.write('\n' + '网络夜班总数量：' + str(staff_old_night_B))
    print("网络夜班总数量,乱序：", staff_old_night_B_random)
    f.write('\n' + '网络夜班总数量,乱序：' + str(staff_old_night_B_random))

    # 应用岗位非主岗老员工的夜班总数量
    staff_old_night_C = {
                         'C2': staff_small.get('C2') + staff_full_night.get('C2'), \
                         # C3 与 F5 对调后C3变为松健  F5 变为嵩哥，C3不是应用岗位老员工，因此需要去掉
    #                     'C3': staff_small.get('C3') + staff_full_night.get('C3'), \
                         'C4': staff_small.get('C4') + staff_full_night.get('C4'), \
                         'C5': staff_small.get('C5') + staff_full_night.get('C5')
                                }
    #随机排列
    staff_old_night_C_random={}
    staff_old_night_C_list = list(staff_old_night_C.keys())
    random.shuffle(staff_old_night_C_list)
    for i in staff_old_night_C_list:
        staff_old_night_C_random.update({i: staff_old_night_C.get(i)})

    print("应用夜班总数量：", staff_old_night_C)
    f.write('\n' + '应用夜班总数量：' + str(staff_old_night_C))
    print("应用夜班总数量,乱序：", staff_old_night_C_random)
    f.write('\n' + '应用夜班总数量,乱序：' + str(staff_old_night_C_random))


    # 除了应用和网络的非主岗老员工的夜班总数量
    staff_old_night_other = {
                             'A3': staff_small.get('A3') + staff_full_night.get('A3'), \
                             'A4': staff_small.get('A4') + staff_full_night.get('A4'), \
                             'A5': staff_small.get('A5') + staff_full_night.get('A5'), \
                             'D3': staff_small.get('D3') + staff_full_night.get('D3'), \
                             'D4': staff_small.get('D4') + staff_full_night.get('D4'), \
                             'E2': staff_small.get('E2') + staff_full_night.get('E2'), \
                             'E3': staff_small.get('E3') + staff_full_night.get('E3'), \
                             'E4': staff_small.get('E4') + staff_full_night.get('E4'), \
                             'F2': staff_small.get('F2') + staff_full_night.get('F2'), \
                             'F3': staff_small.get('F3') + staff_full_night.get('F3'), \
                             'F4': staff_small.get('F4') + staff_full_night.get('F4'), \
                             # 与C3对调，F5变为嵩哥，因此添加嵩哥 added by songml 20190126
                             'F5': staff_small.get('F5') + staff_full_night.get('F5'), \
                             'G2': staff_small.get('G2') + staff_full_night.get('G2')
                                       }
    #随机排列
    staff_old_night_other_random={}
    staff_old_night_other_list = list(staff_old_night_other.keys())
    random.shuffle(staff_old_night_other_list)
    for i in staff_old_night_other_list:
        staff_old_night_other_random.update({i: staff_old_night_other.get(i)})

    print("其他老员工夜班总数量：", staff_old_night_other)
    f.write('\n' + '其他老员工夜班总数量：' + str(staff_old_night_other))
    print("其他老员工夜班总数量,乱序：", staff_old_night_other_random)
    f.write('\n' + '其他老员工夜班总数量,乱序：' + str(staff_old_night_other_random))

    #各个岗位老员工+主岗的夜班总数量
    # 由于浅拷贝不会拷贝子对象，因此需要再update一次，以后再试的时候可以考虑使用deepcopy方法 by songml 20190122
    staff_ChiefAndOtherOld=staff_old_night_other_random.copy()
    staff_ChiefAndOtherOld.update(staff_chief_night_random)

    # 随机排列
    staff_ChiefAndOtherOld_random = {}
    staff_ChiefAndOtherOld_list = list(staff_ChiefAndOtherOld.keys())
    random.shuffle(staff_ChiefAndOtherOld_list)
    for i in staff_ChiefAndOtherOld_list:
        staff_ChiefAndOtherOld_random.update({i: staff_ChiefAndOtherOld.get(i)})

    print("各个岗位老员工+主岗的夜班总数量：", staff_ChiefAndOtherOld)
    f.write('\n' + '各个岗位老员工+主岗的夜班总数量：' + str(staff_ChiefAndOtherOld))
    print("各个岗位老员工+主岗的夜班总数量,乱序：", staff_ChiefAndOtherOld_random)
    f.write('\n' + '各个岗位老员工+主岗的夜班总数量,乱序：' + str(staff_ChiefAndOtherOld_random))

    # 新员工的夜班总数量
    staff_new_night = {
                       'A6': staff_small.get('A6') + staff_full_night.get('A6'), \
                       'B7': staff_small.get('B7') + staff_full_night.get('B7'), \
                       'C6': staff_small.get('C6') + staff_full_night.get('C6'), \
                       'C7': staff_small.get('C7') + staff_full_night.get('C7'), \
                       'H2': staff_small.get('H2') + staff_full_night.get('H2'), \
                       'H3': staff_small.get('H3') + staff_full_night.get('H3'), \
                       'I2': staff_small.get('I2') + staff_full_night.get('I2'), \
                       'I3': staff_small.get('I3') + staff_full_night.get('I3'), \
        #晓丽不再参与值班，因此去掉I4 deleted by songml 20190126
        #               'I4': staff_small.get('I4') + staff_full_night.get('I4'), \
                       'C3': staff_small.get('C3') + staff_full_night.get('C3')
                            }
    # 随机排列
    staff_new_night_random = {}
    staff_new_night_list = list(staff_new_night.keys())
    random.shuffle(staff_new_night_list)
    for i in staff_new_night_list:
        staff_new_night_random.update({i: staff_new_night.get(i)})

    print("新人夜班总数量：", staff_new_night)
    f.write('\n' + '新人夜班总数量：' + str(staff_new_night))
    print("新人夜班总数量,乱序：", staff_new_night_random)
    f.write('\n' + '新人夜班总数量,乱序：' + str(staff_new_night_random))

    ################################排序##################################################
    # 根据夜班总数量排的   主岗列表，按值夜班数量从小到大排序
    # 判断当天如果是周一或者节假日后首日(包括节假后首日是周五的情况)20190123 by songml
    f.write("\n=========>>>>>>>>>>>> SpecialDay is " + str(Specialday) + "  WeekDay is " + str(Weekday))
    if (Specialday == 2) or (Specialday == 0 and Weekday == 1):
        # 按照夜班总数及周一节假日首日进行排序 开始 20190123 by songml end
        # 遍历主岗哈希，结合map,生成新的基于周一夜班的哈希，总共生成3个列表
        ### new added
        if Weekday == 5:
            tmplist = []
            for staff in staff_chief_night_random.keys():
                tmplist.append((staff_chief_night_random.get(staff), staff_small_mon.get(staff)
                                , staff_small_fri.get(staff), staff))

            staff_chief_night_inorder = sorted(tmplist, key=lambda x: (x[0], x[1], x[2]))
            f.write('\n' + '+++ 完整版排序列表=====主岗列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_chief_night_inorder))
            ### new added
            for i in range(len(staff_chief_night_inorder)):
                # 值班人员变为数组第4个参数
                staff_chief_night_inorder[i] = staff_chief_night_inorder[i][3]

            f.write('\n' + '+++主岗列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_chief_night_inorder))

            # 根据夜班总数量排的   除去网络和应用老员工列表，按值夜班数量从小到大排序

            ### new added
            tmplist2 = []
            for staff in staff_old_night_other_random.keys():
                tmplist2.append((staff_old_night_other_random.get(staff), staff_small_mon.get(staff)
                                 , staff_small_fri.get(staff), staff))
            staff_old_night_other_inorder = sorted(tmplist2, key=lambda x: (x[0], x[1], x[2]))
            ### new added
            f.write('\n' + '+++ 完整版排序列表 ===== 除去网络和应用老员工列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(
                staff_old_night_other_inorder))

            for i in range(len(staff_old_night_other_inorder)):
                staff_old_night_other_inorder[i] = staff_old_night_other_inorder[i][3]

            f.write('\n' + '+++除去网络和应用老员工列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_other_inorder))

            # 根据夜班总数量排的   新员工列表，按值夜班数量从小到大排序
            ### new added
            tmplist3 = []
            for staff in staff_new_night_random.keys():
                tmplist3.append((staff_new_night_random.get(staff), staff_small_mon.get(staff)
                                 , staff_small_fri.get(staff), staff))
            staff_new_night_inorder = sorted(tmplist3, key=lambda x: (x[0], x[1], x[2]))

            f.write('\n' + '+++ 完整版排序列表 ===== 新员工列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_new_night_inorder))

            ### new added

            for i in range(len(staff_new_night_inorder)):
                staff_new_night_inorder[i] = staff_new_night_inorder[i][3]

            f.write('\n' + '+++ 新员工列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_new_night_inorder))

            # 根据夜班总数量排的   网络岗位列表，按值夜班数量从小到大排序

            tmplist4 = []
            for staff in staff_old_night_B_random.keys():
                tmplist4.append((staff_old_night_B_random.get(staff), staff_small_mon.get(staff)
                                 , staff_small_fri.get(staff), staff))
            staff_old_night_B_inorder = sorted(tmplist4, key=lambda x: (x[0], x[1], x[2]))
            f.write('\n' + '+++ 完整版排序列表 ===== 网络岗位列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_B_inorder))

            ### new added
            for i in range(len(staff_old_night_B_inorder)):
                staff_old_night_B_inorder[i] = staff_old_night_B_inorder[i][3]

            f.write('\n' + '+++ 网络岗位列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_B_inorder))

            # 根据夜班总数量排的   应用岗位列表，按值夜班数量从小到大排序
            tmplist5 = []
            for staff in staff_old_night_C_random.keys():
                tmplist5.append((staff_old_night_C_random.get(staff), staff_small_mon.get(staff)
                                 , staff_small_fri.get(staff), staff))
            staff_old_night_C_inorder = sorted(tmplist5, key=lambda x: (x[0], x[1], x[2]))
            f.write('\n' + '+++ 完整版排序列表 ===== 应用岗位列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_C_inorder))

            ### new added

            for i in range(len(staff_old_night_C_inorder)):
                staff_old_night_C_inorder[i] = staff_old_night_C_inorder[i][3]

            f.write('\n' + '+++ 应用岗位列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_C_inorder))

            # 根据夜班总数量排的   主岗和除了网络应用的老员工，按值夜班数量从小到大排序
            tmplist6 = []
            for staff in staff_ChiefAndOtherOld_random.keys():
                tmplist6.append((staff_ChiefAndOtherOld_random.get(staff), staff_small_mon.get(staff)
                                 , staff_small_fri.get(staff), staff))
            staff_ChiefAndOtherOld_inorder = sorted(tmplist6, key=lambda x: (x[0], x[1], x[2]))
            f.write('\n' + '+++ 完整版排序列表 ===== 主岗和除了网络应用的老员工，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(
                staff_ChiefAndOtherOld_inorder))

            ### new added
            for i in range(len(staff_ChiefAndOtherOld_inorder)):
                staff_ChiefAndOtherOld_inorder[i] = staff_ChiefAndOtherOld_inorder[i][3]

            f.write('\n' + '+++ 主岗和除了网络应用的老员工，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_ChiefAndOtherOld_inorder))
        else:
            tmplist = []
            for staff in staff_chief_night_random.keys():
                tmplist.append((staff_chief_night_random.get(staff), staff_small_mon.get(staff), staff))

            staff_chief_night_inorder = sorted(tmplist, key=lambda x: (x[0], x[1]))
            f.write('\n' + '+++ 完整版排序列表=====主岗列表，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_chief_night_inorder))
            ### new added
            for i in range(len(staff_chief_night_inorder)):
                # 值班人员变为数组第3个参数
                staff_chief_night_inorder[i] = staff_chief_night_inorder[i][2]

            f.write('\n' + '+++主岗列表，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_chief_night_inorder))

            # 根据夜班总数量排的   除去网络和应用老员工列表，按值夜班数量从小到大排序

            ### new added
            tmplist2 = []
            for staff in staff_old_night_other_random.keys():
                tmplist2.append((staff_old_night_other_random.get(staff), staff_small_mon.get(staff), staff))
            staff_old_night_other_inorder = sorted(tmplist2, key=lambda x: (x[0], x[1]))
            ### new added
            f.write('\n' + '+++ 完整版排序列表 ===== 除去网络和应用老员工列表，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_other_inorder))

            for i in range(len(staff_old_night_other_inorder)):
                staff_old_night_other_inorder[i] = staff_old_night_other_inorder[i][2]

            f.write('\n' + '+++除去网络和应用老员工列表，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_other_inorder))

            # 根据夜班总数量排的   新员工列表，按值夜班数量从小到大排序
            ### new added
            tmplist3 = []
            for staff in staff_new_night_random.keys():
                tmplist3.append((staff_new_night_random.get(staff), staff_small_mon.get(staff), staff))
            staff_new_night_inorder = sorted(tmplist3, key=lambda x: (x[0], x[1]))

            f.write('\n' + '+++ 完整版排序列表 ===== 新员工列表，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_new_night_inorder))

            ### new added

            for i in range(len(staff_new_night_inorder)):
                staff_new_night_inorder[i] = staff_new_night_inorder[i][2]

            f.write('\n' + '+++ 新员工列表，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_new_night_inorder))

            # 根据夜班总数量排的   网络岗位列表，按值夜班数量从小到大排序

            tmplist4 = []
            for staff in staff_old_night_B_random.keys():
                tmplist4.append((staff_old_night_B_random.get(staff), staff_small_mon.get(staff), staff))
            staff_old_night_B_inorder = sorted(tmplist4, key=lambda x: (x[0], x[1]))
            f.write('\n' + '+++ 完整版排序列表 ===== 网络岗位列表，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_B_inorder))

            ### new added
            for i in range(len(staff_old_night_B_inorder)):
                staff_old_night_B_inorder[i] = staff_old_night_B_inorder[i][2]

            f.write('\n' + '+++ 网络岗位列表，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_B_inorder))

            # 根据夜班总数量排的   应用岗位列表，按值夜班数量从小到大排序
            tmplist5 = []
            for staff in staff_old_night_C_random.keys():
                tmplist5.append((staff_old_night_C_random.get(staff), staff_small_mon.get(staff), staff))
            staff_old_night_C_inorder = sorted(tmplist5, key=lambda x: (x[0], x[1]))
            f.write('\n' + '+++ 完整版排序列表 ===== 应用岗位列表，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_C_inorder))

            ### new added

            for i in range(len(staff_old_night_C_inorder)):
                staff_old_night_C_inorder[i] = staff_old_night_C_inorder[i][2]

            f.write('\n' + '+++ 应用岗位列表，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_C_inorder))

            # 根据夜班总数量排的   主岗和除了网络应用的老员工，按值夜班数量从小到大排序
            tmplist6 = []
            for staff in staff_ChiefAndOtherOld_random.keys():
                tmplist6.append((staff_ChiefAndOtherOld_random.get(staff), staff_small_mon.get(staff), staff))
            staff_ChiefAndOtherOld_inorder = sorted(tmplist6, key=lambda x: (x[0], x[1]))
            f.write('\n' + '+++ 完整版排序列表 ===== 主岗和除了网络应用的老员工，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_ChiefAndOtherOld_inorder))

            ### new added
            for i in range(len(staff_ChiefAndOtherOld_inorder)):
                staff_ChiefAndOtherOld_inorder[i] = staff_ChiefAndOtherOld_inorder[i][2]

            f.write('\n' + '+++ 主岗和除了网络应用的老员工，按值夜班数量(及节假日首日数量进行排序)从小到大排序：' + str(staff_ChiefAndOtherOld_inorder))
        # 判断当天如果是周一或者节假日后首日20190123 by songml end
    # 判断当天如果是周五 2019
    elif (Specialday == 0 and Weekday == 5):
        # added by songml 20190126

        # 按照夜班总数及周五夜班数进行排序 开始 20190126 by songml end
        ### new added
        tmplist = []
        for staff in staff_chief_night_random.keys():
            tmplist.append((staff_chief_night_random.get(staff), staff_small_fri.get(staff), staff))

        staff_chief_night_inorder = sorted(tmplist, key=lambda x: (x[0], x[1]))
        f.write('\n' + '+++ 完整版排序列表=====主岗列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_chief_night_inorder))
        ### new added
        for i in range(len(staff_chief_night_inorder)):
            # 值班人员变为数组第3个参数
            staff_chief_night_inorder[i] = staff_chief_night_inorder[i][2]

        f.write('\n' + '+++主岗列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_chief_night_inorder))

        # 根据夜班总数量排的   除去网络和应用老员工列表，按值夜班数量从小到大排序

        ### new added
        tmplist2 = []
        for staff in staff_old_night_other_random.keys():
            tmplist2.append((staff_old_night_other_random.get(staff), staff_small_fri.get(staff), staff))
        staff_old_night_other_inorder = sorted(tmplist2, key=lambda x: (x[0], x[1]))
        ### new added
        f.write('\n' + '+++ 完整版排序列表 ===== 除去网络和应用老员工列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_other_inorder))

        for i in range(len(staff_old_night_other_inorder)):
            staff_old_night_other_inorder[i] = staff_old_night_other_inorder[i][2]

        f.write('\n' + '+++除去网络和应用老员工列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_other_inorder))

        # 根据夜班总数量排的   新员工列表，按值夜班数量从小到大排序
        ### new added
        tmplist3 = []
        for staff in staff_new_night_random.keys():
            tmplist3.append((staff_new_night_random.get(staff), staff_small_fri.get(staff), staff))
        staff_new_night_inorder = sorted(tmplist3, key=lambda x: (x[0], x[1]))

        f.write('\n' + '+++ 完整版排序列表 ===== 新员工列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_new_night_inorder))

        ### new added

        for i in range(len(staff_new_night_inorder)):
            staff_new_night_inorder[i] = staff_new_night_inorder[i][2]

        f.write('\n' + '+++ 新员工列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_new_night_inorder))

        # 根据夜班总数量排的   网络岗位列表，按值夜班数量从小到大排序

        tmplist4 = []
        for staff in staff_old_night_B_random.keys():
            tmplist4.append((staff_old_night_B_random.get(staff), staff_small_fri.get(staff), staff))
        staff_old_night_B_inorder = sorted(tmplist4, key=lambda x: (x[0], x[1]))
        f.write('\n' + '+++ 完整版排序列表 ===== 网络岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_B_inorder))

        ### new added
        for i in range(len(staff_old_night_B_inorder)):
            staff_old_night_B_inorder[i] = staff_old_night_B_inorder[i][2]

        f.write('\n' + '+++ 网络岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_B_inorder))

        # 根据夜班总数量排的   应用岗位列表，按值夜班数量从小到大排序
        tmplist5 = []
        for staff in staff_old_night_C_random.keys():
            tmplist5.append((staff_old_night_C_random.get(staff), staff_small_fri.get(staff), staff))
        staff_old_night_C_inorder = sorted(tmplist5, key=lambda x: (x[0], x[1]))
        f.write('\n' + '+++ 完整版排序列表 ===== 应用岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_C_inorder))

        ### new added

        for i in range(len(staff_old_night_C_inorder)):
            staff_old_night_C_inorder[i] = staff_old_night_C_inorder[i][2]

        f.write('\n' + '+++ 应用岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_C_inorder))

        # 根据夜班总数量排的   主岗和除了网络应用的老员工，按值夜班数量从小到大排序
        tmplist6 = []
        for staff in staff_ChiefAndOtherOld_random.keys():
            tmplist6.append((staff_ChiefAndOtherOld_random.get(staff), staff_small_fri.get(staff), staff))
        staff_ChiefAndOtherOld_inorder = sorted(tmplist6, key=lambda x: (x[0], x[1]))
        f.write('\n' + '+++ 完整版排序列表 ===== 主岗和除了网络应用的老员工，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_ChiefAndOtherOld_inorder))

        ### new added
        for i in range(len(staff_ChiefAndOtherOld_inorder)):
            staff_ChiefAndOtherOld_inorder[i] = staff_ChiefAndOtherOld_inorder[i][2]

        f.write('\n' + '+++ 主岗和除了网络应用的老员工，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_ChiefAndOtherOld_inorder))
        # 判断当天如果是周一或者节假日后首日(非周五)20190123 by songml end

        # added by songml 20190126
    else:

        # 其它日子
        staff_chief_night_inorder = sorted(zip(staff_chief_night_random.values(), staff_chief_night_random.keys()),key=lambda x:x[0])
        for i in range(len(staff_chief_night_inorder)):
            staff_chief_night_inorder[i] = staff_chief_night_inorder[i][1]

        f.write('\n' + '主岗列表，按值夜班数量从小到大排序：' + str(staff_chief_night_inorder))

        # 根据夜班总数量排的   除去网络和应用老员工列表，按值夜班数量从小到大排序
        staff_old_night_other_inorder = sorted(zip(staff_old_night_other_random.values(), staff_old_night_other_random.keys()),key=lambda x:x[0])
        for i in range(len(staff_old_night_other_inorder)):
            staff_old_night_other_inorder[i] = staff_old_night_other_inorder[i][1]

        f.write('\n' + '除去网络和应用老员工列表，按值夜班数量从小到大排序：' + str(staff_old_night_other_inorder))

        # 根据夜班总数量排的   新员工列表，按值夜班数量从小到大排序
        staff_new_night_inorder = sorted(zip(staff_new_night_random.values(), staff_new_night_random.keys()),key=lambda x:x[0])
        for i in range(len(staff_new_night_inorder)):
            staff_new_night_inorder[i] = staff_new_night_inorder[i][1]

        f.write('\n' + '新员工列表，按值夜班数量从小到大排序：' + str(staff_new_night_inorder))

        # 根据夜班总数量排的   网络岗位列表，按值夜班数量从小到大排序
        staff_old_night_B_inorder = sorted(zip(staff_old_night_B_random.values(), staff_old_night_B_random.keys()),key=lambda x:x[0])
        for i in range(len(staff_old_night_B_inorder)):
            staff_old_night_B_inorder[i] = staff_old_night_B_inorder[i][1]

        f.write('\n' + '网络岗位列表，按值夜班数量从小到大排序：' + str(staff_old_night_B_inorder))

        # 根据夜班总数量排的   应用岗位列表，按值夜班数量从小到大排序
        staff_old_night_C_inorder = sorted(zip(staff_old_night_C_random.values(), staff_old_night_C_random.keys()),key=lambda x:x[0])
        for i in range(len(staff_old_night_C_inorder)):
            staff_old_night_C_inorder[i] = staff_old_night_C_inorder[i][1]

        f.write('\n' + '应用岗位列表，按值夜班数量从小到大排序：' + str(staff_old_night_C_inorder))

        # 根据夜班总数量排的   主岗和除了网络应用的老员工，按值夜班数量从小到大排序
        staff_ChiefAndOtherOld_inorder = sorted(zip(staff_ChiefAndOtherOld_random.values(), staff_ChiefAndOtherOld_random.keys()),key=lambda x:x[0])
        for i in range(len(staff_ChiefAndOtherOld_inorder)):
            staff_ChiefAndOtherOld_inorder[i] = staff_ChiefAndOtherOld_inorder[i][1]

        f.write('\n' + '主岗和除了网络应用的老员工，按值夜班数量从小到大排序：' + str(staff_ChiefAndOtherOld_inorder))

    ###################选出6个值班人员#############################
    ##########################################################
    ############将值班数量最少的主岗选出，作为值班第一天的岗位################
    ############ 添加女生计数器 ########
    ############ 添加女生计数器 counterWoman ########
    duty_women_cnt=0 #added by songml

    # 主岗不能是昨天值班的人员
    for i in range(main_amount):
        if staff_chief_night_inorder[i] in LastMateList:
            continue
        else:
            duty.append(staff_chief_night_inorder[i])
            # added by songml for duty_women_cnt 20181214
            if staff_chief_night_inorder[i] in list_women:
                f.write('\n' + '选中的女生为：' + staff_chief_night_inorder[i])
                duty_women_cnt += 1
            break


    ###################选出当天的值班新人###########################
    for i in range(new_amount):
        if staff_new_night_inorder[i] in LastMateList:
            continue
        else:
            if duty[0][0] == staff_new_night_inorder[i][0]:
                continue  # 如果值班主岗和新员工顺序表中的第一位是一个岗位的，则当日新员工为表中第二个人。
            else:
                duty.append(staff_new_night_inorder[i])  # 如果不相同，则当日新员工为表中第一位
                # added by songml for duty_women_cnt 20181214
                if staff_new_night_inorder[i] in list_women:
                    f.write('\n' + '选中的女生为：' + staff_new_night_inorder[i])
                    duty_women_cnt += 1
                break

    f.write('\n' + '选过主岗、新人的新版值班表：' + str(duty))
    ###################先判断是否有网络和应用岗位,然后选出余下的值班人员(新算法)######################
    ##############################################################################

    f.write('\n' + '选过主岗和新人后女生的人数===========：' + str(duty_women_cnt))
    if (duty[0][0] != "B") and (duty[1][0] != "B"):
        print("没有网络，额外添加")
        for i in range(len(staff_old_night_B_inorder)):  # 按照夜班数量的从小到大安排网络岗位值班,并确保当天值班人员不是一个岗位的
            if staff_old_night_B_inorder[i] in LastMateList:  # 判断和上一日值班人员是否重复
                continue
            else:

                # added by songml for duty_women_cnt 20181214
                if staff_old_night_B_inorder[i] in list_women:

                    if duty_women_cnt == 2:
                        f.write('\n' + ' 网络选人中 且这次选中的人为女生 但女生数已为2 跳过')
                        continue
                    else:
                        duty.append(staff_old_night_B_inorder[i])
                        f.write('\n' + '选中的女生为：' + staff_old_night_B_inorder[i])
                        duty_women_cnt += 1
                        break
                # added by songml for duty_women_cnt 20181214
                else:
                    duty.append(staff_old_night_B_inorder[i])
                    break
                # break
    f.write('\n' + '选过网络岗位后女生人数===========：' + str(duty_women_cnt))
    if (duty[0][0] != "C") and (duty[1][0] != "C"):
        print("没有应用，额外添加")
        for i in range(len(staff_old_night_C_inorder)):  # 按照夜班数量的从小到大安排网络岗位值班,并确保当天值班人员不是一个岗位的
            if staff_old_night_C_inorder[i] in LastMateList:  # 判断和上一日值班人员是否重复
                continue
            else:

                # added by songml for duty_women_cnt 20181214
                if staff_old_night_C_inorder[i] in list_women:
                    if duty_women_cnt == 2:
                        f.write('\n' + ' 应用选人中 且这次选中的人为女生 但女生数已为2 跳过')
                        continue
                    else:
                        duty.append(staff_old_night_C_inorder[i])
                        f.write('\n' + '选中的女生为：' + staff_old_night_C_inorder[i])
                        duty_women_cnt += 1
                        break
                # added by songml for duty_women_cnt 20181214
                else:
                    duty.append(staff_old_night_C_inorder[i])
                    break
                # break
    ##############转换为新的值班表，列表形式############
    f.write('\n' + '选过主岗、新人、网络、应用的新版值班表：' + str(duty))
    for i in range(len(duty)):
        duty_group[i] = duty[i][0]
    ###################################################
    f.write('\n' + '选过应用岗位后女生人数===========：' + str(duty_women_cnt))
    # 以下为除去网络和应用外的其他岗位排班
    for m in range(len(duty), 6):
        for i in range(len(staff_ChiefAndOtherOld_inorder)):
            if staff_ChiefAndOtherOld_inorder[i] in LastMateList:  # 判断和上一日是否重复
                continue
            else:
                if staff_ChiefAndOtherOld_inorder[i][0] in duty_group:
                    continue
                #主岗人数大于2人就不选主岗了
                else:
                    if staff_ChiefAndOtherOld_inorder[i] in list_main:
                        if chief_amout==1:
                            if staff_ChiefAndOtherOld_inorder[i] not in list_women:
                                duty.append(staff_ChiefAndOtherOld_inorder[i])
                                duty_group.append(staff_ChiefAndOtherOld_inorder[i][0])
                                chief_amout += 1
                                break
                            else:
                                if duty_women_cnt == 2:
                                    f.write('\n' + ' 已选了2个主岗 且这次选的人为女生 但女生数已为2 跳过')
                                    continue
                                else:
                                    duty.append(staff_ChiefAndOtherOld_inorder[i])
                                    duty_group.append(staff_ChiefAndOtherOld_inorder[i][0])
                                    f.write('\n' + '选中的女生为：' + staff_ChiefAndOtherOld_inorder[i])
                                    chief_amout += 1
                                    duty_women_cnt += 1
                                    break
                            # added by songml for duty_women_cnt 20181214
                        else:
                            continue
                    else:
                        # added by songml for duty_women_cnt 20181214
                        if staff_ChiefAndOtherOld_inorder[i] not in list_women:
                            duty.append(staff_ChiefAndOtherOld_inorder[i])
                            duty_group.append(staff_ChiefAndOtherOld_inorder[i][0])
                            break
                        else:
                            if duty_women_cnt == 2:
                                f.write('\n' + ' 除去网络和应用外选人 非主岗，且这次选中的人为女生 但女生数已为2 跳过')
                                continue
                            else:
                                duty.append(staff_ChiefAndOtherOld_inorder[i])
                                duty_group.append(staff_ChiefAndOtherOld_inorder[i][0])
                                f.write('\n' + '选中的女生为：' + staff_ChiefAndOtherOld_inorder[i])
                                duty_women_cnt += 1
                                break
                        # added by songml for duty_women_cnt 20181214
    f.write('\n' + '选过除去网络和应用外的其他岗位排班后女生人数===========：' + str(duty_women_cnt))
    #如果不满足6人值班要求，空余值班位置由主岗补上，此时主岗人数大于2人
    if len(duty)<6:
        for m in range(len(duty), 6):
            for i in range(len(staff_ChiefAndOtherOld_inorder)):
                if staff_ChiefAndOtherOld_inorder[i] in LastMateList:  # 判断和上一日是否重复
                    continue
                else:
                    if staff_ChiefAndOtherOld_inorder[i][0] in duty_group:
                        continue
                    # 主岗人数大于4人就不选主岗了
                    else:
                        if staff_ChiefAndOtherOld_inorder[i] in list_main:
                            if chief_amout <= 4:
                                if staff_ChiefAndOtherOld_inorder[i] not in list_women:
                                    duty.append(staff_ChiefAndOtherOld_inorder[i])
                                    duty_group.append(staff_ChiefAndOtherOld_inorder[i][0])
                                    chief_amout += 1
                                    break
                                else:
                                    if duty_women_cnt == 2:
                                        f.write('\n' + '<6 选中了主岗且 选中的人为女生 但女生数已为2 跳过')
                                        continue
                                    else:
                                        duty.append(staff_ChiefAndOtherOld_inorder[i])
                                        duty_group.append(staff_ChiefAndOtherOld_inorder[i][0])
                                        f.write('\n' + '选中的女生为：' + staff_ChiefAndOtherOld_inorder[i])
                                        chief_amout += 1
                                        duty_women_cnt += 1
                                        break

                            else:
                                continue
                        else:
                            if staff_ChiefAndOtherOld_inorder[i] not in list_women:
                                duty.append(staff_ChiefAndOtherOld_inorder[i])
                                duty_group.append(staff_ChiefAndOtherOld_inorder[i][0])
                                break
                            else:
                                if duty_women_cnt == 2:
                                    f.write('\n' + '<6 选中人没有主岗，选中的人为女生 但女生数已为2 跳过')
                                    continue
                                else:
                                    duty.append(staff_ChiefAndOtherOld_inorder[i])
                                    duty_group.append(staff_ChiefAndOtherOld_inorder[i][0])
                                    f.write('\n' + '选中的女生为：' + staff_ChiefAndOtherOld_inorder[i])
                                    duty_women_cnt += 1
                                    break
    f.write('\n' + '选择补齐6个人后女生人数===========：' + str(duty_women_cnt))

    print("新版值班表的人员结果，不含岗位:", duty)
    f.write('\n' + '今日主岗人数：' + str(chief_amout))
    f.write('\n' + '新版值班表的结果，不含岗位：' + str(duty))
    #6个人至此选择结束



    #######################################
    # 随机排列
    random.shuffle(duty)
    print("新版值班表的人员结果（随机）:", duty)
    f.write('\n' + '新版值班表的结果，不含岗位（随机）：' + str(duty))

    ###########################################################################
    ###########################################################################
    #########################河口、值班经理、大夜班、小夜班选择############################
    ###########当天可以去河口的人
    hekou = []
    hekou_dict = {}
    # 河口值班不可以是女生和主岗
    for i in duty:
        if i not in (list_women + list_main):
            hekou.append(i)

    for i in range(len(hekou)):
        hekou_dict.update({hekou[i]: staff_hekou.get(hekou[i])})

    hekou_dict_inorder = sorted(zip(hekou_dict.values(), hekou_dict.keys()),key=lambda x:x[0])

    print("河口的值班顺序:", hekou_dict_inorder)
    f.write('\n' + '河口的值班顺序：' + str(hekou_dict_inorder))

    duty_result[1] = hekou_dict_inorder[0][1]
    print("河口的值班人员：", hekou_dict_inorder[0][1])
    f.write('\n' + '河口的值班人员：' + str(hekou_dict_inorder[0][1]))

    ##############值班经理选择
    manager = []
    manager_dict = {}
    # 值班经理不是新人，不是河口值班人员
    for i in duty:
        if (i not in list_new) and (i != duty_result[1]):
            manager.append(i)

    for i in range(len(manager)):
        manager_dict.update({manager[i]: staff_manager.get(manager[i])})
    manager_dict_inorder = sorted(zip(manager_dict.values(), manager_dict.keys()),key=lambda x:x[0])

    print("值班经理的值班顺序:", manager_dict_inorder)
    f.write('\n' + '值班经理的值班顺序：' + str(manager_dict_inorder))

    duty_result[2] = manager_dict_inorder[0][1]
    print("值班经理:", manager_dict_inorder[0][1])
    f.write('\n' + '值班经理：' + str(manager_dict_inorder[0][1]))

    ########################################################
    ###########################考虑节假日的大小夜班排班#########################
    # 节日前一天，4个小夜班，计数器不加1
    if Specialday == 1:
        smallnight = []
        for i in duty:
            if (i != duty_result[2]) and (i != duty_result[1]):
                smallnight.append(i)
        # 小夜班
        duty_result[5] = smallnight[0]
        duty_result[6] = smallnight[1]

    # 节日后第一个交易日，全是大夜班，如果是周五，还是6个小夜班
    elif Specialday == 2:
        if Weekday == 5:
            ##############大夜班,不是值班经理，不是河口值班的
            fullnight = []
            fullnight_dict = {}

            for i in duty:
                if (i != duty_result[2]) and (i != duty_result[1]):
                    fullnight.append(i)
            for i in range(len(fullnight)):
                fullnight_dict.update({fullnight[i]: staff_full_night.get(fullnight[i])})
            fullnight_dict_inorder = sorted(zip(fullnight_dict.values(), fullnight_dict.keys()), key=lambda x: x[0])

            print("大夜班的值班顺序:", fullnight_dict_inorder)
            f.write('\n' + '大夜班的值班顺序：' + str(fullnight_dict_inorder))

            # 大夜班
            duty_result[3] = fullnight_dict_inorder[0][1]
            duty_result[4] = fullnight_dict_inorder[1][1]
            print("大夜班:", fullnight_dict_inorder[0][1], "+", fullnight_dict_inorder[1][1])
            f.write('\n' + '大夜班：' + str(fullnight_dict_inorder[0][1]) + '、' + str(fullnight_dict_inorder[1][1]))

            ######################小夜班
            duty_result[5] = fullnight_dict_inorder[2][1]
            duty_result[6] = fullnight_dict_inorder[3][1]
            print("小夜班:", fullnight_dict_inorder[2][1], "+", fullnight_dict_inorder[3][1])
            f.write('\n' + '小夜班：' + str(fullnight_dict_inorder[2][1]) + '、' + str(fullnight_dict_inorder[3][1]))

            ##########################################
            ##############计数器分别加1####################
            # 河口计数器
            staff_hekou[duty_result[1]] += 1
            # 值班经理计数器
            staff_manager[duty_result[2]] += 1

            # 大转小，按小夜班计数
            staff_small[duty_result[3]] += 1
            staff_small[duty_result[4]] += 1

            # 小夜班计数器
            staff_small[duty_result[1]] += 1
            staff_small[duty_result[2]] += 1
            staff_small[duty_result[5]] += 1
            staff_small[duty_result[6]] += 1

            ## 周五的计数器 added by songml 20190127
            staff_small_fri[duty_result[1]] += 1
            staff_small_fri[duty_result[2]] += 1
            staff_small_fri[duty_result[3]] += 1
            staff_small_fri[duty_result[4]] += 1
            staff_small_fri[duty_result[5]] += 1
            staff_small_fri[duty_result[6]] += 1
            f.write('\n' + '周五夜班后计数：'
                    + str(duty_result[1]) + '：' + str(staff_small_fri[duty_result[1]])
                    + str(duty_result[2]) + '：' + str(staff_small_fri[duty_result[2]])
                    + str(duty_result[3]) + '：' + str(staff_small_fri[duty_result[3]])
                    + str(duty_result[4]) + '：' + str(staff_small_fri[duty_result[4]])
                    + str(duty_result[5]) + '：' + str(staff_small_fri[duty_result[5]])
                    + str(duty_result[6]) + '：' + str(staff_small_fri[duty_result[6]])
                    )
            ## 周五的计数器 added by songml
            ## 周五的计数器 added by songml 20190127
        ####################################################
        #如果不是周五
        else:
            ##############大夜班,不是值班经理，不是河口值班的,不是应用，参与周一小夜班次数少的人
            smallnight_mon = []
            smallnight_mon_dict = {}
            for i in duty:
                if ((i != duty_result[2]) and (i != duty_result[1]) and (i[0] != "C")):
                    smallnight_mon.append(i)
            for i in range(len(smallnight_mon)):
                smallnight_mon_dict.update({smallnight_mon[i]: staff_small_mon.get(smallnight_mon[i])})
            smallnight_mon_dict_inorder = sorted(zip(smallnight_mon_dict.values(), smallnight_mon_dict.keys()), key=lambda x: x[0],reverse=True)

            f.write('\n' + '周一小夜班的值班数量，从大到小：' + str(smallnight_mon_dict_inorder))

            # 大夜班
            duty_result[3] = smallnight_mon_dict_inorder[0][1]
            duty_result[4] = smallnight_mon_dict_inorder[1][1]

            f.write('\n' + '大夜班：' + str(smallnight_mon_dict_inorder[0][1]) + '、' + str(smallnight_mon_dict_inorder[1][1]))

            ######################小夜班
            duty_result[5] = smallnight_mon_dict_inorder[2][1]
            # 如果这个是应用，则是启停，如果不是，应用在河口和值班经理位置上
            for i in duty:
                if i not in duty_result:
                    duty_result[6] = i
                    break
            f.write('\n' + '小夜班：' + duty_result[5] + '、' + duty_result[6])

            ##########################################
            ##############计数器分别加1####################
            # 河口计数器
            staff_hekou[duty_result[1]] += 1
            # 值班经理计数器
            staff_manager[duty_result[2]] += 1
            # 大夜班计数器
            staff_full_night[duty_result[3]] += 1
            staff_full_night[duty_result[4]] += 1

            # 小夜班计数器
            staff_small[duty_result[1]] += 1
            staff_small[duty_result[2]] += 1
            staff_small[duty_result[5]] += 1
            staff_small[duty_result[6]] += 1

            #周一小夜班计数器
            staff_small_mon[duty_result[1]] += 1
            staff_small_mon[duty_result[2]] += 1
            staff_small_mon[duty_result[5]] += 1
            staff_small_mon[duty_result[6]] += 1
            ##########################################

            ##########################################
    # 其他正常工作日
    elif Specialday == 0:
        # 周一6个大夜班
        if Weekday == 1:
            ##############大夜班,不是值班经理，不是河口值班的,不是应用，参与周一小夜班次数少的人
            smallnight_mon = []
            smallnight_mon_dict = {}
            for i in duty:
                if ((i != duty_result[2]) and (i != duty_result[1]) and (i[0] != "C")):
                    smallnight_mon.append(i)
            for i in range(len(smallnight_mon)):
                smallnight_mon_dict.update({smallnight_mon[i]: staff_small_mon.get(smallnight_mon[i])})
            smallnight_mon_dict_inorder = sorted(zip(smallnight_mon_dict.values(), smallnight_mon_dict.keys()),
                                                 key=lambda x: x[0], reverse=True)

            f.write('\n' + '周一小夜班的值班数量，从大到小：' + str(smallnight_mon_dict_inorder))

            # 大夜班
            duty_result[3] = smallnight_mon_dict_inorder[0][1]
            duty_result[4] = smallnight_mon_dict_inorder[1][1]

            f.write(
                '\n' + '大夜班：' + str(smallnight_mon_dict_inorder[0][1]) + '、' + str(smallnight_mon_dict_inorder[1][1]))

            ######################小夜班
            duty_result[5] = smallnight_mon_dict_inorder[2][1]
            # 如果这个是应用，则是启停，如果不是，应用在河口和值班经理位置上
            for i in duty:
                if i not in duty_result:
                    duty_result[6] = i
                    break
            f.write('\n' + '小夜班：' + duty_result[5] + '、' + duty_result[6])

            ##########################################
            ##############计数器分别加1####################
            # 河口计数器
            staff_hekou[duty_result[1]] += 1
            # 值班经理计数器
            staff_manager[duty_result[2]] += 1
            # 大夜班计数器
            staff_full_night[duty_result[3]] += 1
            staff_full_night[duty_result[4]] += 1

            # 小夜班计数器
            staff_small[duty_result[1]] += 1
            staff_small[duty_result[2]] += 1
            staff_small[duty_result[5]] += 1
            staff_small[duty_result[6]] += 1

            # 周一小夜班计数器
            staff_small_mon[duty_result[1]] += 1
            staff_small_mon[duty_result[2]] += 1
            staff_small_mon[duty_result[5]] += 1
            staff_small_mon[duty_result[6]] += 1

            ##########################################
        # 正常值班的大、小夜班
        else:
            ##############大夜班,不是值班经理，不是河口值班的
            fullnight = []
            fullnight_dict = {}

            for i in duty:
                if (i != duty_result[2]) and (i != duty_result[1]):
                    fullnight.append(i)
            for i in range(len(fullnight)):
                fullnight_dict.update({fullnight[i]: staff_full_night.get(fullnight[i])})
            fullnight_dict_inorder = sorted(zip(fullnight_dict.values(), fullnight_dict.keys()),key=lambda x:x[0])

            print("大夜班的值班顺序:", fullnight_dict_inorder)
            f.write('\n' + '大夜班的值班顺序：' + str(fullnight_dict_inorder))

            # 大夜班
            duty_result[3] = fullnight_dict_inorder[0][1]
            duty_result[4] = fullnight_dict_inorder[1][1]
            print("大夜班:", fullnight_dict_inorder[0][1], "+", fullnight_dict_inorder[1][1])
            f.write('\n' + '大夜班：' + str(fullnight_dict_inorder[0][1]) +'、'+ str(fullnight_dict_inorder[1][1]))

            ######################小夜班
            duty_result[5] = fullnight_dict_inorder[2][1]
            duty_result[6] = fullnight_dict_inorder[3][1]
            print("小夜班:", fullnight_dict_inorder[2][1], "+", fullnight_dict_inorder[3][1])
            f.write('\n' + '小夜班：' + str(fullnight_dict_inorder[2][1]) +'、'+ str(fullnight_dict_inorder[3][1]))

            ##########################################
            ##############计数器分别加1####################
            # 河口计数器
            staff_hekou[duty_result[1]] += 1
            # 值班经理计数器
            staff_manager[duty_result[2]] += 1

            if Weekday == 5:
                #大转小，按小夜班计数
                staff_small[duty_result[3]] += 1
                staff_small[duty_result[4]] += 1

                ## 周五的计数器 added by songml
                staff_small_fri[duty_result[1]] += 1
                staff_small_fri[duty_result[2]] += 1
                staff_small_fri[duty_result[3]] += 1
                staff_small_fri[duty_result[4]] += 1
                staff_small_fri[duty_result[5]] += 1
                staff_small_fri[duty_result[6]] += 1
                f.write('\n' + '周五夜班后计数：'
                        + str(duty_result[1]) + '：' + str(staff_small_fri[duty_result[1]])
                        + str(duty_result[2]) + '：' + str(staff_small_fri[duty_result[2]])
                        + str(duty_result[3]) + '：' + str(staff_small_fri[duty_result[3]])
                        + str(duty_result[4]) + '：' + str(staff_small_fri[duty_result[4]])
                        + str(duty_result[5]) + '：' + str(staff_small_fri[duty_result[5]])
                        + str(duty_result[6]) + '：' + str(staff_small_fri[duty_result[6]])
                        )
                ## 周五的计数器 added by songml
            else:
                # 正常大夜班计数
                staff_full_night[duty_result[3]] += 1
                staff_full_night[duty_result[4]] += 1

            # 小夜班计数器
            staff_small[duty_result[1]] += 1
            staff_small[duty_result[2]] += 1
            staff_small[duty_result[5]] += 1
            staff_small[duty_result[6]] += 1

    # 除此之外的为参数错误
    else:
        print("Specialday参数错误")
        f.write('\n' + 'Specialday参数错误' )
    ##################值班总数#########################
    # 所有夜班值班总数计数器
    Record_all = ["夜班总数"]
    for i in range(0, total):
        Record_all.append(staff_small[map[i]]+staff_full_night[map[i]])
    print("值班总数:", Record_all)
    ####################################################

    ########################当日排班,记录文件#######################
    duty_result[0] = StartDate  # 日期
    print("今日值班表(有顺序)：", duty_result)
    f.write('\n' + '今日值班表(有顺序)：' + str(duty_result)+'\n')
    # 将当日的值班人员写入schedule_edition1.csv######
    out = open("D:\\dutyInfo\\duty_schedule_raw.csv", "a", newline="")
    csv_writer = csv.writer(out, dialect="excel")
    csv_writer.writerow(duty_result)

    out.close()

    ####################################################
    ########################当日排班,给宋明霖的文件#######################
    duty_song=[0,0,0,0,0,0,0]
    duty_song[0] = StartDate  # 日期
    duty_song[1] = SongDict.get(duty_result[1])
    duty_song[2] = SongDict.get(duty_result[2])
    duty_song[3] = SongDict.get(duty_result[3])
    duty_song[4] = SongDict.get(duty_result[4])
    duty_song[5] = SongDict.get(duty_result[5])
    duty_song[6] = SongDict.get(duty_result[6])
    print("今日值班表,给宋老师的(有顺序)：", duty_song)
    f.write('\n' + '今日值班表,给宋老师的(有顺序)：' + str(duty_song) + '\n')
    # 将当日的值班人员写入schedule_edition1.csv######
    out = open("D:\\dutyInfo\\duty_schedule.csv", "a", newline="")
    csv_writer = csv.writer(out, dialect="excel")
    csv_writer.writerow(duty_song)

    out.close()

    #######################################################
    #####################写CSV值班计数#########################
    # 将每天的值班天数计数写入csv文件
    # 序号
    result_date = []
    result_date.append("日期")
    result_date.append(StartDate)

    ########### 添加周五的计数器 added by songml 20190127
    result_small_fri = []
    result_small_fri.append("周五夜班")
    for i in staff_small_fri.values():
        result_small_fri.append(i)
    ########## 添加周五的计数器 added by songml 20190127

    ###########
    result_small_mon = []
    result_small_mon.append("周一小夜班")
    for i in staff_small_mon.values():
        result_small_mon.append(i)

    ####################
    result_hekou = []
    result_hekou.append("河口")
    for i in staff_hekou.values():
        result_hekou.append(i)
    ###########
    result_manager = []
    result_manager.append("值班经理")
    for i in staff_manager.values():
        result_manager.append(i)
    ###########
    result_big = []
    result_big.append("大夜班")
    for i in staff_full_night.values():
        result_big.append(i)
    ###########
    result_small = []
    result_small.append("小夜班")
    for i in staff_small.values():
        result_small.append(i)

    ###########
    print("result_hekou:", result_hekou)

    out = open("D:\\dutyInfo\\duty_counter.csv", "a", newline="")
    csv_writer = csv.writer(out, dialect="excel")
    csv_writer.writerow(result_date)
    # counter.csv中添加周五计数器的行 added by songml 20190127
    csv_writer.writerow(result_small_fri)
    # counter.csv中添加周五计数器的行 added by songml 20190127
    csv_writer.writerow(result_small_mon)
    csv_writer.writerow(result_hekou)
    csv_writer.writerow(result_manager)
    csv_writer.writerow(result_big)
    csv_writer.writerow(result_small)
    csv_writer.writerow(Record_all)

    out.close()
    #日志关闭
    f.close()

# PaiBan("20181001",1, 0)
