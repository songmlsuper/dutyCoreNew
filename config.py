## 20190126  宋明霖  组人员调整F5 李松健 <=> C3 范嵩  ==> C3 李松健, F5 范嵩，去掉I4
## 20190201  宋明霖  fdh=>lph
##                   相应的角色也调整
#注意：除了更改初始列表外，还需要更改每个人的计数器求和函数
#节假日 使用git测试 test2
holiday = ["20180924", "20180929","20180930", "20181001", "20181002", "20181003", "20181004", "20181005", "20181006",
           "20181007", "20181229", "20181230", "20181231", "20190101",
           "20190202", "20190203", "20190204", "20190205", "20190206", "20190207", "20190208", "20190209", "20190210",
           "20190405", "20190406", "20190407",
           "20190501",
           "20190607", "20190608", "20190609","20190913",
           "20191001", "20191002", "20191003", "20191004", "20191005", "20191006", "20191007",
           "20191228", "20191229", "20191230", "20191231", "20200101"]
#节假日前一个交易日
holiday_lastday = ["20180921","20180928","20181228", "20190201", "20190404","20190430","20190606","20190912","20190930","20191227"]
#节假日后一个交易日
holiday_nextday = ["20180925","20181008","20190102", "20190211", "20190408","20190502","20190610","20190916","20191007","20200102"]


#和宋老师对接的转化字典
SongDict={'A1':'hw', 'A2':'dzt', 'A3':'srk', 'A4':'zyh', 'A5':'bk', 'A6':'sq', \
           'B1':'spc', 'B2':'wxl', 'B3':'yhr', 'B4':'wmy', 'B5':'yl', 'B6':'czh', 'B7':'yanglei', \
           'C1':'wyj', 'C2':'lph', 'C3':'lsj', 'C4':'zky', 'C5':'cj', 'C6':'lyc', 'C7':'fjk',  \
           'D1':'zn', 'D2':'zmm', 'D3':'xyj', 'D4':'wxlv', \
           'E1':'dxj', 'E2':'gxy', 'E3':'zxs', 'E4':'gzq', \
           'F1':'wel', 'F2':'lal', 'F3':'sml', 'F4':'czlv', 'F5':'fs',\
           'G1':'yqq', 'G2':'sxm', \
           'H1':'dlm', 'H2':'zc', 'H3':'zyf', \
           'I1':'wsg', 'I2':'ccm', 'I3':'ht', #'I4':'yxl', \
           'J1':'wx'}


##########################初始化员工列表#####################
# 主岗列表
list_main = ['A1', 'A2', 'B1', 'C1', 'D1', 'D2', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1']
# 新人列表
list_new = ['A6', 'B7', 'C6', 'C7', 'H2', 'H3', 'I2', 'I3', 'C3']
# 女员工列表
list_women = ['D4', 'F2', 'F4', 'G1', 'G2', 'I2', 'I3']
# 非主岗老员工
list_group_A = ['A3', 'A4', 'A5']
list_group_B = ['B2', 'B3', 'B4', 'B5', 'B6']
list_group_C = ['C2', 'C4', 'C5']
list_group_D = ['D3', 'D4']
list_group_E = ['E2', 'E3', 'E4']
list_group_F = ['F2', 'F3', 'F4', 'F5']
list_group_G = ['G2']

######人员列表####顺序和计数器中的顺序硬应该保持一致，否则计数混乱###############
map = [
       'A1', 'A2', 'A3', 'A4', 'A5', 'A6', \
       'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', \
       'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', \
       'D1', 'D2', 'D3', 'D4', \
       'E1', 'E2', 'E3', 'E4', \
       'F1', 'F2', 'F3', 'F4', 'F5',\
       'G1', 'G2', \
       'H1', 'H2', 'H3', \
       'I1', 'I2', 'I3',  \
       'J1'
       ]




