@echo off
echo ��������ʼ�������·���������Ӧ��ֵ���e.g.201810 201811
echo ���������һ���·ݵ�ֵ���e.g.201810 201810
set /p a=��������ʼ�·�:
set /p b=����������·�:
@java -jar dutyDB.jar %a% %b%
@pause