package main

import (
		"fmt"
        "strings"
)


func charCodeAt(s string, n int) rune {
    for i, r := range s {
        if i == n {
            return r
        }
    }
    return 0
}


func toHex(myStr string) string {
	var r string = ""
	letter := []string{"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"}

	for i := 0; i < len(myStr); i++ {
        r += letter[charCodeAt(myStr, i) >> 4] + letter[charCodeAt(myStr, i) & 15]
    }

	return r
}


func saxxCustomAlgorithmOrNot(myStr string) string {

	var init int = 0
	var out string = ""
	var value int

	for i := 0; i < len(myStr); i++ {
		value = int(charCodeAt(myStr, i))
		init ^= (value << 2) ^ value
		out  += string(init & 0xff) // pas bon ce qui emmene au replace a patcher
		init >>= 8
    }
	
	return strings.Replace(toHex(out), "00", "", -1)  ;
}


func main() {
	//fmt.Println(saxxCustomAlgorithmOrNot("BREIZHCTF{###REDACTED###}"))
	fmt.Println("4a1b506c33694e055f9605555550a4a5a54ad2d7227266226322e4afd2a0f0227de4224ebb9cb1a5d22250a5221ee49939224e22501e05227d22721111721e50a4a5a50455555088")
}