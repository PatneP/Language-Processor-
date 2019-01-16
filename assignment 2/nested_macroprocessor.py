def checkForMacro(line):
    l = line.split()
    if l[0].lower() == "macro":
        return 1
    elif l[0].lower() == "mend":
        return 0
    elif l[0].lower() == "end":
        return 2
    return -1
def searchMNT(mnt, key):
    for i in range(len(mnt)):
        if key == mnt[i]:
            return i
    return -1
ExpandedMacro = []
def expandMacro(fl, mnt, mdt, para, pos):
    for i in range(len(fl)):
        y = fl[i].split()
        position = searchMNT(mnt, y[0])
        if position != -1:
            if para[position] == 0:
                start = pos[position] - 1
                if position == len(pos) - 1:
                    end = len(mdt)
                else:
                    end = pos[position + 1] - 1
                for j in range(start, end):
                    data = mdt[j].split()
                    posi = searchMNT(mnt, data[0])
                    if posi == -1:
                        ExpandedMacro.append(mdt[j])
                    else:
                        ans = []
                        ans.append(mdt[j])
                        expandMacro(ans, mnt, mdt, para, pos)
            else:
                actvspos = {}
                w = y[1].split(",")
                for i in range(len(w)):
                    actvspos["#" + str(i + 1)] = w[i]
                start = pos[position] - 1
                if position == len(pos) - 1:
                    end = len(mdt)
                else:
                    end = pos[position + 1] - 1
                for j in range(start, end):
                    w = mdt[j].split()
                    posi = searchMNT(mnt, w[0])
                    if posi != -1:
                        ans = []
                        ans.append(mdt[j])
                        expandMacro(ans, mnt, mdt, para, pos)
                    else:
                        x = w[1].split(",")
                        l = []
                        for k in range(len(x)):
                            l.append(actvspos[x[k]])
                        x = ",".join(l)
                        w = w[0] + " " + x
                        ExpandedMacro.append(w)
        else:
            ExpandedMacro.append(fl[i])

def macroProcess(fl):
    m1 = []
    mnt = []
    para = []
    pos = []
    mdt = []
    prev = 0
    check = 0
    for i in range(len(fl)):
        m = checkForMacro(fl[i])
        if prev == 1 and m == -1:
            if check == 1:
                y = fl[i].split()
                l = []
                for i in range(len(y)):
                    if y[i][0] == '&':
                        w = formvspos[y[i]]
                        l.append(w)
                    else:
                        l.append(y[i])
                fl[i] = " ".join(l)
            mdt.append(fl[i])
        if m == 2:
            break
        if prev == 0 and m != 1:
            m1.append(2)
        else:
            m1.append(m)
        if m == 1:
            x = fl[i].split()
            mnt.append(x[1])
            pos.append(len(mdt) + 1)
            if len(x) <= 2:
                para.append(0)
                check = 0
            else:
                y = x[2].split(",")
                para.append(len(y))
                check = 1
                formvspos = {}
                for i in range(len(y)):
                    formvspos[y[i]] = "#" + str(i + 1)
            prev = 1
        elif m == 0:
            prev = 0
    output = []
    finalExpansion = []
    for i in range(len(m1)):
        if m1[i] == 2:
            finalExpansion.append(fl[i])
    expandMacro(finalExpansion, mnt, mdt, para, pos)
    ExpandedMacro.append("END")
    output = "\n".join(ExpandedMacro)
    return output
def main():
    t = input()
    f = open(t, "r")
    fl = f.readlines()
    fl = "".join(fl)
    fl = fl.split("\n")
    output = macroProcess(fl)
    f.close()
    f = open("output.txt", "w")
    f.write(output)
    f.close()
    print(output)
if __name__ == '__main__':
    main()
