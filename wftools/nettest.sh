#!/bin/sh  
  
rm time_cost  
i=0  
times=100  
url="http://warframe.market/api/get_orders/Set/Ash Prime Set"
while [ $i -le $times ]  
do  
        #echo "call time "`date +%Y%m%d_%H_%M_%S` >> time_cost   
        curl -o j_out -s -w "%{time_connect}:%{time_starttransfer}:%{time_total}" "${url}" >> time_cost  
        let "i++"  
        echo '' >> time_cost  
        sleep 2  
done  
