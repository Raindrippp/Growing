第一版
#! /usr/bin/bash

t=$1
kubeadm alpha certs check-expiration | sed -n '5,14p' | awk '{print $7}' | sort -r | sed 's/.$'// > a.txt
min_time=$(sed -n "1,1p" a.txt | awk '{print $1}')
if [ $min_time -lt $t ]
        then
                kubeadm alpha certs renew all
fi









第二版
#! /usr/bin/bash
##########################################
# Function: 延长组件证书有效期           #
# Author: DingHang                       #
# CreateTime: 2021/9/27                  #
##########################################

T=$1
#输入最低有效期天数
kubeadm alpha certs check-expiration | grep -n -A9 'admin' | awk '{print $7}' | sort | sed 's/.$'//  > a.txt
#将各组件的剩余天数从小到大顺序排列存入a.txt文件中
MINI_TIME=$(sed -n "1,1p" a.txt | awk '{print $1}')
#取最小的有效期
if [ $MINI_TIME -lt $T ]
        then
                kubeadm alpha certs renew all
                #最小有效期低于要求时更新组件有效期
                if [ $? -eq 0 ]
                #判断上一步更新是否成功
        then
                echo "更新成功"
        #更新完成后提示更新成功
fi
else
                echo "无需更新"
                #最小有效期满足要求，无需更新。
fi

第三版
#! /usr/bin/bash
##########################################
# Function: 延长组件证书有效期           #
# Author: DingHang                       #
# CreateTime: 2021/9/27                  #
##########################################

set -o nounset
set -o errexit
#Sed -i 's/\r//' clear_sshd_process.sh  format the script.

# Export the LANG environment.
vOsType=$(uname | tr '[a-z]' '[A-Z]')
if [ "${vOsType}" = "AIX" -o "${vOsType}" = "LINUX" ];then
	export LANG=es_US.utf8
fi

T=$1
#输入最低有效期天数
MINI_TIME=$(kubeadm alpha certs check-expiration | grep -n -A9 'admin' | awk '{print $7}' | sed 's/.$'// | awk 'NR==1{min=$1;next}{min=min<$1?min:$1}END{print min}')
#在各组件的剩余天数取最小的有效期
if [ $MINI_TIME -lt $T ]
        then
                kubeadm alpha certs renew all
                #最小有效期低于要求时更新组件有效期
                if [ $? -eq 0 ]
                #判断上一步更新是否成功
        then
                echo "更新成功"
        #更新完成后提示更新成功
fi
else
                echo "无需更新"
                #最小有效期满足要求，无需更新。
fi









第四版
#! /usr/bin/bash
##########################################
# Function: 延长组件证书有效期           #
# Author: DingHang                       #
# CreateTime: 2021/9/27                  #
##########################################

set -o nounset
set -o errexit
#Sed -i 's/\r//' clear_sshd_process.sh  format the script.

# Export the LANG environment.
vOsType=$(uname | tr '[a-z]' '[A-Z]')
if [ "${vOsType}" = "AIX" -o "${vOsType}" = "LINUX" ];then
	export LANG=es_US.utf8
fi

T=$1
MINI_TIME1=$(kubeadm alpha certs check-expiration | grep  -A9 'admin' | awk '{print $7}' | grep 'd' | sed 's/.$'// | awk 'NR==1{min=$1;next}{min=min<$1?min:$1}END{print min}')
MINI_TIME2=$(kubeadm alpha certs check-expiration | grep  -A9 'admin' | awk '{print $7}' | grep 'y' | sed 's/.$'// | awk 'NR==1{min=$1;next}{min=min<$1?min:$1}END{print min}')
#输入最低有效期天数

if [ ! $MINI_TIME1 ]; then
  MINI_TIME=$(expr $MINI_TIME2 \* 365 )
else
  MINI_TIME=$MINI_TIME1
fi

if [ $MINI_TIME -lt $T ]
        then
                kubeadm alpha certs renew all
                #最小有效期低于要求时更新组件有效期
                if [ $? -eq 0 ]
                #判断上一步更新是否成功
        then
                echo "更新成功"
        #更新完成后提示更新成功
fi
else
                echo "无需更新"
                #最小有效期满足要求，无需更新。
fi









第五版
#! /usr/bin/bash
##########################################
# Function: 延长组件证书有效期           #
# Author: DingHang                       #
# CreateTime: 2021/9/27                  #
##########################################

set -o nounset
set -o errexit
#Sed -i 's/\r//' clear_sshd_process.sh  format the script.

# Export the LANG environment.
vOsType=$(uname | tr '[a-z]' '[A-Z]')
if [ "${vOsType}" = "AIX" -o "${vOsType}" = "LINUX" ];then
	export LANG=es_US.utf8
fi

T=$1
MINI_TIME1=$(kubeadm alpha certs check-expiration | grep  -A9 'admin' | awk '{print $7}' | grep 'd' | sed 's/.$'// | awk 'NR==1{min=$1;next}{min=min<$1?min:$1}END{print min}')
MINI_TIME2=$(kubeadm alpha certs check-expiration | grep  -A9 'admin' | awk '{print $7}' | grep 'y' | sed 's/.$'// | awk 'NR==1{min=$1;next}{min=min<$1?min:$1}END{print min}')
#输入最低有效期天数，区分年还是日。

if [ ! $MINI_TIME1 ]; then
  MINI_TIME=$(expr $MINI_TIME2 \* 365 )
else
  MINI_TIME=$MINI_TIME1
fi


function writeLog
{
    echo "$(date +'%Y-%m-%d %H:%M:%S') ${1}" 
} 

function renew()
{
	if [ $MINI_TIME -lt $T ]
			then
					kubeadm alpha certs renew all
					#最小有效期低于要求时更新组件有效期
					if [ $? -eq 0 ]
					#判断上一步更新是否成功
			then
					writeLog "更新成功"
			#更新完成后提示更新成功
	fi
	else
					writeLog "无需更新"
					#最小有效期满足要求，无需更新。
	fi
}


renew
exit 0
