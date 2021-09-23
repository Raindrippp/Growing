第一版

#! /usr/bin/bash

t=$1
kubeadm alpha certs check-expiration | sed -n '5,14p' | awk '{print $7}' | sort -r | sed 's/.$'// > a.txt
min_time=$(sed -n "1,1p" a.txt | awk '{print $1}')
if [ $min_time -lt $t ]
        then
                kubeadm alpha certs renew all
fi
