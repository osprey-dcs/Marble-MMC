#! /usr/bin/python3

# A bunch of common tools for formatting output for C header files

import time

def makeFileName(s):
    s = str(s).lower()
    return "{}.h".format(s)

def makeHDef(s):
    return "__{}_H_".format(s.upper())

def sectionLine(s, width = 80):
    width = max(width, len(s) + 6)
    fmt = "/* {:=^" + str(width - 6) + "} */"
    return fmt.format(" {} ".format(s))

def write(msg, fd=None):
    if fd is None:
        print(msg)
    else:
        fd.write(msg + '\n')

def getDateTimeString(fmt = None):
    ts = time.localtime()
    if fmt is not None and fmt.lower() == TIME_FORMAT_MDY:
        date = "{1}/{2}/{0}".format(ts.tm_year, ts.tm_mon, ts.tm_mday)
    else:
        date = "{0:04}-{1:02}-{2:02}".format(ts.tm_year, ts.tm_mon, ts.tm_mday)
    ltime = "{:02}:{:02}".format(ts.tm_hour, ts.tm_min)
    return (date, ltime)

def writeHeader(fd, prefix, filename=None, scriptname=None):
    dateString, timeString = getDateTimeString()
    hdef = makeHDef(prefix)
    l = (
        "/*",
        " * File: {}".format(filename),
        " * Date: {}".format(dateString),
        " * Desc: Header file for {}. Auto-generated by {}.".format(prefix, scriptname),
        " */\n",
        "#ifndef {0}\n#define {0}\n\n#ifdef __cplusplus\n extern \"C\" {{\n#endif\n".format(hdef)
        )
    s = '\n'.join(l)
    write(s, fd)
    return

def writeFooter(fd, prefix):
    # Write footer
    hdef = makeHDef(prefix)
    s = "\n#ifdef __cplusplus\n}\n#endif"
    write(s, fd)
    s = "\n#endif /* {} */".format(hdef)
    write(s, fd)


