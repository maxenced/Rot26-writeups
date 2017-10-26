#!/bin/bash

DST="index.md"

rm -f $DST

echo "# Members" >> $DST

echo "* [Fooker](https://twitter.com/Memoi2001)" >> $DST
echo "* [Kalimer0x00](https://twitter.com/kalimer0x00)" >> $DST
echo "* [Govlog](https://twitter.com/govlog)" >> $DST
echo "* [Sp4rKy](https://twitter.com/maxencedun)" >> $DST

echo -e "\n# WriteUps\n" >> $DST

for ctf in CTF/*;do
    echo "" >> $DST
    echo "## ${ctf##*/}" >> $DST
    _ctf=${ctf##*/}
    echo -e "---\ntitle: \"${_ctf}\"\nlayout: category\n---" > category/${_ctf}.md
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
