@echo off
echo ��������ʼ�������·���������Ӧ��ֵ���
echo ���������һ���·ݵ�ֵ����·���ͬ
set /p a=��������ʼ�·�(��ʽ YYYYMM):
set /p b=����������·�(��ʽ YYYYMM):
@python.exe Date_control2.py %a% %b%
@java -jar dutyDB.jar %a% %b%
@pause