#!/bin/bash

# for the fun (cuz I like doing stuff like this)
# full bash builtin version without pipe/subshell
# gov

mapfile < enc

declare -A dick_map

for line in ${MAPFILE[*]}; do

    [[ $line =~ ^# ]] && cyphertext=${line/\#/}

    if [[ $line =~ ^8 ]]; then
        line=${line/^/ }
        split=( ${line//::/ } )
        [[ ! ${dick_map[${split[3]}]} ]] && dick_map[${split[3]}]=${split[1]}
    fi

done

for (( x=0 ; x<${#cyphertext} ; x+=2 )){
    echo -en ${dick_map[${cyphertext:$x:2}]}
}
