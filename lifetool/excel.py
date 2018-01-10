#!/usr/bin/python
# -*- coding:utf-8 -*- 

from dateutil.relativedelta import relativedelta
import datetime

class  ExcelTool:
    def getSBNTitle(self):
        row = {}
        row['eid'] = 'Employee ID'
        row['empl_rcd'] = 'Empl Rcd'
        row['ecode'] = 'Earning Code'
        row['effective_date'] = 'Effective Date'
        row['addtional_sequence'] = 'Additional Sequence'
        row['payment_amount'] = 'Payment Amount'
        row['ok_to_pay'] = 'OK To Pay'
        row['currency'] = 'Currency'
        row['start'] = 'Start Date'
        row['end'] = 'End Date'
        row['vcp'] = 'VCP %'
        output=''
        output += "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(row['eid'],row['empl_rcd'],row['ecode'],row['effective_date'],row['addtional_sequence'],row['payment_amount'],row['ok_to_pay'],row['currency'],row['start'],row['end'],row['vcp'])
        return output

    def getSBNContent(self,eid,startDate,firstYearBonus,secondYearBonus):
        startDate = str(startDate)
        startTS =  datetime.datetime.strptime(startDate,"%Y%m%d")
        #打印表头
        row = {}
        output=''
        #设置不变量
        row['eid'] = eid
        row['empl_rcd'] =0
        row['ecode'] = 'SBN'
        row['addtional_sequence'] = 1
        row['ok_to_pay'] = 'Y'
        row['currency'] = 'CNY'
        row['vcp'] = ''
        firstYearCount = 0;
        secondYearCount = 0
        for n in range(1,25):
            #设置变量\

            edata = startTS + relativedelta(months=n-1)
            row['effective_date'] = edata.strftime("%d-%b-%y")
            if n<12:
                row['payment_amount'] = round(firstYearBonus/12.00,2)
                firstYearCount += row['payment_amount']
            elif n==12:
                row['payment_amount'] = firstYearBonus - firstYearCount
            elif n >12 and n <24:   
                row['payment_amount'] = round(secondYearBonus/12.00,2)
                secondYearCount += row['payment_amount']
            elif n == 24:
                row['payment_amount'] = secondYearBonus - secondYearCount
            row['start'] = row['effective_date']    
            row['end'] = (edata+relativedelta(months=1,days=-1)).strftime("%d-%b-%y")
            output += "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(row['eid'],row['empl_rcd'],row['ecode'],row['effective_date'],row['addtional_sequence'],row['payment_amount'],row['ok_to_pay'],row['currency'],row['start'],row['end'],row['vcp'])

#        file_object = open('SBN.csv', 'w')
 #       file_object.write(output)
  #      file_object.close( )
 
        return output

#fobj = open('sbn.csv','w')
#fobj.write(ExcelTool().getSBNContent(12345678,20171122,150000,120000))
#fobj.close()

#print ExcelTool().getSBNContent(12345678,20171122,150000,120000)

