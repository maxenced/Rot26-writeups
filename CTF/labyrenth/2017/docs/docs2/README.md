What a nice challenge !

In this docs2 challenge, you get 1337 doc files. Once again, you're asked to enable macro.

# 1 Macro per day is okay ...

So, let's look to some macroses in some random files, they all look like :

```vbnet
Private Sub Document_Open()
If ActiveDocument.Variables("zJTxqS").Value <> "wadoz" Then
GJmLhJxtSqFSSGx
ActiveDocument.Variables("zJTxqS").Value = "wadoz"
If ActiveDocument.ReadOnly = False Then
ActiveDocument.Save
End If
End If
End Sub

-------------------------------------------------------------------------------
VBA MACRO FfwMwxA.bas
in file: pkg/lab_1_file.doc - OLE stream: u'Macros/VBA/FfwMwxA'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Private Function sUPofBHPpg(BJcRgNedRY As Variant, SSUsYPSWRa As Integer)
Dim PkQzVmeRsW, vNyQDXSsCa As String, hrBvomJTpj, bbSHicjpnn
vNyQDXSsCa = ActiveDocument.Variables("zJTxqS").Value()
PkQzVmeRsW = ""
hrBvomJTpj = 1
While hrBvomJTpj < UBound(BJcRgNedRY) + 2
bbSHicjpnn = hrBvomJTpj Mod Len(vNyQDXSsCa): If bbSHicjpnn = 0 Then bbSHicjpnn = Len(vNyQDXSsCa)
PkQzVmeRsW = PkQzVmeRsW + Chr(Asc(Mid(vNyQDXSsCa, bbSHicjpnn + SSUsYPSWRa, 1)) Xor CInt(BJcRgNedRY(hrBvomJTpj - 1)))
hrBvomJTpj = hrBvomJTpj + 1
Wend
sUPofBHPpg = PkQzVmeRsW
End Function
Public Function GJmLhJxtSqFSSGx()
mXHYDYcv = sUPofBHPpg(Array(27, 30, 5, 1, 8, 11, 13, 92, 10, 29, 25, 85, 34, 17, 32, 16, 12, 46, 6, 15, 22, _
34, 73, 124, 45, 1, 23, 35, 13, 21, 40, 0, 7, 17, 72, 42, 45, 16, 18), 561)
BEChyIOD = sUPofBHPpg(Array(33, 27, 59, 57, 23, 123, 57, 36, 40, 53, 21, 72, 32, 25, 38, 35, 25, 26, 119, 20, 41, _
118, 15, 23, 49, 16, 119, 114, 114, 122, 36, 15, 18, 9, 22, 66, 117, 120, 0, 14, 57, _
0, 56, 41, 22, 54, 77, 24, 109, 36, 112, 43, 51, 35, 43, 37, 15, 37, 27, 22, 117, _
1, 56, 27, 37, 119, 112, 36, 9, 26, 42, 117, 27, 8, 1, 28, 57, 11, 7, 6, 48, _
59, 15, 20, 121, 48, 76, 34, 25, 84, 32, 15, 14, 4, 10, 54, 12, 54, 2, 52, 14, _
4, 37, 45, 43, 53, 37, 16, 13, 33, 14, 119, 18, 27, 56, 0, 4, 14, 42, 4, 38, _
47, 22, 55, 36, 23, 98, 0, 54, 62, 5, 22, 23, 21, 36, 13, 48, 114, 40, 2, 36, _
5, 119, 50, 16, 22, 112, 10, 49, 117, 51, 45, 59, 23, 3, 48, 24, 41, 22, 18, 58, _
44, 56, 85, 46, 112, 11, 3, 28, 48, 21, 0, 46, 113, 119, 43, 40, 100, 16, 46, 39, _
36, 124, 47, 29, 37, 15, 15, 40, 0, 15, 47, 16, 39, 118, 87, 8, 43, 97, 55, 49, _
48, 27, 49, 19, 112, 34, 19, 63, 56, 47, 52, 12, 2, 13, 115, 44, 53, 55, 31, 8, _
15, 114, 41, 43, 42, 38, 3, 39, 16), 13)
vXdDrhSV = sUPofBHPpg(Array(42, 23, 113, 4, 15, 2, 2, 34, 10, 11, 13, 30, 14, 9, 56, 0, 32, 119, 36, 120, 45, _
15, 57, 44, 3, 121, 33, 57, 40, 94, 39, 15, 42, 20, 124, 114, 46, 51, 114, 50, 61, _
52, 33, 20, 19, 47, 39, 2, 57, 53, 34, 52, 44, 38, 23, 49, 11, 116, 120, 45, 116, _
87, 51, 115, 49, 46, 3, 45, 113, 53, 50, 33, 9, 47, 34, 45, 51, 16, 46, 112, 113, _
46, 11, 37, 4, 51, 35, 12, 59, 6, 25, 121, 21, 107, 48, 10, 36, 34, 21, 27, 50, _
13, 22, 122, 73, 37, 122, 6, 41, 2, 53, 53, 120, 23, 44, 50, 52, 124, 121, 15, 57, _
23, 60, 6, 14, 62, 7, 119, 0, 50, 120, 41, 112, 86, 116, 51, 50, 20, 28, 22, 113, _
51, 114, 115, 49, 51, 19, 116, 0, 49, 2, 48, 8, 44, 58, 19, 112, 16, 32, 119, 42, _
47, 17, 15, 3, 119, 50, 19, 52, 55, 124, 53, 118, 23, 49, 117, 9, 3, 39, 15, 37, _
15, 27, 123, 2, 119, 57, 8, 116, 12, 34, 15, 37, 23, 47, 55, 26, 1, 51, 116, 57, _
27, 11, 18, 15, 116, 56, 32, 28, 49, 120, 49, 45, 14, 19, 49, 60, 5, 30, 42, 18, _
127, 39, 32, 39, 120, 33, 0, 10, 76), 331)
KWYNkLDy = sUPofBHPpg(Array(117, 117, 24, 40, 31, 117, 9, 17, 6, 24, 29, 117, 9, 51, 27, 105, 49, 38, 12, 120, 26, _
15, 34, 7, 44, 20, 124, 20, 15, 4, 12, 29, 25, 118, 3, 43, 117, 50, 119, 125, 114, _
60, 23, 50, 90, 40, 9, 22, 36, 57, 7, 46, 98, 11, 53, 21, 22, 60, 8, 11, 10, _
22, 46, 18, 56, 46, 18, 46, 59, 32, 115, 26, 51, 30, 105, 27, 37, 11, 123, 96, 22, _
46, 41, 2, 49, 34, 50, 121), 243)
VgafpjZU = mXHYDYcv + BEChyIOD + vXdDrhSV + KWYNkLDy
VBodWvPv = sUPofBHPpg(Array(99, 61, 107, 29, 44, 3, 60, 127), 600)
Dim Obj As Object
Set Obj = CreateObject(sUPofBHPpg(Array(5, 101, 47, 34, 28, 69, 76, 66, 106, 39, 49, 11, 59), 0))
Obj.Run VgafpjZU, 1
End Function
```

What we have here :

 * a variable with random name (`zJTxqS` here) which is used in the macro itself
 * a private function which does some xor stuff
 * a public function which call the private "crypto" func many times and, at the end, does a "CreateObject" and run it

This is basically the same kind of macro than docs1, easy enough to understand. The only issue ... you have 1337 of them.

# ... but three macroses brings problem

No way, I won't parse the 1337 ones by hand. What I decided to do is write some script to:

 * extract the macro
 * find variable name and extract the var
 * store the macro with it's variable in some file.

for each document !

## Uno to the rescue

[Uno](https://api.libreoffice.org/) is the name of LibreOffice API. Yes, there is an api, and yes, your LibreOffice can listen on some socket !

So first thing first , run libreoffice so that it listens on some socket:

```bash
$ soffice --headless --invisible --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
```

Then, start python code. The code to contact the API is not really ... straightforward to understand, and is taken from various websites. Here it is :

```python
def main():
    retVal = 0
    doc = None
    stdout = False

    try:
        stdout = True

        ctxLocal = uno.getComponentContext()
        smgrLocal = ctxLocal.ServiceManager

        resolver = smgrLocal.createInstanceWithContext(
                 "com.sun.star.bridge.UnoUrlResolver", ctxLocal )
        url = "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
        ctx = resolver.resolve( url )
        smgr = ctx.ServiceManager
        msp = ctx.getValueByName("/singletons/com.sun.star.script.provider.theMasterScriptProviderFactory")
        sp = msp.createScriptProvider("")

        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx )

        cwd = systemPathToFileUrl( getcwd() )

        inProps = PropertyValue( "Hidden" , 0 , True, 0 ),
```

I'm not sure if these in/outProps are really needed, but it worked that way.

At this point, we have only opened a connection to our soffice instance. Then we open each document :

```python
        wrong = []
        for index in range(1,1338):
            path = "lab_%s_file.doc" % index
            try:
                fileUrl = absolutize( cwd, systemPathToFileUrl(path) )
                doc = desktop.loadComponentFromURL( fileUrl , "_blank", 0, inProps )
```

Nothing too magic here, just create full file path, and ask my instance to open it.

### Parse document

So, now the document is opened, we need to:

 * Get the macro name. For this we get all macroses and remove the default ones

```python
                # Find macro name
               	macro_name = list(doc.BasicLibraries.getByName('Project').getElementNames())
                macro_name.remove('ThisDocument')
                if 'Module1' in macro_name:
                    macro_name.remove('Module1')
                #print(macro_name)
                assert(len(macro_name) == 1)
                macro_name = macro_name[0]
                # print("Doc[%s] : Found macro name %s, fetch it" % (index, macro_name))

                # Get macro
                macro_code = doc.BasicLibraries.getByName('Project').getByName(macro_name)
                assert("ActiveDocument.Variables" in macro_code)
```

 * Get the variable with random name used in macro

```python
                # Get User defined variable
                property_name = [ l for l in macro_code.split('\n') if "ActiveDocument.Variables" in l ][0].split('"')[1]
                assert(property_name != '')
                property_value = doc.getDocumentProperties().getUserDefinedProperties().getPropertyValue(property_name)
```

 * replace the macro variable with its value in vba

```python
                macro_code = re.sub(re.compile("Active.*$", re.MULTILINE), '"%s"' % property_value, macro_code)
```

 * and save the macro in some file:
```python
                with open('/tmp/%s.macro.vba' % index,'w') as output:
                    output.write(macro_code)
```

Nice. Now we have 1337 vba, but no idea how to exec it :/ I can't find a way to push and exec a macro in soffice through Uno.

So, once again, python to the rescue !

## And now it goes insane

So, in docs1, I converted the vba macro to python ... by hand. No, I won't do it by hand for 1337 files, so let's script it.
This is basically a find & replace function so that this dirty vba becomes some nice python :

```python
def vba2py(payload):
    """ Convert the VBA macro to py
    """
    res = []
    indent = 0
    inArray = False
    cur_func = None
    first_func = None
    first_func_count = 0
    last_func = None

    for l in payload.split('\n'):
        if not l:
            continue

        # Line without interest
        if 'Option' in l or 'Rem Attribute' in l:
            continue

        # Variable definition
        if 'Dim ' in l:
            l = l.replace('Dim ','')
            for sub_l in l.split(','):
                sub_l = re.sub(' As [^ ]+','',sub_l)
                res.append('%s%s = None' % ('    ' * indent, sub_l.lstrip()))
            continue

        if "CInt" in l:
            l = re.sub('CInt\(([^\)]+)\(([^\)]+)\)',r'int(\1[\2]',l)

        if 'Obj.Run' in l:
            l = "print(%s)" % l.split(' ')[1].replace(',','')
            res.append('%s%s' % ('    ' * indent, l.lstrip()))
            continue

        # if Ubound, replace by len(x) - 1
        if 'UBound' in l:
            l = re.sub(r'UBound\(([^\)]+)\)',r'len(\1) - 1 ', l)

        # Function definition
        if 'Private Function' in l or 'Public Function' in l:
            indent += 1
            l = re.sub('(Private|Public) Function ', 'def ',l)
            l = re.sub(' As [a-zA-Z]+','',l)
            cur_func = l.split(' ')[1].split('(')[0]
            if first_func is None:
                first_func = cur_func
            last_func = cur_func
            res.append(l.lstrip() + ':')
            continue

        # End of function / Loop, just de-indent of 1 level
        if 'End Function' in l:
            cur_func = None
            indent -= 1
            continue

        if 'Wend' == l:
            indent -= 1
            continue

        if cur_func is not None and cur_func in l:
            l = l.replace("%s = " % cur_func, "return ")

        # Ensure we don't indent more than once
        toIndent = False

		# Simple replace
        l = l.replace('Set Obj = ','')
        l = l.replace('CreateObject','print')
        l = l.replace('Mod','%')
        l = l.replace(' Xor ',' ^ ')
        l = l.replace('Chr','chr')
        l = l.replace('Asc','ord')
        l = l.replace('Len','len')

		# Manage single line if
        if ': If ' in l:
            lleft,lright = l.split(' If ')
            res.append('%s%s' % ('    ' * indent, lleft.lstrip().replace(':','')))
            res.append(re.sub(r' *([a-zA-Z]+).*Then ([^ ]+) = len\((.+)\)',r'%sif \1 == 0:\n%s\2 = len(\3)' % ('    ' * indent, '    ' * (indent +1)),lright))
            continue

        # match multiline stuff
        if l[-1] == '_':
            l = l[:-1] # Remove leading '_'

        if 'Mid(' in l:
            l = re.sub(r'Mid\(([^,]+), *([^,]+), *([0-9]+)\)', r'\1[\2-1:\2+\3-1]', l)

        if 'Array(' in l:
            l = l.replace('Array(','[')
            inArray = True

        # Close array if in Array
        if inArray and ')' in l:
            inArray = False
            l = l.replace(')',']',1)  # Change first parenthesis to array close

        # We need to get the 5th call to first_func to print it
        if first_func is not None and first_func in l:
            first_func_count += 1
            if first_func_count == 5:
                res.append("%s%s" % ('    ' * indent, l.lstrip()))
                position = l.split(' ')[0]
                res.append(('    ' * indent ) + 'print("POS:"+' + position + ')')
                continue

        # While loop
        if 'While' in l:
            l = l.replace('While','while')
            l += ':'
            toIndent = True

        res.append("%s%s" % ('    ' * indent, l.lstrip()))

        if toIndent:
            toIndent = False
            indent += 1

    res.append('%s()' % last_func)
    return('\n'.join(res))
```

Once we have this, we can also save our 1337 python files :

```python
                with open('/tmp/%s.macro.py' % index,'w') as output:
                    output.write(vba2py(macro_code))
```

## Run the pycros

So, then, we just run our 1337 macro files, and we see that most of the time we get a "POSITION" string printed, and sometimes a string like 'ONE', 'TWO' up to 'SEVENTEEN'.
We just ignore the results with POSITION, and sort the others :

```python
interesting = {}
for i in range(1,1338):
    out = str(subprocess.check_output("python3 /tmp/%s.macro.py" % i, shell=True))
    if 'POSITION' in out:
        continue
    else:
        pos = out.split('\\n')[0].split(':')[-1]
        b64data = out.split('\n')[-1].split(' ')[-1].replace("'",'').replace('\\n','')
        data = base64.b64decode(b64data)
        interesting[pos] = data

print("## Step 3 : Print FLAG")
for p in ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','TWELVE','THIRTEEN','FOURTEEN','FIFTEEN','SIXTEEN','SEVENTEEN']:
    print('\n'.join(interesting[p].decode("utf-8").split('\n')[2:8]))
```

And here you get the flag, in ASCII art :)

For thoses who are interested, I put the full python script ;)
