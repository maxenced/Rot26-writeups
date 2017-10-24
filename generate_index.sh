#!/bin/bash

DST="index.md"

echo -e "# Rot26 WriteUps \n" > $DST

for ctf in CTF/*;do
    echo "" >> $DST
    echo "## ${ctf##*/}" >> $DST
    for year in ${ctf}/*;do
        echo "### ${year##*/}" >> $DST
        for cat in ${year}/*;do
            for chall in ${cat}/*;do
                _cat=${cat##*/}
                _chall=${chall##*/}
                echo " * [*${_cat}* : ${_chall}]($chall)" >> $DST
            done
        done
    done
done
