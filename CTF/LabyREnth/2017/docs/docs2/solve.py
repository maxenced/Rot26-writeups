#!/usr/bin/env python3

# Run soffice with :
# soffice --headless --invisible --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
#
# Then run this script


import getopt, sys
import uno
import base64
import subprocess
import re
from unohelper import Base, systemPathToFileUrl, absolutize
from os import getcwd, system
from os.path import splitext
from com.sun.star.beans import PropertyValue
from com.sun.star.uno import Exception as UnoException
from com.sun.star.io import IOException, XOutputStream

class OutputStream( Base, XOutputStream ):
    def __init__( self ):
        self.closed = 0
    def closeOutput(self):
        self.closed = 1
    def writeBytes( self, seq ):
        sys.stdout.write( seq.value )
    def flush( self ):
        pass

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
        outProps = (
#            PropertyValue( "FilterName" , 0, filterName , 0 ),
            PropertyValue( "Overwrite" , 0, True , 0 ),
            PropertyValue( "OutputStream", 0, OutputStream(), 0)
        )

        inProps = PropertyValue( "Hidden" , 0 , True, 0 ),
# 97, 169, 211
        wrong = []
        for index in range(1,1338):
            path = "lab_%s_file.doc" % index
            try:
                fileUrl = absolutize( cwd, systemPathToFileUrl(path) )
                doc = desktop.loadComponentFromURL( fileUrl , "_blank", 0, inProps )
#                print(doc)

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

                # Get User defined variable
                property_name = [ l for l in macro_code.split('\n') if "ActiveDocument.Variables" in l ][0].split('"')[1]
                assert(property_name != '')
                # print("Doc[%s]: Found property name %s" % (index, property_name))

		# Find property value
                property_value = doc.getDocumentProperties().getUserDefinedProperties().getPropertyValue(property_name)
                # print("Doc[%s]: Found property value of length %s" % (index, len(property_value)))


                macro_code = re.sub(re.compile("Active.*$", re.MULTILINE), '"%s"' % property_value, macro_code)

                with open('/tmp/%s.macro.vba' % index,'w') as output:
                    # print("Doc[%s]: Write updated macro to macros/%s.macro.vba" % (index, index))
                    output.write(macro_code)

                with open('/tmp/%s.macro.py' % index,'w') as output:
                    # print("Doc[%s]: Write python macro to macros/%s.macro.py" % (index, index))
                    output.write(vba2py(macro_code))


#                scriptx = sp.getScript('vnd.sun.star.script:Standard.Module1.Main?language=Basic&location=application')
#                print(scriptx)
                if not doc:
                    raise UnoException( "Couldn't open stream for unknown reason", None )
                else:
                    doc.dispose()

        #        if not stdout:
        #            (dest, ext) = splitext(path)
        #            dest = dest + "." + extension
        #            destUrl = absolutize( cwd, systemPathToFileUrl(dest) )
        #            sys.stderr.write(destUrl + "\n")
        #            doc.storeToURL(destUrl, outProps)
        #        else:
        #            doc.storeToURL("private:stream",outProps)
            except IOException as e:
                sys.stderr.write( "Error during conversion: " + e.Message + "\n" )
                retVal = 1
            except UnoException as e:
                sys.stderr.write( "Error ("+repr(e.__class__)+") during conversion:" + e.Message + "\n" )
                retVal = 1
#            except Exception as e:
#                sys.stderr.write("Assertion error parsing document %s . Skipping it : %s" % (index, e))
#                wrong.append(index)
#                print(doc)
#                sys.exit(1)

    except UnoException as e:
        sys.stderr.write( "Error ("+repr(e.__class__)+") :" + e.Message + "\n" )
        retVal = 1
    except getopt.GetoptError as e:
        sys.stderr.write( str(e) + "\n" )
        usage()
        retVal = 1

#    sys.exit(retVal)

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

# TODO
        #    key = l.split(' ')[0]
        #    key2 = l.split(' ')[0]
        #    res.append('%s%s' % ('    ' * indent, "if %s == 0" % key))
        #    res.append('%s%s' % ('    ' * indent + 1, "%s = len(%s)" % (key,)))

        ###
        # Inline changes : may have more than one so don't break loop at the end of conditioin
        ###

        # Ensure we don't indent more than once
        toIndent = False

	# Simple replace
        l = l.replace('Set Obj = ','')
        l = l.replace('CreateObject','print')
        l = l.replace('Mod','%')
        l = l.replace(' Xor ',' ^ ')
        l = l.replace('Chr','chr')
        l = l.replace('Asc','ord')
#        l = l.replace('CInt','int')
        l = l.replace('Len','len')

	# Manage single line if
        if ': If ' in l:
            lleft,lright = l.split(' If ')
            res.append('%s%s' % ('    ' * indent, lleft.lstrip().replace(':','')))
            res.append(re.sub(r' *([a-zA-Z]+).*Then ([^ ]+) = len\((.+)\)',r'%sif \1 == 0:\n%s\2 = len(\3)' % ('    ' * indent, '    ' * (indent +1)),lright))
            continue

        # match multiline stuff
        if l[-1] == '_':
            l = l[:-1] # Remove leaing '_'

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

print("## Step 1 : extract VBA & convert VBA to Python")
main()
print("## Step 2 : Exec Python")
interesting = {}
for i in range(1,1338):
    out = str(subprocess.check_output("python3 /tmp/%s.macro.py" % i, shell=True))
#    print(out)
    if 'POSITION' in out:
#        print("Doc[%s]: found string 'POSITION', skipping it" % i)
        continue
    else:
        pos = out.split('\\n')[0].split(':')[-1]
        b64data = out.split('\n')[-1].split(' ')[-1].replace("'",'').replace('\\n','')
        data = base64.b64decode(b64data)
        interesting[pos] = data

print("## Step 3 : Print FLAG")
for p in ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','TWELVE','THIRTEEN','FOURTEEN','FIFTEEN','SIXTEEN','SEVENTEEN']:
    print('\n'.join(interesting[p].decode("utf-8").split('\n')[2:8]))
