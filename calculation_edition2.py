#!/usr/bin/python3
####################################################
##    date      editor                        action
## 20180707  李松健                     发布1.0版本
## 20180816  李松健  将节日前一天特殊处理，白班人员可以参加下一日的值班
## 20180904  李松健  将选过6个人后的值班表打乱顺序，避免后续职责选人时的固定顺序现象，例如之前河口都是优先选择新人
## 20180919  李松健  增加3个主岗霍伟、丁肇町、宋鹏程，每日值班主岗人数限制为2人以内
## 20180920  李松健  增加主岗张宁
## 20180927  李松健  将输入参数变为年、月，初始参数全部转移至config2.py文件
## 20180928  李松健  人员变化，删除于林立、李沛衡，其他人员重新排序，数据独立存储
## 20181009  李松健  增加日期判断，提示错误的日期输入，生成的csv文件存在D:\\dutyInfo；每日主岗在特殊情况可以为4人
## 20181017  李松健  增加周一小夜班计数器，节假日后第一天的小夜班采用计数器，周一小夜班的多的人值大夜班
## 20181024  李松健  周一小夜班计数器数据补充至2017年7月，增加李松健至值班人员表
## 20181214  宋明霖  夜班女生人数限制为最多2人
## 20190122  宋明霖  添加节假日后首日与周一合并作为【节假日后首日】进行计数，逻辑一并调整
## 20190125  宋明霖  添加周五计数器，CVS添加周五计数器，排完班后需要相应地计数。
## 20190126  宋明霖  组人员调整F5 李松健 <=> C3 范嵩  ==> C3 李松健, F5 范嵩，去掉I4
## 20190126  宋明霖  相应的角色也调整 git test 5
## 20190514  宋明霖  王欣(女）不再参加值班、李沛衡暂不参加值班，张驰、沈全从新员工转为老员工（可担任值班经理）
## 20190516  宋明霖  逻辑调整，原来单独选择新人，调整后：选择完主岗、网络、应用后，将主岗、非主岗人员（包括新人）混在一起选，新人只是角色（同女生)
## 20190516  宋明霖  晓梅由原来的G2变为C8 由质量管理岗位变为应用岗位
## 20190618  宋明霖  逻辑修改，河口变为白班，原来多个岗位归并为5个岗位：网络、应用、主机、数据库、安全，进行人员分组
## 20190619  宋明霖  主机 数据库 安全 分别按照日期的情况，依组别进行夜班计数排序选人；修改hardcode,依据config2里的配置进行随机打乱
## 20190620  宋明霖  选定河口值班人员（主岗、中层、春苗、韩婷除外），随机乱序，排序；不在昨天、今天（五人）之中，选择河口计数器最小的河口值班
##                    但是河口的夜班计数、周一及节假日后首日的计数、周五的计数均不再添加1；计划调整计数模式，每组15人
##                    已存在的人员在前，后面没分配的为none，补齐15人，这样配置文件好调整
## 20190625  宋明霖   添加河口白班节假日后首日计数器，添加夜盘值班监控组排他，添加夜盘值班OA组排他，添加夜盘值班总监助理排他
## 20190923  宋明霖   总监助理数据库排他那里有问题，staff_old_night_D_list 使用错误，应当使用staff_old_night_D_inorder
## 20200427  宋明霖   男王欣纳入河口白班 songml
## 20200520  宋明霖   值班的间隔尝试调整到间隔4天(原来为3天),以扩大值班间隔。使值班人员值班最少间隔7天。
import csv
import random
import config2


SongDict=config2.SongDictNew


#节假日的前一交易日
holiday_lastday = config2.holiday_lastday

def PaiBan(StartDate, Weekday, Specialday):

    #日志文件
    f = open("D:\\dutyInfo\\test.log", 'a')
    f.write('#################################################################################################' )
    f.write('\n'+'日志日期：'+StartDate)
    #####################从历史数据中提取最后一次的值班人员###########
    LastMateList_1 = [0, 0, 0, 0, 0, 0]
    LastMateList_2 = [0, 0, 0, 0, 0, 0]
    LastMateList_3 = [0, 0, 0, 0, 0, 0]
    # 倒数第四天 added by songml
    LastMateList_4 = [0, 0, 0, 0, 0, 0]
    with open("D:\\dutyInfo\\duty_schedule_raw.csv")  as csvfile:
        reader = csv.reader(csvfile)
        TotalLines = csvfile.readlines()
    #倒数第1天的值班人员
    targetLine_1 = TotalLines[-1]
    #倒数第2天的值班人员
    targetLine_2 = TotalLines[-2]
    #倒数第3天的值班人员
    targetLine_3 = TotalLines[-3]

    #倒数第4天的值班人员
    targetLine_4 = TotalLines[-4]


    targetLine_1 = "".join(targetLine_1.split())  # 去掉无效字符
    targetLine_2 = "".join(targetLine_2.split())  # 去掉无效字符
    targetLine_3 = "".join(targetLine_3.split())  # 去掉无效字符
    targetLine_4 = "".join(targetLine_4.split())  # 去掉无效字符

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

    for i in range(1, len(targetLine_4.split(','))):
        LastMateList_4[i - 1] = targetLine_4.split(',')[i]
    Date_4 = targetLine_4.split(',')[0]
    print("大前天的值班日期:", Date_4)
    print("大前天的值班人员", LastMateList_4)
    f.write('\n' + '4天前的值班人员：' + str(LastMateList_4))

    # 删除掉河口的人，因为河口是白班了，把河口值班排除在外进行选择
    LastMateList_1.remove(LastMateList_1[0])
    LastMateList_2.remove(LastMateList_2[0])
    LastMateList_3.remove(LastMateList_3[0])
    LastMateList_4.remove(LastMateList_4[0])
    f.write('\n' + '昨天除去河口的值班人员：' + str(LastMateList_1))
    f.write('\n' + '前天除去河口的值班人员：' + str(LastMateList_2))
    f.write('\n' + '大前天除去河口的值班人员：' + str(LastMateList_3))
    f.write('\n' + '大前天除去河口的值班人员：' + str(LastMateList_4))
    # if Date_1 in holiday_lastday:
    #     LastMateList =  LastMateList_2 + LastMateList_3
    # elif Date_2 in holiday_lastday:
    #     LastMateList = LastMateList_1 + LastMateList_3
    # elif Date_3 in holiday_lastday:
    #     LastMateList = LastMateList_1 + LastMateList_2
    # else:
    #     LastMateList = LastMateList_1 + LastMateList_2 + LastMateList_3
    # 节前最后一天也纳入，排除选项，否则会出现节前值班，节后第一天再次值班
    #LastMateList = LastMateList_1 + LastMateList_2 + LastMateList_3
    LastMateList = LastMateList_1 + LastMateList_2 + LastMateList_3 + LastMateList_4
    print("前4天的值班人员：",LastMateList)
    f.write('\n' + '前4天的值班人员：' + str(LastMateList))

    csvfile.close()
    #######################从历史数据中提取最后一次计数器###########
    with open("D:\\dutyInfo\\duty_counter.csv")  as csvfile:
        reader = csv.reader(csvfile)
        TotalLines = csvfile.readlines()

    #added by songml 20190620
    dutyNumLimit=75
    targetLine_Id = TotalLines[0]
    targetLine_Name = TotalLines[1]

    # added by songml 20190624
    targetLine_hekou_mon = TotalLines[-8]  # 周一节假日后河口值白班
    # added by songml 20190624

    # added by songml 20190126
    targetLine_small_fri = TotalLines[-7]  # 周五夜班
    # added by songml 20190126

    targetLine_small_mon = TotalLines[-6]  # 周一小夜班
    targetLine_hekou = TotalLines[-5]  # 河口值班计数器
    targetLine_manager = TotalLines[-4]  # 值班经理计数器
    targetLine_big = TotalLines[-3]  # 大夜班计数器
    targetLine_small = TotalLines[-2]  # 小夜班计数器

    # added by songml 20190126
    targetLine_hekou_mon = "".join(targetLine_hekou_mon.split())  # 去掉无效字符
    # added by songml 20190126

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
    list_main = config2.list_main
    # 主岗人数
    main_amount = len(list_main)
    # 新人列表
    list_new = config2.list_new
    # 新人人数
    new_amount = len(list_new)

    # 女员工列表
    list_women = config2.list_women

    # 监控组
    list_moni = config2.list_moni
    # OA组
    list_oa = config2.list_oa
    # 总监助理组
    list_da = config2.list_da
    # 不去河口的
    list_not_hekou = config2.list_not_hekou

    # 初始化每天的值班名单
    duty = []
    # 初始化每天的值班名单
    duty_group = [0, 0, 0, 0, 0, 0]
    # 初始化每天按顺序导出到csv的值班名单
    duty_result = [0, 0, 0, 0, 0, 0, 0]
    #每天主岗的人数
    chief_amout= 0

    ############################计数器###########################

    ######人员列表####
    #map = config2.map
    ###### 人员列表 不从config2中直接赋值，因为他包含了一些人没有
    map=[]

    # 自2018年9月新版排班上线以来，每个人夜盘交易日周五的计数器，VBA统计了6个月的
    # 从2019年3月开始，正式纳入周五夜班计数
    # 在counter 文件中查找名字非none的人，将其认为是有效的值班人员 by songml 20190620
    dutySeq=[]
    allmemberList=[]
    allmemberIdList = []
    for i in range(1, dutyNumLimit + 1):
        name = targetLine_Name.split(',')[i]
        memid = targetLine_Id.split(',')[i]
        allmemberList.append(name)
        allmemberIdList.append(memid)
        if name != "none":
            dutySeq.append((memid, name))
            map.append(memid)
    total = len(map)
    memLimitNum = len(allmemberList)

    print("参与排班人员总数：", total)
    f.write('\n' + '参与排班人员总数：' + str(total))
    f.write("参与排班姓名表：" + str(allmemberList))

    #河口白班周一计数器
    staff_hekou_mon = {}
    HistoryDate_hekou_mon = []
    tmpIdx = 0
    for i in range(1, memLimitNum + 1):
        name = targetLine_Name.split(',')[i]
        if name != "none":
            HistoryDate_hekou_mon.append(int(targetLine_hekou_mon.split(',')[i]))
            # print(map[tmpIdx] + "============ " + str(HistoryDate_hekou_mon[tmpIdx]))
            # f.write(map[tmpIdx] + "============ " + str(HistoryDate_hekou_mon[tmpIdx]))
            staff_hekou_mon.update({map[tmpIdx]: HistoryDate_hekou_mon[tmpIdx]})
            tmpIdx += 1
    print("周一河口白班值班的历史计数器:", staff_hekou_mon)
    f.write('\n' + '周一河口白班值班的历史计数器：' + str(staff_hekou_mon))

    #周一小夜班计数器
    staff_small_fri = {}
    HistoryDate_small_fri = []
    tmpIdx = 0
    for i in range(1, memLimitNum + 1):
        name = targetLine_Name.split(',')[i]
        if name != "none":
            HistoryDate_small_fri.append(int(targetLine_small_fri.split(',')[i]))
            # print(map[tmpIdx] + "============ " + str(HistoryDate_small_fri[tmpIdx]) )
            # f.write(map[tmpIdx] + "============ " + str(HistoryDate_small_fri[tmpIdx]) )
            staff_small_fri.update({map[tmpIdx]: HistoryDate_small_fri[tmpIdx]})
            tmpIdx += 1
    print("周五夜班值班的历史计数器:", staff_small_fri)
    f.write('\n' + '周五夜班值班的历史计数器：' + str(staff_small_fri))

    # 每个人大夜班的计数器,从历史数据中导入，作为此次排班的依据
    staff_full_night = {}
    HistoryDate_full_night = []
    tmpIdx = 0
    for i in range(1, memLimitNum + 1):
        name = targetLine_Name.split(',')[i]
        if name != "none":
            HistoryDate_full_night.append(int(targetLine_big.split(',')[i]))
            staff_full_night.update({map[tmpIdx]: HistoryDate_full_night[tmpIdx]})
            tmpIdx += 1
    print("大夜班的历史计数器:", staff_full_night)
    f.write('\n' + '大夜班的历史计数器：' + str(staff_full_night))

    # 值班经理计数器
    staff_manager = {}
    HistoryDate_manager = []
    tmpIdx = 0
    for i in range(1, memLimitNum + 1):
        name = targetLine_Name.split(',')[i]
        if name != "none":
            HistoryDate_manager.append(int(targetLine_manager.split(',')[i]))
            staff_manager.update({map[tmpIdx]: HistoryDate_manager[tmpIdx]})
            tmpIdx += 1
    print("值班经理的历史计数器:", staff_manager)
    f.write('\n' + '值班经理的历史计数器：' + str(staff_manager))

    # 河口值班计数器 变为河口白班计数器，自2019年7月31日起清零
    staff_hekou = {}
    HistoryDate_hekou = []
    tmpIdx = 0
    for i in range(1, memLimitNum + 1):
        name = targetLine_Name.split(',')[i]
        if name != "none":
            HistoryDate_hekou.append(int(targetLine_hekou.split(',')[i]))
            staff_hekou.update({map[tmpIdx]: HistoryDate_hekou[tmpIdx]})
            tmpIdx += 1
    print("河口值班的历史计数器:", staff_hekou)
    f.write('\n' + '河口值班的历史计数器：' + str(staff_hekou))

    # 周一小夜班值班计数器
    # 此计数器也即节假日后首日计数器，by songml 20190122
    staff_small_mon = {}
    HistoryDate_small_mon = []
    tmpIdx = 0
    for i in range(1, memLimitNum + 1):
        name = targetLine_Name.split(',')[i]
        if name != "none":
            HistoryDate_small_mon.append(int(targetLine_small_mon.split(',')[i]))
            staff_small_mon.update({map[tmpIdx]: HistoryDate_small_mon[tmpIdx]})
            tmpIdx += 1
    print("周一小夜班值班的历史计数器:", staff_small_mon)
    f.write('\n' + '周一小夜班值班的历史计数器：' + str(staff_small_mon))

    # 小夜班值班计数器
    staff_small = {}
    HistoryDate_small = []
    tmpIdx = 0
    for i in range(1, memLimitNum + 1):
        name = targetLine_Name.split(',')[i]
        if name != "none":
            HistoryDate_small.append(int(targetLine_small.split(',')[i]))
            staff_small.update({map[tmpIdx]: HistoryDate_small[tmpIdx]})
            tmpIdx += 1
    print("小夜班的历史计数器:", staff_small)
    f.write('\n' + '小夜班的历史计数器：' + str(staff_small))



    # 主岗的夜班总数量
    staff_chief_night = {}
    staff_main_arr = []
    staff_main_arr = config2.list_main
    for staff in staff_main_arr:
        staff_chief_night.update({staff: staff_small.get(staff) + staff_full_night.get(staff)})

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
    # 网络岗位的非主岗员工的夜班总数量(原来是非主岗老员工，现在把新人纳入进来，新人只是一个角色)
    staff_old_night_B = {}
    staff_B_arr=[]
    staff_B_arr = config2.list_group_B
    for staff in staff_B_arr:
        staff_old_night_B.update({staff: staff_small.get(staff) + staff_full_night.get(staff)})

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

    # 应用岗位非主岗员工的夜班总数量(原来是非主岗老员工，现在把新人纳入，新人只是一个角色)
    staff_old_night_C = {}
    staff_C_arr = []
    staff_C_arr = config2.list_group_C
    for staff in staff_C_arr:
        staff_old_night_C.update({staff: staff_small.get(staff) + staff_full_night.get(staff)})

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


    #主机岗位
    staff_old_night_A = {}
    staff_A_arr = []
    staff_A_arr = config2.list_group_A
    for staff in staff_A_arr:
        staff_old_night_A.update({staff: staff_small.get(staff) + staff_full_night.get(staff)})

    # 随机排列
    staff_old_night_A_random = {}
    staff_old_night_A_list = list(staff_old_night_A.keys())
    random.shuffle(staff_old_night_A_list)
    for i in staff_old_night_A_list:
        staff_old_night_A_random.update({i: staff_old_night_A.get(i)})

    print("主机夜班总数量：", staff_old_night_A)
    f.write('\n' + '主机夜班总数量：' + str(staff_old_night_A))
    print("主机夜班总数量,乱序：", staff_old_night_A_random)
    f.write('\n' + '主机夜班总数量,乱序：' + str(staff_old_night_A_random))

    #数据库岗位
    staff_old_night_D = {}
    staff_D_arr = []
    staff_D_arr = config2.list_group_D
    for staff in staff_D_arr:
        staff_old_night_D.update({staff: staff_small.get(staff) + staff_full_night.get(staff)})

    # 随机排列
    staff_old_night_D_random = {}
    staff_old_night_D_list = list(staff_old_night_D.keys())
    random.shuffle(staff_old_night_D_list)
    for i in staff_old_night_D_list:
        staff_old_night_D_random.update({i: staff_old_night_D.get(i)})

    print("数据库夜班总数量：", staff_old_night_D)
    f.write('\n' + '数据库夜班总数量：' + str(staff_old_night_D))
    print("数据库夜班总数量,乱序：", staff_old_night_D_random)
    f.write('\n' + '数据库夜班总数量,乱序：' + str(staff_old_night_D_random))

    #安全岗位
    staff_old_night_E = {}
    staff_E_arr = config2.list_group_E
    for staff in staff_E_arr:
        staff_old_night_E.update({staff: staff_small.get(staff) + staff_full_night.get(staff)})

    # 随机排列
    staff_old_night_E_random = {}
    staff_old_night_E_list = list(staff_old_night_E.keys())
    random.shuffle(staff_old_night_E_list)
    for i in staff_old_night_E_list:
        staff_old_night_E_random.update({i: staff_old_night_E.get(i)})

    print("安全岗位夜班总数量：", staff_old_night_E)
    f.write('\n' + '安全岗位夜班总数量：' + str(staff_old_night_E))
    print("安全岗位夜班总数量,乱序：", staff_old_night_E_random)
    f.write('\n' + '安全岗位夜班总数量,乱序：' + str(staff_old_night_E_random))

    # 河口白班值班（除了主岗、中层均可去河口，由河口白班计数器控制，原河口计数器清零，重新计数）
    tmp_hekou_arr = config2.list_group_A + config2.list_group_B + config2.list_group_C + config2.list_group_D + config2.list_group_E
    for mainMem in staff_main_arr:
        tmp_hekou_arr.remove(mainMem)
    for da in list_da:
        tmp_hekou_arr.remove(da)
    for nothekou in list_not_hekou:
        tmp_hekou_arr.remove(nothekou)
    #女王欣不参加夜盘，但参加河口值班
    tmp_hekou_arr.append('D10') # 女王欣参加河口白班值班
    tmp_hekou_arr.append('E10')  # 男王欣参加河口白班值班
    random.shuffle(tmp_hekou_arr)
    staff_hekou_day = {}
    for staff in tmp_hekou_arr:
        staff_hekou_day.update({staff: staff_hekou.get(staff)})
    print("河口白班值班员工夜班总数量,乱序：", staff_hekou_day)
    f.write('\n' + '河口白班值班员工夜员工夜班总数量,乱序：' + str(staff_hekou_day))



    ################################排序##################################################
    # 根据夜班总数量排的   主岗列表，按值夜班数量从小到大排序
    # 判断当天如果是周一或者节假日后首日(包括节假后首日是周五的情况)20190123 by songml
    f.write("\n=========>>>>>>>>>>>> SpecialDay is " + str(Specialday) + "  WeekDay is " + str(Weekday))
    if (Specialday == 2) or (Specialday == 0 and Weekday == 1):
        # 按照夜班总数及周一节假日首日进行排序 开始 20190123 by songml end
        # 遍历主岗哈希，结合map,生成新的基于周一夜班的哈希，总共生成3个列表

        # 只要是周一或节假日后第一天，河口白班都需要到大厦协助启停检查，为避免总轮到，添加河口白班周一及节假日后首日
        # 计数器
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

            # 主机岗位
            # 根据夜班总数量排的   主机岗位列表，按值夜班数量从小到大排序
            tmplist2 = []
            for staff in staff_old_night_A_random.keys():
                tmplist2.append((staff_old_night_A_random.get(staff), staff_small_mon.get(staff)
                                 , staff_small_fri.get(staff), staff))
            staff_old_night_A_inorder = sorted(tmplist2, key=lambda x: (x[0], x[1], x[2]))
            f.write('\n' + '+++ 完整版排序列表 ===== 主机岗位列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_A_inorder))

            ### new added

            for i in range(len(staff_old_night_A_inorder)):
                staff_old_night_A_inorder[i] = staff_old_night_A_inorder[i][3]

            f.write('\n' + '+++ 主机岗位列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_A_inorder))

            # 数据库岗位
            # 根据夜班总数量排的   数据库岗位列表，按值夜班数量从小到大排序
            tmplist3 = []
            for staff in staff_old_night_D_random.keys():
                tmplist3.append((staff_old_night_D_random.get(staff), staff_small_mon.get(staff)
                                 , staff_small_fri.get(staff), staff))
            staff_old_night_D_inorder = sorted(tmplist3, key=lambda x: (x[0], x[1], x[2]))
            f.write('\n' + '+++ 完整版排序列表 ===== 数据库岗位列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_D_inorder))

            ### new added

            for i in range(len(staff_old_night_D_inorder)):
                staff_old_night_D_inorder[i] = staff_old_night_D_inorder[i][3]

            f.write('\n' + '+++ 数据库岗位列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_D_inorder))

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


            # 安全岗位
            # 根据夜班总数量排的   安全岗位列表，按值夜班数量从小到大排序
            tmplist7 = []
            for staff in staff_old_night_E_random.keys():
                tmplist7.append((staff_old_night_E_random.get(staff), staff_small_mon.get(staff)
                                 , staff_small_fri.get(staff), staff))
            staff_old_night_E_inorder = sorted(tmplist7, key=lambda x: (x[0], x[1], x[2]))
            f.write('\n' + '+++ 完整版排序列表 ===== 安全岗位列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_E_inorder))

            ### new added

            for i in range(len(staff_old_night_E_inorder)):
                staff_old_night_E_inorder[i] = staff_old_night_E_inorder[i][3]

            f.write('\n' + '+++ 安全岗位列表，按值夜班数量(节假日首日及周五计数进行排序)从小到大排序：' + str(staff_old_night_E_inorder))

        else:
            tmplist = []
            for staff in staff_chief_night_random.keys():
                tmplist.append((staff_chief_night_random.get(staff), staff_small_mon.get(staff), staff))

            staff_chief_night_inorder = sorted(tmplist, key=lambda x: (x[0], x[1]))
            f.write('\n' + '+++ 完整版排序列表=====主岗列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_chief_night_inorder))
            ### new added
            for i in range(len(staff_chief_night_inorder)):
                # 值班人员变为数组第3个参数
                staff_chief_night_inorder[i] = staff_chief_night_inorder[i][2]

            f.write('\n' + '+++主岗列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_chief_night_inorder))

            # 根据夜班总数量排的   主机岗位员工列表，按值夜班数量从小到大排序
            tmplist2 = []
            for staff in staff_old_night_A_random.keys():
                tmplist2.append((staff_old_night_A_random.get(staff), staff_small_mon.get(staff), staff))
            staff_old_night_A_inorder = sorted(tmplist2, key=lambda x: (x[0], x[1]))
            f.write('\n' + '+++ 完整版排序列表 ===== 主机岗位列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_A_inorder))

            ### new added
            for i in range(len(staff_old_night_A_inorder)):
                staff_old_night_A_inorder[i] = staff_old_night_A_inorder[i][2]

            f.write('\n' + '+++ 主机岗位列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_A_inorder))

            # 根据夜班总数量排的   数据库岗位列表，按值夜班数量从小到大排序
            tmplist3 = []
            for staff in staff_old_night_D_random.keys():
                tmplist3.append((staff_old_night_D_random.get(staff), staff_small_mon.get(staff), staff))
            staff_old_night_D_inorder = sorted(tmplist3, key=lambda x: (x[0], x[1]))
            f.write('\n' + '+++ 完整版排序列表 ===== 数据库岗位列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_D_inorder))

            ### new added

            for i in range(len(staff_old_night_D_inorder)):
                staff_old_night_D_inorder[i] = staff_old_night_D_inorder[i][2]

            f.write('\n' + '+++ 数据库岗位列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_D_inorder))


            # 根据夜班总数量排的   网络岗位列表，按值夜班数量从小到大排序
            tmplist4 = []
            for staff in staff_old_night_B_random.keys():
                tmplist4.append((staff_old_night_B_random.get(staff), staff_small_mon.get(staff), staff))
            staff_old_night_B_inorder = sorted(tmplist4, key=lambda x: (x[0], x[1]))
            f.write('\n' + '+++ 完整版排序列表 ===== 网络岗位列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_B_inorder))

            ### new added
            for i in range(len(staff_old_night_B_inorder)):
                staff_old_night_B_inorder[i] = staff_old_night_B_inorder[i][2]

            f.write('\n' + '+++ 网络岗位列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_B_inorder))

            # 根据夜班总数量排的   应用岗位列表，按值夜班数量从小到大排序
            tmplist5 = []
            for staff in staff_old_night_C_random.keys():
                tmplist5.append((staff_old_night_C_random.get(staff), staff_small_mon.get(staff), staff))
            staff_old_night_C_inorder = sorted(tmplist5, key=lambda x: (x[0], x[1]))
            f.write('\n' + '+++ 完整版排序列表 ===== 应用岗位列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_C_inorder))

            ### new added

            for i in range(len(staff_old_night_C_inorder)):
                staff_old_night_C_inorder[i] = staff_old_night_C_inorder[i][2]

            f.write('\n' + '+++ 应用岗位列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_C_inorder))

            # 根据夜班总数量排的   安全岗位员工列表，按值夜班数量从小到大排序
            tmplist7 = []
            for staff in staff_old_night_E_random.keys():
                tmplist7.append((staff_old_night_E_random.get(staff), staff_small_mon.get(staff), staff))
            staff_old_night_E_inorder = sorted(tmplist7, key=lambda x: (x[0], x[1]))
            f.write('\n' + '+++ 完整版排序列表 ===== 安全岗位员工列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_E_inorder))

            ### new added

            for i in range(len(staff_old_night_E_inorder)):
                staff_old_night_E_inorder[i] = staff_old_night_E_inorder[i][2]

            f.write('\n' + '+++ 安全岗位员工列表，按值夜班数量(节假日首日数量进行排序)从小到大排序：' + str(staff_old_night_E_inorder))

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

        # 根据夜班总数量排的   主机岗位员工列表，按值夜班数量从小到大排序
        tmplist2 = []
        for staff in staff_old_night_A_random.keys():
            tmplist2.append((staff_old_night_A_random.get(staff), staff_small_fri.get(staff), staff))
        staff_old_night_A_inorder = sorted(tmplist2, key=lambda x: (x[0], x[1]))
        f.write('\n' + '+++ 完整版排序列表 ===== 主机岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_A_inorder))

        ### new added
        for i in range(len(staff_old_night_A_inorder)):
            staff_old_night_A_inorder[i] = staff_old_night_A_inorder[i][2]

        f.write('\n' + '+++ 主机岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_A_inorder))

        # 根据夜班总数量排的   数据库岗位列表，按值夜班数量从小到大排序
        tmplist3 = []
        for staff in staff_old_night_D_random.keys():
            tmplist3.append((staff_old_night_D_random.get(staff), staff_small_fri.get(staff), staff))
        staff_old_night_D_inorder = sorted(tmplist3, key=lambda x: (x[0], x[1]))
        f.write('\n' + '+++ 完整版排序列表 ===== 数据库岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_D_inorder))

        ### new added

        for i in range(len(staff_old_night_D_inorder)):
            staff_old_night_D_inorder[i] = staff_old_night_D_inorder[i][2]

        f.write('\n' + '+++ 数据库岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_D_inorder))

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


        # 根据夜班总数量排的   安全岗位列表，按值夜班数量从小到大排序
        tmplist7 = []
        for staff in staff_old_night_E_random.keys():
            tmplist7.append((staff_old_night_E_random.get(staff), staff_small_fri.get(staff), staff))
        staff_old_night_E_inorder = sorted(tmplist7, key=lambda x: (x[0], x[1]))
        f.write('\n' + '+++ 完整版排序列表 ===== 安全岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_E_inorder))

        ### new added

        for i in range(len(staff_old_night_E_inorder)):
            staff_old_night_E_inorder[i] = staff_old_night_E_inorder[i][2]

        f.write('\n' + '+++ 安全岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_E_inorder))

        # added by songml 20190126
    else:

        # 其它日子
        staff_chief_night_inorder = sorted(zip(staff_chief_night_random.values(), staff_chief_night_random.keys()),key=lambda x:x[0])
        for i in range(len(staff_chief_night_inorder)):
            staff_chief_night_inorder[i] = staff_chief_night_inorder[i][1]

        f.write('\n' + '主岗列表，按值夜班数量从小到大排序：' + str(staff_chief_night_inorder))

        # 根据夜班总数量排的  主机岗位列表，按值夜班数量从小到大排序
        staff_old_night_A_inorder = sorted(zip(staff_old_night_A_random.values(), staff_old_night_A_random.keys()),
                                           key=lambda x: x[0])
        for i in range(len(staff_old_night_A_inorder)):
            staff_old_night_A_inorder[i] = staff_old_night_A_inorder[i][1]

        f.write('\n' + '主机岗位列表，按值夜班数量从小到大排序：' + str(staff_old_night_A_inorder))

        # 根据夜班总数量排的   数据库岗位列表，按值夜班数量从小到大排序
        staff_old_night_D_inorder = sorted(zip(staff_old_night_D_random.values(), staff_old_night_D_random.keys()),
                                           key=lambda x: x[0])
        for i in range(len(staff_old_night_D_inorder)):
            staff_old_night_D_inorder[i] = staff_old_night_D_inorder[i][1]

        f.write('\n' + '数据库岗位列表，按值夜班数量从小到大排序：' + str(staff_old_night_D_inorder))

        # 根据夜班总数量排的   网络岗位列表，按值夜班数量从小到大排序
        staff_old_night_B_inorder = sorted(zip(staff_old_night_B_random.values(), staff_old_night_B_random.keys()), key=lambda x:x[0])
        for i in range(len(staff_old_night_B_inorder)):
            staff_old_night_B_inorder[i] = staff_old_night_B_inorder[i][1]

        f.write('\n' + '网络岗位列表，按值夜班数量从小到大排序：' + str(staff_old_night_B_inorder))

        # 根据夜班总数量排的   应用岗位列表，按值夜班数量从小到大排序
        staff_old_night_C_inorder = sorted(zip(staff_old_night_C_random.values(), staff_old_night_C_random.keys()), key=lambda x:x[0])
        for i in range(len(staff_old_night_C_inorder)):
            staff_old_night_C_inorder[i] = staff_old_night_C_inorder[i][1]

        f.write('\n' + '应用岗位列表，按值夜班数量从小到大排序：' + str(staff_old_night_C_inorder))

        # 根据夜班总数量排的   安全列表，按值夜班数量从小到大排序
        staff_old_night_E_inorder = sorted(zip(staff_old_night_E_random.values(), staff_old_night_E_random.keys()),
                                           key=lambda x: x[0])
        for i in range(len(staff_old_night_E_inorder)):
            staff_old_night_E_inorder[i] = staff_old_night_E_inorder[i][1]

        f.write('\n' + '安全岗位岗位列表，按值夜班数量从小到大排序：' + str(staff_old_night_E_inorder))

    ###################选出6个值班人员#############################
    ##########################################################
    ############将值班数量最少的主岗选出，作为值班第一天的岗位################
    ############ 添加女生计数器 、新人计数器（20190514）########
    ############ 添加女生计数器 counterWoman duty_new_cnt ########
    duty_women_cnt = 0 #added by songml
    duty_new_cnt = 0 #added by songml 20190514
    main_cnt = 0
    moni_cnt = 0
    oa_cnt = 0

    # 主岗不能是昨天值班的人员
    for i in range(main_amount):
        if staff_chief_night_inorder[i] in LastMateList:
            continue
        else:
            duty.append(staff_chief_night_inorder[i])
            chief_amout += 1
            # added by songml for duty_women_cnt 20181214
            if staff_chief_night_inorder[i] in list_women:
                f.write('\n' + '选中的女生为：' + staff_chief_night_inorder[i])
                duty_women_cnt += 1
            break
    main_cnt += 1
    f.write('\n' + '选过主岗的新版值班表：' + str(duty))
    ###################先判断是否有网络和应用岗位,然后选出余下的值班人员(新算法)######################
    ##############################################################################

    f.write('\n' + '选过主岗后女生的人数===========：' + str(duty_women_cnt))
    if duty[0][0] != "B":
        print("没有网络，额外添加")
        f.write('\n' + ' 没有网络，额外添加')
        for i in range(len(staff_old_night_B_inorder)):  # 按照夜班数量的从小到大安排网络岗位值班,并确保当天值班人员不是一个岗位的
            if staff_old_night_B_inorder[i] in LastMateList:  # 判断和上一日值班人员是否重复
                continue
            else:
                # added by songml for duty_women_cnt 20181214
                if staff_old_night_B_inorder[i] in list_women:  # 如果是女生

                    if duty_women_cnt == 2:  # 女生数为2 ，直接跳过
                        f.write('\n' + ' 网络选人中 且这次选中的人为女生 但女生数已为2 跳过:'
                                + staff_old_night_B_inorder[i])
                        continue
                    else:  # 女生数不为2
                        duty.append(staff_old_night_B_inorder[i])
                        f.write('\n' + '选中的女生为：' + staff_old_night_B_inorder[i])
                        duty_women_cnt += 1
                        if staff_old_night_B_inorder[i] in list_new:  # 女生数不为2，如果新人，之前没有新人，新人计数器添加1
                            f.write('\n' + '网络选中的新人为：' + staff_old_night_B_inorder[i])
                            duty_new_cnt += 1
                        # 网络主岗没有女生，所以不考虑主岗情况
                        break
                # added by songml for duty_women_cnt 20181214
                else:  # 不是女生
                    duty.append(staff_old_night_B_inorder[i])
                    if staff_old_night_B_inorder[i] in list_new:  # 不是女生，且之前没有新人，所以新人计数直接添加1
                        f.write('\n' + '网络选中的新人、非女生为：' + staff_old_night_B_inorder[i])
                        duty_new_cnt += 1
                    if staff_old_night_B_inorder[i] in list_main:  # 如果是主岗，主岗计数器添加1
                        f.write('\n' + '网络选中主岗、非女生为：' + staff_old_night_B_inorder[i])
                        main_cnt += 1
                    break
                # break
    f.write('\n' + '选过网络岗位后女生人数===========：' + str(duty_women_cnt))
    f.write('\n' + '选过网络岗位后新人数===========：' + str(duty_new_cnt))
    f.write('\n' + '选过网络主岗人数===========：' + str(main_cnt))
    #选择完网络后 看是否选择了一个总监助理，是否选择了具有监控属性的人


    for i in range(len(duty)):
        if duty[i][0] == "B":
            # f.write('\n当前为============= ' + duty[i])
            if duty[i] in list_da:#网络组选中了总监助理后，与主机，数据库的总监助理互斥
                for da in list_da:
                    if da in staff_old_night_A_inorder:
                        # f.write('\n总监主机删除============= '+ da)
                        staff_old_night_A_inorder.remove(da)
                    if da in staff_old_night_D_inorder:
                        # f.write('\n数据库主机删除============= ' + da)
                        staff_old_night_D_inorder.remove(da)
                f.write('\n' + '选择了一个总监助理后========主机组===：' + str(staff_old_night_A_inorder))
                f.write('\n' + '选择了一个总监助理后========数据库组===：' + str(staff_old_night_D_inorder))
            if duty[i] in list_moni: #网络组选中一个人有监控组属性后，与数据库组中监控的人互斥
                for moni in list_moni:
                    # f.write('\n当前为里面============= ' + duty[i] + ' ===== ' + moni)
                    if moni in staff_old_night_C_inorder:
                        # f.write('\n应用监控删除============= ' + moni)
                        staff_old_night_C_inorder.remove(moni)
                    if moni in staff_old_night_D_inorder:
                        # f.write('\n数据库监控删除============= ' + moni)
                        staff_old_night_D_inorder.remove(moni)
                f.write('\n' + '选择了监控组属性的人后========应用组除去监控属性的人，剩余的人===：' + str(staff_old_night_C_inorder))
                f.write('\n' + '选择了监控组属性的人后========数据库组除去监控属性的人，剩余的人===：' + str(staff_old_night_D_inorder))
            break



    if duty[0][0] != "C":
        print("没有应用，额外添加")
        f.write('\n' + ' 没有应用，额外添加')
        f.write('\n'+str(staff_old_night_C_inorder))
        f.write('\n' + str(LastMateList))
        for i in range(len(staff_old_night_C_inorder)):  # 按照夜班数量的从小到大安排网络岗位值班,并确保当天值班人员不是一个岗位的
            if staff_old_night_C_inorder[i] in LastMateList:  # 判断和上一日值班人员是否重复
                continue
            else:

                # added by songml for duty_women_cnt 20181214
                if staff_old_night_C_inorder[i] in list_women:  # 如果选中了女生
                    if duty_women_cnt == 2:  # 女生数已经为2
                        f.write('\n' + ' 应用选人中 且这次选中的人为女生 但女生数已为2 跳过 :' + staff_old_night_C_inorder[i])
                        continue
                    else:  # 女生数小于2
                        if staff_old_night_C_inorder[i] in list_new:  # 选中的人为新人
                            if duty_new_cnt == 0:  # 女生小于2人 且 新人数为0 添加并计数
                                duty.append(staff_old_night_C_inorder[i])
                                f.write('\n' + '应用选人女生<2且新人=0;选中的女生新人为：' + staff_old_night_C_inorder[i])
                                duty_women_cnt += 1
                                duty_new_cnt += 1
                                break
                            else:  # 女生小于2人 但新人数已经为1 直接跳过
                                f.write('\n' + ' 应用选人中 且这次选中的人为女生 但女生数 < 2 但新人数超过1 跳过'
                                        + staff_old_night_C_inorder[i])
                                continue
                        else:
                            duty.append(staff_old_night_C_inorder[i])
                            f.write('\n' + '应用选人中 选中的非新人女生为：' + staff_old_night_C_inorder[i] )
                            duty_women_cnt += 1
                            #应用主岗没有女生，所以不考虑主岗情况
                            break
                # added by songml for duty_women_cnt 20181214
                else:  # 非女生
                    if staff_old_night_C_inorder[i] in list_new:
                        if duty_new_cnt == 0:  # 非女生 且为新人数 为 0
                            duty.append(staff_old_night_C_inorder[i])
                            f.write('\n' + '选中的新人(非女生)为：' + staff_old_night_C_inorder[i] + ' 新人数：'
                                    + str(duty_women_cnt))
                            duty_new_cnt += 1

                            break
                        else:
                            f.write('\n' + ' 应用选人中 且这次选中的人为新人、非女生， 但新人数已为1 跳过 '
                                    + staff_old_night_C_inorder[i])
                            continue
                    else:#非新人
                        duty.append(staff_old_night_C_inorder[i])
                        if staff_old_night_C_inorder[i] in list_main:  # 如果是主岗，主岗计数器添加1
                            f.write('\n' + '应用选中主岗、非女生为：' + staff_old_night_C_inorder[i])
                            main_cnt += 1
                        break
                # break
    ##############转换为新的值班表，列表形式############
    f.write('\n' + '选过主岗、网络(可能是新人)、应用(可能是新人)的新版值班表：' + str(duty))
    for i in range(len(duty)):
        if duty[i][0] == "C":
            if duty[i] in list_moni: #网络组选中一个人有监控组属性后，与数据库组中监控的人互斥
                for moni in list_moni:
                    if moni in staff_old_night_D_inorder:
                        staff_old_night_D_inorder.remove(moni)
                f.write('\n' + '应用选择了监控组属性的人后========数据库组除去监控属性的人，剩余的人===：' + str(staff_old_night_C_inorder))
            break

    ######选择主机岗位的人员  20190618 by songml #######################
    if duty[0][0] != "A":
        print("没有主机，额外添加")
        f.write('\n' + ' 没有主机，额外添加')
        f.write('\n'+str(staff_old_night_A_inorder))
        f.write('\n' + str(LastMateList))
        for i in range(len(staff_old_night_A_inorder)):  # 按照夜班数量的从小到大安排网络岗位值班,并确保当天值班人员不是一个岗位的
            if staff_old_night_A_inorder[i] in LastMateList:  # 判断和上一日值班人员是否重复
                continue
            else:

                # added by songml for duty_women_cnt 20181214
                if staff_old_night_A_inorder[i] in list_women:  # 如果选中了女生
                    if duty_women_cnt == 2:  # 女生数已经为2
                        f.write('\n' + ' 主机选人中 且这次选中的人为女生 但女生数已为2 跳过 :' + staff_old_night_A_inorder[i])
                        continue
                    else:  # 女生数小于2
                        if staff_old_night_A_inorder[i] in list_new:  # 选中的人为新人
                            if duty_new_cnt == 0:  # 女生小于2人 且 新人数为0 添加并计数
                                duty.append(staff_old_night_A_inorder[i])
                                f.write('\n' + '主机选人女生<2且新人=0;选中的女生新人为：' + staff_old_night_A_inorder[i])
                                duty_women_cnt += 1
                                duty_new_cnt += 1
                                break
                            else:  # 女生小于2人 但新人数已经为1 直接跳过
                                f.write('\n' + ' 主机选人中 且这次选中的人为女生 但女生数 < 2 但新人数超过1 跳过'
                                        + staff_old_night_A_inorder[i])
                                continue
                        else:
                            duty.append(staff_old_night_A_inorder[i])
                            f.write('\n' + '主机选人中 选中的非新人女生为：' + staff_old_night_A_inorder[i] )
                            duty_women_cnt += 1
                            break
                # added by songml for duty_women_cnt 20181214
                else:  # 非女生
                    if staff_old_night_A_inorder[i] in list_new:
                        if duty_new_cnt == 0:  # 非女生 且为新人数 为 0  直接跳过
                            duty.append(staff_old_night_A_inorder[i])
                            f.write('\n' + '主机选人中，选中的新人(非女生)为：' + staff_old_night_A_inorder[i] + ' 新人数：'
                                    + str(duty_women_cnt))
                            duty_new_cnt += 1
                            break
                        else:
                            f.write('\n' + ' 主机选人中 且这次选中的人为新人、非女生， 但新人数已为1 跳过 '
                                    + staff_old_night_A_inorder[i])
                            continue
                    else:
                        if staff_old_night_A_inorder[i] not in list_main:
                            duty.append(staff_old_night_A_inorder[i])
                            break
                        else:
                            if main_cnt < 3:
                                duty.append(staff_old_night_A_inorder[i])
                                main_cnt += 1
                                f.write('\n' + ' 主机选人中 且这次选中的男主岗为：' + staff_old_night_A_inorder[i])
                                break
                            else:
                                continue

                # break
    ##############转换为新的值班表，列表形式############
    f.write('\n' + '选过主岗、网络(可能是新人)、应用(可能是新人)、主机（可能是新人）的新版值班表：' + str(duty))
    for i in range(len(duty)):
        if duty[i][0] == "A":
            if duty[i] in list_da:
                for da in list_da:
                    # 原来使用的是 staff_old_night_D_list 使用错误 20190923
                    if da in staff_old_night_D_inorder:
                        staff_old_night_D_inorder.remove(da)
                f.write('\n' + '主机选择了一个总监助理后========数据库组，除去总监剩余的人===：' + str(staff_old_night_D_list))
            if duty[i] in list_oa: #主机组选中一个人有监控组属性后，与数据库组中监控的人互斥
                for oa in list_oa:
                    if oa in staff_old_night_D_inorder:
                        staff_old_night_D_inorder.remove(oa)
                f.write('\n' + '主机选择了OA属性的人后========数据库组除去OA属性的人，剩余的人===：' + str(staff_old_night_D_list))
            break

    ######选择主机  20190618 by songml #######################

    ######选择数据库  20190618 by songml #######################
    if duty[0][0] != "D":
        print("没有数据库，额外添加")
        f.write('\n' + ' 没有数据库，额外添加')
        f.write('\n'+str(staff_old_night_D_inorder))
        f.write('\n' + str(LastMateList))
        for i in range(len(staff_old_night_D_inorder)):  # 按照夜班数量的从小到大安排数据库岗位值班,并确保当天值班人员不是一个岗位的
            if staff_old_night_D_inorder[i] in LastMateList:  # 判断和上一日值班人员是否重复
                continue
            else:

                # added by songml for duty_women_cnt 20181214
                if staff_old_night_D_inorder[i] in list_women:  # 如果选中了女生
                    if duty_women_cnt == 2:  # 女生数已经为2
                        f.write('\n' + ' 数据库选人中 且这次选中的人为女生 但女生数已为2 跳过 :' + staff_old_night_D_inorder[i])
                        continue
                    else:  # 女生数小于2
                        if staff_old_night_D_inorder[i] in list_new:  # 选中的人为新人
                            if duty_new_cnt == 0:  # 女生小于2人 且 新人数为0 添加并计数
                                duty.append(staff_old_night_D_inorder[i])
                                f.write('\n' + '数据库选人女生<2且新人=0;选中的女生新人为：' + staff_old_night_D_inorder[i])
                                duty_women_cnt += 1
                                duty_new_cnt += 1
                                break
                            else:  # 女生小于2人 但新人数已经为1 直接跳过
                                f.write('\n' + ' 数据库选人中 且这次选中的人为女生 但女生数 < 2 但新人数超过1 跳过'
                                        + staff_old_night_D_inorder[i])
                                continue
                        else:# 选中的人不为新人
                            if staff_old_night_D_inorder not in list_main: #不是主岗
                                duty.append(staff_old_night_D_inorder[i])
                                f.write('\n' + '数据库选人中 选中的非新人女生为：' + staff_old_night_D_inorder[i] )
                                duty_women_cnt += 1
                                break
                            else:
                                if main_cnt < 3: #主岗人数小于3，这个人是女主岗 目前走不到这里
                                    duty.append(staff_old_night_D_inorder[i])
                                    f.write('\n' + '数据库选人中 选中的非新人女生,并且为主岗为：' + staff_old_night_D_inorder[i])
                                    duty_women_cnt += 1
                                    main_cnt += 1
                                    break
                                else:
                                    continue

                # added by songml for duty_women_cnt 20181214
                else:  # 非女生
                    if staff_old_night_D_inorder[i] in list_new:
                        if duty_new_cnt == 0:  # 非女生 且为新人数 为 0
                            duty.append(staff_old_night_D_inorder[i])
                            f.write('\n' + '数据库选人中，选中的新人(非女生)为：' + staff_old_night_D_inorder[i] + ' 新人数：'
                                + str(duty_women_cnt))
                            duty_new_cnt += 1
                            break
                        else:
                            f.write('\n' + ' 数据库选人中 且这次选中的人为新人、非女生， 但新人数已为1 跳过 '
                                    + staff_old_night_D_inorder[i])
                            continue
                    else: #不是新人 非女生
                        if staff_old_night_D_inorder[i] not in list_main: #不是主岗
                            duty.append(staff_old_night_D_inorder[i])
                            break
                        else:
                            if main_cnt < 3: #是主岗，且当前已选中的主岗数量小于3
                                duty.append(staff_old_night_D_inorder[i])
                                main_cnt += 1
                                f.write('\n' + ' 数据库选人中 且这次选中的男主岗' + staff_old_night_D_inorder[i])
                                break
                            else:
                                continue
                # break
    ##############转换为新的值班表，列表形式############
    f.write('\n' + '选过主岗、网络、应用、主机、数据库的新版值班表：' + str(duty))

    ######选择数据库  20190618 by songml #######################

    ######选择安全  20190618 by songml #######################
    if duty[0][0] != "E":
        print("没有安全，额外添加")
        f.write('\n' + ' 没有安全，额外添加')
        f.write('\n'+str(staff_old_night_E_inorder))
        f.write('\n' + str(LastMateList))
        for i in range(len(staff_old_night_E_inorder)):  # 按照夜班数量的从小到大安排数据库岗位值班,并确保当天值班人员不是一个岗位的
            if staff_old_night_E_inorder[i] in LastMateList:  # 判断和上一日值班人员是否重复
                continue
            else:

                # added by songml for duty_women_cnt 20181214
                if staff_old_night_E_inorder[i] in list_women:  # 如果选中了女生
                    if duty_women_cnt == 2:  # 女生数已经为2
                        f.write('\n' + ' 安全选人中 且这次选中的人为女生 但女生数已为2 跳过 :' + staff_old_night_E_inorder[i])
                        continue
                    else:  # 女生数小于2
                        if staff_old_night_E_inorder[i] in list_new:  # 选中的人为新人
                            if duty_new_cnt == 0:  # 女生小于2人 且 新人数为0 添加并计数
                                duty.append(staff_old_night_E_inorder[i])
                                f.write('\n' + '安全选人女生<2且新人=0;选中的女生新人为：' + staff_old_night_E_inorder[i])
                                duty_women_cnt += 1
                                duty_new_cnt += 1
                                break
                            else:  # 女生小于2人 但新人数已经为1 直接跳过
                                f.write('\n' + ' 安全选人中 且这次选中的人为女生 但女生数 < 2 但新人数超过1 跳过'
                                        + staff_old_night_E_inorder[i])
                                continue
                        else:
                            if staff_old_night_E_inorder not in list_main:
                                duty.append(staff_old_night_E_inorder[i])
                                f.write('\n' + '安全选人中 选中的非新人女生、非主岗为：' + staff_old_night_E_inorder[i] )
                                duty_women_cnt += 1
                                break
                            else:
                                if main_cnt < 3:
                                    duty.append(staff_old_night_E_inorder[i])
                                    f.write('\n' + '安全选人中 选中的非新人女生,并且为主岗为：' + staff_old_night_E_inorder[i])
                                    duty_women_cnt += 1
                                    main_cnt += 1
                                    break
                                else:
                                    continue
                # added by songml for duty_women_cnt 20181214
                else:  # 非女生
                    if staff_old_night_E_inorder[i] in list_new:
                        if duty_new_cnt == 0:  # 非女生 且为新人数 为 0  直接跳过
                            duty.append(staff_old_night_E_inorder[i])
                            f.write('\n' + '安全选人中，选中的新人(非女生)为：' + staff_old_night_E_inorder[i] + ' 新人数：'
                                    + str(duty_women_cnt))
                            duty_new_cnt += 1
                            break
                        else:
                            f.write('\n' + ' 安全选人中 且这次选中的人为新人、非女生， 但新人数已为1 跳过 '
                                    + staff_old_night_E_inorder[i])
                            continue
                    else:
                        if staff_old_night_E_inorder[i] not in list_main:
                            duty.append(staff_old_night_E_inorder[i])
                            break
                        else:
                            if main_cnt < 3:
                                duty.append(staff_old_night_E_inorder[i])
                                main_cnt += 1
                                f.write('\n' + ' 安全岗位选人中 且这次选中的男主岗为：' + staff_old_night_E_inorder[i])
                                break
                            else:
                                continue
                # break
    ##############转换为新的值班表，列表形式############
    f.write('\n' + '选过主岗、网络、应用、主机、数据库、安全的新版值班表：' + str(duty))
    ######选择安全  20190618 by songml #######################

    # 值班组都包含哪些岗位，提取出来
    for i in range(len(duty)):
        duty_group[i] = duty[i][0]
    ###################################################
    f.write('\n' + '选过应用岗位后女生人数===========：' + str(duty_women_cnt))
    f.write('\n' + '选过应用岗位后新人数===========：' + str(duty_new_cnt))
    f.write('\n' + '上3个工作日的值班人员===========：' + str(LastMateList))

    #######################################
    # 随机排列
    random.shuffle(duty)
    print("新版值班表的人员结果（随机）:", duty)
    f.write('\n' + '新版值班表的结果，不含岗位（随机）：' + str(duty))

    ###########################################################################
    ###########################################################################
    #########################河口、值班经理、大夜班、小夜班选择############################
    ###########选择河口值班当天及前一个夜盘的人排除后再选人
    hekouExcptList = LastMateList_1 + duty
    if Date_1 in holiday_lastday:
        hekouExcptList = duty
    tmplistHekou = []
    # 河口值班排序添加计数器
    if (Specialday == 2) or (Specialday == 0 and Weekday == 1):
        # 只要是周一或节假日后第一天，河口白班都需要到大厦协助启停检查，为避免总轮到，添加河口白班周一及节假日后首日计数器
        for staff in staff_hekou_day.keys():
            tmplistHekou.append((staff_hekou_day.get(staff), staff_hekou_mon.get(staff), staff))
            hekou_day_inorder = sorted(tmplistHekou, key=lambda x: (x[0], x[1]))
        f.write('\n' + '+++ 完整版排序列表 ===== 应用岗位列表，按值夜班数量(及周五夜班数量进行排序)从小到大排序：' + str(staff_old_night_C_inorder))

        ### new added
        for i in range(len(hekou_day_inorder)):
            hekou_day_inorder[i] = hekou_day_inorder[i][2]
        f.write('\n' + '+++ 完整版排序列表=====河口白班，按河口值班数量从小到大排序：' + str(hekou_day_inorder))

    else:#不是周一或节假日后第一天
        for staff in staff_hekou_day.keys():
            tmplistHekou.append((staff_hekou_day.get(staff), staff))

        hekou_day_inorder = sorted(tmplistHekou, key=lambda x: (x[0]))

        ### new added
        for i in range(len(hekou_day_inorder)):
            # 值班人员变为数组第2个参数
            hekou_day_inorder[i] = hekou_day_inorder[i][1]

        f.write('\n' + '+++ 完整版排序列表=====河口白班，按河口值班数量从小到大排序：' + str(hekou_day_inorder))

    # 河口选人，把上一个夜盘及今天的值班人员排除后选择，选择到第一个即退出
    for i in range(len(hekou_day_inorder)):
        if hekou_day_inorder[i] not in hekouExcptList:
            duty_result[1] = hekou_day_inorder[i]
            break
        else:
            continue
    print("河口的值班人员：", duty_result[1])
    f.write('\n' + '河口的值班人员：' + str(duty_result[1]))

    ##############值班经理选择
    manager = []
    manager_dict = {}
    # 值班经理不是新人，不是河口值班人员,不是应用那两个新人 modified by songml 20190514
    for i in duty:
        #值班经理不能是应用新人(不满2年),2个应用新人临时添加到应用老人，要不然不够排了 modified by songml 20190514
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
        # 河口计数器
        staff_hekou[duty_result[1]] += 1
        # 值班经理计数器
        staff_manager[duty_result[2]] += 1

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

            #考虑节假日后首日选择之后，启停没有应用岗位的人。 by songml 20191220
            f.write('\n' + '判断周五，节假日首日小夜班有没有应用的人')
            if duty_result[5][0] != "C" and duty_result[6][0] != "C" and duty_result[2][0] != "C":
                if duty_result[3][0] == "C":
                    f.write('\n' + 'duty_result[3] 是应用组的 duty_result[3] 与 duty_result[5])互换')
                    tmpDuty = duty_result[3]
                    duty_result[3] = duty_result[5]
                    duty_result[5] = tmpDuty
                elif duty_result[4][0] == "C":
                    f.write('\n' + 'duty_result[4] 是应用组的 duty_result[4] 与 duty_result[6])互换')
                    tmpDuty = duty_result[4]
                    duty_result[4] = duty_result[6]
                    duty_result[6] = tmpDuty

            #考虑节假日后首日选择之后，启停没有应用岗位的人。 by songml 20191220
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
            #staff_small[duty_result[1]] += 1 #河口变为白班了 by songml 20190619
            staff_small[duty_result[2]] += 1
            staff_small[duty_result[5]] += 1
            staff_small[duty_result[6]] += 1

            ## 周五的计数器 added by songml 20190127 #河口变为白班 周五计数器也不必计数了
            #staff_small_fri[duty_result[1]] += 1
            staff_small_fri[duty_result[2]] += 1
            staff_small_fri[duty_result[3]] += 1
            staff_small_fri[duty_result[4]] += 1
            staff_small_fri[duty_result[5]] += 1
            staff_small_fri[duty_result[6]] += 1
            f.write('\n' + '周五河口计数：'
                    + str(duty_result[1]) + '：' + str(staff_hekou[duty_result[1]])
                    + '周五夜班计数：'
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
            #staff_small[duty_result[1]] += 1  #河口变成白班了 by songml 20190619
            staff_small[duty_result[2]] += 1
            staff_small[duty_result[5]] += 1
            staff_small[duty_result[6]] += 1

            #周一小夜班计数器
            #staff_small_mon[duty_result[1]] += 1 #河口变成白班了 by songml 20190619
            staff_small_mon[duty_result[2]] += 1
            staff_small_mon[duty_result[5]] += 1
            staff_small_mon[duty_result[6]] += 1
            ##########################################
        staff_hekou_mon[duty_result[1]] += 1
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

            # 大夜班 因为周一小夜班值班多，因此下面两个人为大夜班
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
            # 正常周一河口白班计数器
            staff_hekou_mon[duty_result[1]] += 1
            # 值班经理计数器
            staff_manager[duty_result[2]] += 1
            # 大夜班计数器
            staff_full_night[duty_result[3]] += 1
            staff_full_night[duty_result[4]] += 1

            # 小夜班计数器
            #staff_small[duty_result[1]] += 1  # 河口白班计数器不变
            staff_small[duty_result[2]] += 1
            staff_small[duty_result[5]] += 1
            staff_small[duty_result[6]] += 1

            # 周一小夜班计数器
            #staff_small_mon[duty_result[1]] += 1  #周一小夜班不计数
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

            #处理大
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
                #staff_small_fri[duty_result[1]] += 1 # 河口只是白班，因此不应不做周五夜班计数
                staff_small_fri[duty_result[2]] += 1
                staff_small_fri[duty_result[3]] += 1
                staff_small_fri[duty_result[4]] += 1
                staff_small_fri[duty_result[5]] += 1
                staff_small_fri[duty_result[6]] += 1
                f.write(
                        '\n' + '河口白班计数：'
                        + str(duty_result[1]) + '：' + str(staff_hekou[duty_result[1]]) +
                        '\n' + '周五夜班计数：'
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
            #staff_small[duty_result[1]] += 1 # 河口只是白班，因此不应不做周五夜班计数
            staff_small[duty_result[2]] += 1
            staff_small[duty_result[5]] += 1
            staff_small[duty_result[6]] += 1

    # 除此之外的为参数错误
    else:
        print("Specialday参数错误")
        f.write('\n' + 'Specialday参数错误' )


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
    duty_song = [0, 0, 0, 0, 0, 0, 0]
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

    ########### 添加河口白班节后首日计数器
    result_hekou_mon = []
    result_hekou_mon.append("河口节后首日")

    tmpIdx = 0
    for memberid in range(len(allmemberList)):
        if allmemberList[memberid] != "none":
            tmpCnt = staff_hekou_mon.get(allmemberIdList[memberid])
            result_hekou_mon.append(tmpCnt)
            tmpIdx += 1
        else:
            result_hekou_mon.append(0)
    ########## 添加河口白班节后首日计数器 added by songml 20190127


    ########### 添加周五的计数器 added by songml 20190127
    result_small_fri = []
    result_small_fri.append("周五夜班")

    tmpIdx = 0
    for memberid in range(len(allmemberList)):
        if allmemberList[memberid] != "none":
            tmpCnt = staff_small_fri.get(allmemberIdList[memberid])
            result_small_fri.append(tmpCnt)
            tmpIdx += 1
        else:
            result_small_fri.append(0)
    ########## 添加周五的计数器 added by songml 20190127


    ###########
    result_small_mon = []
    result_small_mon.append("周一小夜班")

    tmpIdx = 0
    for memberid in range(len(allmemberList)):
        if allmemberList[memberid] != "none":
            tmpCnt = staff_small_mon.get(allmemberIdList[memberid])
            result_small_mon.append(tmpCnt)
            tmpIdx += 1
        else:
            result_small_mon.append(0)

    ####################
    result_hekou = []
    result_hekou.append("河口")
    tmpIdx = 0
    for memberid in range(len(allmemberList)):
        if allmemberList[memberid] != "none":
            tmpCnt = staff_hekou.get(allmemberIdList[memberid])
            result_hekou.append(tmpCnt)
            tmpIdx += 1
        else:
            result_hekou.append(0)
    ###########
    result_manager = []
    result_manager.append("值班经理")
    tmpIdx = 0
    for memberid in range(len(allmemberList)):
        if allmemberList[memberid] != "none":
            tmpCnt = staff_manager.get(allmemberIdList[memberid])
            result_manager.append(tmpCnt)
            tmpIdx += 1
        else:
            result_manager.append(0)
    ###########
    result_full_night = []
    result_full_night.append("大夜班")

    tmpIdx = 0
    for memberid in range(len(allmemberList)):
        if allmemberList[memberid] != "none":
            tmpCnt = staff_full_night.get(allmemberIdList[memberid])
            result_full_night.append(tmpCnt)
            tmpIdx += 1
        else:
            result_full_night.append(0)
    ###########
    result_small = []
    result_small.append("小夜班")
    tmpIdx = 0
    for memberid in range(len(allmemberList)):
        if allmemberList[memberid] != "none":

            tmpCnt = staff_small.get(allmemberIdList[memberid])
            result_small.append(tmpCnt)
            tmpIdx += 1
        else:
            result_small.append(0)

    ###########
    ##################值班总数#########################
    # 所有夜班值班总数计数器
    Record_all = ["夜班总数"]

    for memberid in range(len(allmemberList)):
        if allmemberList[memberid] != "none":
            allcnt = staff_small.get(allmemberIdList[memberid]) + staff_full_night.get(allmemberIdList[memberid])
            Record_all.append(allcnt)
        else:
            Record_all.append(0)
    print("值班总数:", Record_all)
    ####################################################
    print("result_hekou:", result_hekou)

    out = open("D:\\dutyInfo\\duty_counter.csv", "a", newline="")
    csv_writer = csv.writer(out, dialect="excel")
    csv_writer.writerow(result_date)
    # 写入河口白班计数器
    csv_writer.writerow(result_hekou_mon)
    # 写入河口白班计数器
    # counter.csv中添加周五计数器的行 added by songml 20190127
    csv_writer.writerow(result_small_fri)
    # counter.csv中添加周五计数器的行 added by songml 20190127
    csv_writer.writerow(result_small_mon)
    csv_writer.writerow(result_hekou)
    csv_writer.writerow(result_manager)
    csv_writer.writerow(result_full_night)
    csv_writer.writerow(result_small)

    csv_writer.writerow(Record_all)

    out.close()
    #日志关闭
    f.close()

# PaiBan("20181001",1, 0)
