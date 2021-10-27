#! /usr/bin/bash
##########################################
# Function: 延长组件证书有效期           #
# Author: DingHang                       #
# CreateTime: 2021/9/27                  #
##########################################

set -o nounset
set -o errexit
#Sed -i 's/\r//'

# Export the LANG environment.
vOsType=$(uname | tr '[a-z]' '[A-Z]')
if [ "${vOsType}" = "AIX" -o "${vOsType}" = "LINUX" ];then
	export LANG=es_US.utf8
fi

T=$1
MINI_TIME1=$(kubeadm alpha certs check-expiration | grep  -A9 'admin' | awk '{print $7}' | grep 'd' | sed 's/.$'// | awk 'NR==1{min=$1;next}{min=min<$1?min:$1}END{print min}')
MINI_TIME2=$(kubeadm alpha certs check-expiration | grep  -A9 'admin' | awk '{print $7}' | grep 'y' | sed 's/.$'// | awk 'NR==1{min=$1;next}{min=min<$1?min:$1}END{print min}')
#

if [ ! $MINI_TIME1 ]; then
  MINI_TIME=$(expr $MINI_TIME2 \* 365 )
else
  MINI_TIME=$MINI_TIME1
fi
#get MINI_TIME

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
									writeLog  "更新成功"
									#更新完成后提示更新成功
	fi
	else
					writeLog "无需更新"
					#最小有效期满足要求，无需更新。
	fi
}


renew
exit 0
