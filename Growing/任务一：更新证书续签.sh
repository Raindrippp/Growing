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
