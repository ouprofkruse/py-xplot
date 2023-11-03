import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
import math

GLYPHS = {"vtick":"\u2502", "htick":"\u2501", "dtick":"\u2577", "utick":"\u2575", \
          "rtick":"\u2576", "ltick":"\u2574", "uarrow":"\u25B2", "darrow":"\u25BC", \
            "larrow":"\u25C0", "rarrow":"\u25B6", "dot":"\u25AA", ".":"\u25AA", \
              "plus":"\u002B", "+":"+", "box":"\u25A2", "diamond":"\u2662", \
                 "x":"x", "mark":"\u25CE" }

COLOR = ("k", "b", "g", "r", "c", "m", "y", "k")

command_list=[]

def command_parse(data_in):
    def set_color(cmd,n):
        cc=0
        if (len(cmd) > n):
            cc=int(cmd[n].strip())
            cc = min(cc,len(COLOR)-1)
            cc = max(cc,0)
        return COLOR[cc]
    j=0
    cl=[["units","",""]]
    while j<len(data_in):
        command = data_in[j].strip().split()
        j+=1
        if (command[0] == "title"):
            cl.append(["title",data_in[j].strip()])
            j+=1
        elif (command[0] == "xlabel"):
            cl.append(["xlabel",data_in[j].strip()])
            j+=1
        elif (command[0] == "ylabel"):
            cl.append(["ylabel",data_in[j].strip()])
            j+=1
        elif (command[0] == "xunits"):
            cl[0][1] =  " ("+data_in[j].strip()+")"
            j+=1
        elif (command[0] == "yunits"):
            cl[0][2] =  " ("+data_in[j].strip()+")"
            j+=1
        elif (command[0] == "line"):
            cl.append(["line",[float(command[1]),float(command[3])],[float(command[2]),float(command[4])],\
                       set_color(command,5)])
        elif (command[0] == "arrow"):
            cl.append(["arrow",[float(command[1]),float(command[2]),\
                        float(command[3]),float(command[4])],\
                        set_color(command,5)])
        elif (command[0] == "dline"):
            cl.append(["line",[float(command[1]),float(command[3])],[float(command[2]),float(command[4])],\
                       set_color(command,5)])
            cl.append(["glyph","mark",float(command[1]),float(command[2]),set_color(command,5)])
            cl.append(["glyph","mark",float(command[3]),float(command[4]),set_color(command,5)])
        elif (command[0] == "invisible"):
            cl.append(["invis",float(command[1]),float(command[2])])
        elif (command[0] == "ctext"):
            cl.append(["text",data_in[j].strip(),float(command[1]),float(command[2]),"center","center"])
            j+=1
        elif (command[0] == "rtext"):
            cl.append(["text",data_in[j].strip(),float(command[1]),float(command[2]),"left","center"])
            j+=1
        elif (command[0] == "ltext"):
            cl.append(["text",data_in[j].strip(),float(command[1]),float(command[2]),"right","center"])
            j+=1
        elif (command[0] == "atext"):
            cl.append(["text",data_in[j].strip(),float(command[1]),float(command[2]),"center","bottom"])
            j+=1
        elif (command[0] == "btext"):
            cl.append(["text",data_in[j].strip(),float(command[1]),float(command[2]),"center","top"])
            j+=1
        elif (command[0] in GLYPHS):
            cl.append(["glyph",command[0],float(command[1]),float(command[2]),set_color(command,3)])
    return cl

def plotter(cl):
    limits=[math.inf,-math.inf,math.inf,-math.inf]

    def update_limits(lim,x,y):
        return [min(lim[0],x),max(lim[1],x),min(lim[2],y),max(lim[3],y)]
    
    fig, ax = plt.subplots()
    for item in cl:
        cmd = item[0]
        match cmd:
            case "title":
                ax.set_title(item[1])
            case "xlabel":
                ax.set_xlabel(item[1] + cl[0][1])
            case "ylabel":
                ax.set_ylabel(item[1] + cl[0][2])
            case "line":
                ax.plot(item[1],item[2],color=item[3])
                limits=update_limits(limits,item[1][0],item[2][0])
                limits=update_limits(limits,item[1][1],item[2][1])
            case "arrow":
                plt.arrow(item[1][0],item[1][1],item[1][2]-item[1][0],item[1][3]-item[1][1],\
                          color=item[2])
                limits=update_limits(limits,item[1][0],item[1][1])
                limits=update_limits(limits,item[1][2],item[1][3])
            case "invis":
                limits=update_limits(limits,item[1],item[2])
            case "text":
                x = item[2]
                y = item[3]
                ax.text(x,y,item[1],ha=item[4],va=item[5])
                limits=update_limits(limits,x,y)
            case "glyph":
                x = item[2]
                y = item[3]
                ax.text(x,y,GLYPHS[item[1]],ha="center",va="center",color=item[4])
                limits=update_limits(limits,x,y)
            case _:
                continue
    ax.set_xlim(limits[0],limits[1])
    ax.set_ylim(limits[2],limits[3])
    plt.show()

in_file = "demo-files/demo.0"
if (len(sys.argv) > 1):
    in_file = sys.argv[1]
fh = open(in_file)
lines = fh.readlines()

command_list = command_parse(lines)
#print(command_list)

plotter(command_list)
