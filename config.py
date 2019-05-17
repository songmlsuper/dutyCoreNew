## 20190126  宋明霖  组人员调整F5 李松健 <=> C3 范嵩  ==> C3 李松健, F5 范嵩，去掉I4
## 20190201  宋明霖  fdh=>lph
##                   相应的角色也调整
#注意：除了更改初始列表外，还需要更改每个人的计数器求和函数
#节假日 使用git测试 test2
#王欣男，从5月份开始不再参加夜班值班工作,备份现有的计数器、排班配置；修改配置，调整计数器 J1相关的配置去掉
#国务院五一休假调整，添加5.1、5.2，及节假日后第一天5.3=>5.6
#王欣(女）不再参加值班、李沛衡暂不参加值班，张驰、沈全从新员工转为老员工（可担任值班经理）
holiday = ["20180924", "20180929","20180930", "20181001", "20181002", "20181003", "20181004", "20181005", "20181006",
           "20181007", "20181229", "20181230", "20181231", "20190101",
           "20190202", "20190203", "20190204", "20190205", "20190206", "20190207", "20190208", "20190209", "20190210",
           "20190405", "20190406", "20190407",
           "20190501", "20190502", "20190503",
           "20190607", "20190608", "20190609","20190913",
           "20191001", "20191002", "20191003", "20191004", "20191005", "20191006", "20191007",
           "20191228", "20191229", "20191230", "20191231", "20200101"]
#节假日前一个交易日
holiday_lastday = ["20180921","20180928","20181228", "20190201", "20190404","20190430","20190606","20190912","20190930","20191227"]
#节假日后一个交易日
holiday_nextday = ["20180925","20181008","20190102", "20190211", "20190408","20190506", "20190610","20190916","20191008","20200102"]


#和宋老师对接的转化字典
SongDict={'A1':'hw', 'A2':'dzt', 'A3':'srk', 'A4':'zyh', 'A5':'bk', 'A6':'sq', \
           'B1':'spc', 'B2':'wxl', 'B3':'yhr', 'B4':'wmy', 'B5':'yl', 'B6':'czh', 'H4':'yanglei', \
           'C1':'wyj', 'C2':'lph', 'C3':'lsj', 'C4':'zky', 'C5':'cj', 'C6':'lyc', 'C7':'fjk',  \
           'D1':'zn', 'D2':'zmm', 'D3':'xyj', 'D4':'wxlv', \
           'E1':'dxj', 'E2':'gxy', 'E3':'zxs', 'E4':'gzq', \
           'F1':'wel', 'F2':'lal', 'F3':'sml', 'F4':'czlv', 'F5':'fs',\
           'G1':'yqq', 'C8':'sxm', \
           'H1':'dlm', 'H2':'zc', 'H3':'zyf', \
           'I1':'wsg', 'I2':'ccm', 'I3':'ht' }#, 20190311 by songml#'I4':'yxl', \
           #'J1':'wx'} #20190311 by songml


##########################初始化员工列表#####################
# 主岗列表
list_main = ['A1', 'A2', 'B1', 'C1', 'D1', 'D2', 'E1', 'F1', 'G1', 'H1', 'I1']# 20190311, 'J1']
# 新人列表
list_new = ['H4', 'H3', 'I2', 'I3', 'C3', 'C6', 'C7'] 
# 女员工列表
list_women = ['F2', 'F4', 'G1', 'G2', 'I2', 'I3', 'C8']
# 非主岗老员工
list_group_A = ['A3', 'A4', 'A5', 'A6']
list_group_B = ['B2', 'B3', 'B4', 'B5', 'B6']
list_group_C = ['C3', 'C4', 'C5', 'C6', 'C7', 'C8']#,'C2']
list_group_D = ['D3']#, 'D4']
list_group_E = ['E2', 'E3', 'E4']
list_group_F = ['F2', 'F3', 'F4', 'F5']
#list_group_G = ['G2']
list_group_H = ['H2', 'H3', 'H4']
list_group_I = ['I2', 'I3']

######人员列表####顺序和计数器中的顺序硬应该保持一致，否则计数混乱###############
map = [
       'A1', 'A2', 'A3', 'A4', 'A5', 'A6', \
       'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'H4', \
       'C1', 'I3', 'C3', 'C4', 'C5', 'C6', 'C7', \
       'D1', 'D2', 'D3', 'I2', \
       'E1', 'E2', 'E3', 'E4', \
       'F1', 'F2', 'F3', 'F4', 'F5',\
       'G1', 'C8', \
       'H1', 'H2', 'H3', \
       'I1'#, 'D4','C2' #20190513 by songml I3<=>C2 <I2=>D4, 删除C2，D4为了保持计数器不串位，相应调整csv表 \
       #'J1'   #20190311
       ]




