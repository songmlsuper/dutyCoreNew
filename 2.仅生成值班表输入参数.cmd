@echo off
echo 请输入起始及结束月份以生成相应的值班表e.g.201810 201811
echo 如果仅生成一个月份的值班表e.g.201810 201810
set /p a=请输入起始月份:
set /p b=请输入结束月份:
@java -jar dutyDB.jar %a% %b%
@pause