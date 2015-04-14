import re, sys, os

empty_line       = "^[ \t]*$"

macro_syntax     = "<<[ \t]*" \
                 + "([a-zA-Z][a-zA-Z0-9_]*|[*])" \
                 + "[ \t]*>>" 

macro_assignment = macro_syntax + "=[ \t]*$"
macro_value      = macro_syntax + "[ \t]*$"


def error(text, filename, linenum):
    print "Error ("+filename+":"+str(linenum)+"): "+text

def abort(text, filename, linenum):
    error(text, filename, linenum)
    sys.exit(1)

def getindent(line):
    return len(line) - len(line.lstrip(' '))


def compress_blank_lines(container):
    last_line_empty = False

    newcontainer = []

    for line in container:
        line = line.rstrip()
        if (re.match(empty_line, line)):
            if last_line_empty == True:
                pass
            else:
                newcontainer.append(line)

            last_line_empty = True
        else:
            newcontainer.append(line)
            last_line_empty = False

    return newcontainer


def process_file(filename):

    content = open(filename).readlines()

    code_container = {}
    code_container["*"] = []

    doc_container = []

    indentLevel = indent = 0
    macro_identifier = None

    last_line_empty = False
    linenum = 0

    for line in content:
        linenum += 1

        line = line.rstrip()
        indent = getindent(line)

        add_line = True

        if indent > 0:

            macro_indent    = "^" \
                            + "[ ]"*indent

            assign = re.match(macro_indent + macro_assignment, line)
            value  = re.match(macro_indent + macro_value,      line)

            if (assign):
                indentLevel = indent
                macro_identifier = assign.group(1)

                if not macro_identifier in code_container:
                    code_container[macro_identifier] = []
                code_container[macro_identifier].append([])

                doc_container.append("\n")

                add_line = False

            elif (value):
                try:
                    for s in code_container[value.group(1)]:
                        code_container[macro_identifier][-1].extend(s)

                except KeyError:
                    abort("Invalid macro reference: '"+value.group(1)+"'",filename,linenum)

                add_line = False

        else:
            if not (re.match(empty_line, line)):
                if last_line_empty == True:
                    if indentLevel > 0:
                        code_container[macro_identifier][-1].pop()

                    indentLevel = 0

                doc_container.append("\n")


        if add_line == True:
            doc_container.append(line)

            if indentLevel > 0:
                code_container[macro_identifier][-1].append(line[indentLevel:])

        if (re.match(empty_line, line)):
            last_line_empty = True
        else:
            last_line_empty = False


    return code_container, doc_container

def write_container(filename, container):

    f = open(filename,"w")

    container = compress_blank_lines(container)
    for l in container:
#        print l
        f.write(l+"\n")

    f.close()


def write_codefile(filename, code_container):

    final = []

    for c in code_container:
        final += c

    write_container(filename, final)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='A sequential literate processor.')
    parser.add_argument('filename', metavar='FILE', nargs=1, help='lit file to process')
    parser.add_argument('-c','--code', action='store_true', help='build final source file')
    parser.add_argument('-d','--doc', action='store_true', help='build markdown documentation')

    args = parser.parse_args()

    if (not args.code) and (not args.doc):
        print "Error: Current selection will do nothing!"
        print "Add '-c' to generate code or '-d' for documentation"
        sys.exit(1)


    filename = args.filename[0]
    code, doc = process_file(filename)

    codefile = os.path.splitext(filename)[0]

    if args.doc:
        write_container(codefile+".md",doc)

    if args.code:
        write_codefile(codefile, code["*"])

