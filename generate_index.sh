#!/bin/bash

DST="index.md"

rm -f $DST

echo -e "\n# WriteUps\n" >> $DST

for ctf in CTF/*;do
    echo "" >> $DST
    echo "## ${ctf##*/}" >> $DST
    _ctf=${ctf##*/}
    _ctf_title=${__ctf//_/ }
    echo -e "---\ntitle: \"${_ctf_title}\"\nlayout: category\n---" > category/${_ctf}.md
    echo "# ${_ctf}" >> category/${_ctf}.md
    for year in ${ctf}/*;do
        echo "### ${year##*/}" >> $DST
        for cat in ${year}/*;do
            for chall in ${cat}/*;do
                _cat=${cat##*/}
                _chall=${chall##*/}
                echo " * [*${_cat}* : ${_chall}](/$chall)" >> $DST
                echo " * [*${_cat}* : ${_chall}](/$chall)" >> category/${_ctf}.md
            done
        done
    done
done
