#!/bin/sh

net=$(iwgetid -r)
if ["$net" = "KIT-WLAP2"];then
    export https_proxy=http://wwwproxy.kanazawa-it.ac.jp:8080/
    export http_proxy=http://wwwproxy.kanazawa-it.ac.jp:8080/
else
    export https_proxy=''
    export http_proxy=''
fi

source ./env/bin/activate

roslaunch spr_speak spr_speak.launch
