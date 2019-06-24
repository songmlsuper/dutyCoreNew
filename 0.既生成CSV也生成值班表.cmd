@echo off
echo 请输入起始及结束月份以生成相应的值班表
echo 如果仅生成一个月份的值班表月份相同
set /p a=请输入起始月份(格式 YYYYMM):
set /p b=请输入结束月份(格式 YYYYMM):
@python.exe Date_control2.py %a% %b%
@java -jar dutyDB.jar %a% %b%
@pause