# U Know Dev ? 

Ce challenge nécessitait de se connecter à un socket qui envoie un bout de code.

Une fois ce bout de code exécuté, on renvoie le résultat, ça en envoie un nouveau, et  ainsi de suite.

En faisant quelques tests on se rend compte qu'il y a 4 languages :

 * php
 * c
 * brainfuck
 * python

En tentant d'en compiler un de chaque à la main on se rend compte que :

 * le code brainfuck exécuté avec  _hsbrainfuck_ ajoute un retour à la ligne
 * le code C ne compile pas tel quel, il faut enlever le char()
 * le code Python print les char 1 par ligne

Une fois ces petites contrariétés passées, le code est (moche mais) simple:

```ruby
#!/usr/bin/ruby
#

require 'socket'

hostname = '10.119.227.42'
port = 52000
s = TCPSocket.open(hostname, port)

iter = 0
11.times { s.gets }


def brainfuck(code)
  open('code.bf', 'w') { |f|
    f.puts code
  }
  return `cat code.bf | hsbrainfuck |head -1`
end

def php(code)
  open('code.php', 'w') { |f|
    f.puts code
  }
  return `php5 code.php`
end

def python(code)
  open('code.py', 'w') { |f|
    f.puts code
  }
  return `python2 code.py |xargs echo | tr -d ' '`
end

def c(code)
  open('code.c', 'w') { |f|
    f.puts code.gsub('char(','').gsub('))',')')
  }
  `gcc -o a.out code.c`
  return `./a.out`
end

while code = s.gets
  print code
  line = code
  if code =~ /\+\+\+\+/
    print "Got brainfuck code : #{code}"
    res = brainfuck(code)
  elsif code =~ /include/
    while line !~ /}/
      line = s.gets
      code += line
    end
    print "Got c code : #{code}"
    res = c(code)
  elsif code =~ /php/
    while line !~ /\?>/
      line = s.gets
      code += line
    end
    print "Got php code : #{code}"
    res = php(code)
  elsif code =~ / = \[/
    while line !~ /print/
      line = s.gets
      code += line
    end
    print "Got python code : #{code}"
    res = python(code)
  else
    print("Unknown code : #{code}")
     next
  end
  print "Send result #{res}"
  s.puts res
        iter += 1
  res = ''
end

print "Did #{iter-1} iterations"

```

Et on récupère le flag :

```bash
$ ruby run.rb
[...]
bzhctf{H0pefully_n0_J4v4_h3r3}
Did 200 iterations
```
