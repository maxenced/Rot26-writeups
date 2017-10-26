#!/bin/bash

DST="index.md"

rm -f $DST

echo -e "\n# WriteUps\n" >> $DST

for ctf in CTF/*;do
    echo "" >> $DST
    echo "## ${ctf##*/}" >> $DST
    _ctf=${ctf##*/}
    echo -e "---\ntitle: \"${_ctf}\"\nlayout: category\n---" > category/${_ctf}.md
    echo "# ${_ctf}" >> category/${_ctf}.md
    for year in ${ctf}/*;do
        echo "### ${year##*/}" >> $DST
        for cat in ${year}/*;do
            for chall in ${cat}/*;do
                _cat=${cat##*/}
                _chall=${chall##*/}
                echo " * [*${_cat}* : ${_chall}](/gh-pages-test/$chall)" >> $DST
                echo " * [*${_cat}* : ${_chall}](/gh-pages-test/$chall)" >> category/${_ctf}.md
            done
        done
    done
done
