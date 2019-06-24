@echo off
set /p a=请输入起始月份:
set /p b=请输入结束月份:
@python.exe Date_Control2.py %a% %b%
@pause