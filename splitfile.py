def split():
    startFlag = True
    pChrom = ''

    with open(chip,'r') as inFile:
        for line in inFile:
            l = line.split()
            currChrom = l[1]

            if startFlag:
                out = '{}_{}.bed'.format(l[1], chip)
                o = open(out,'w')
                pChrom = l[1]            
                startFlag = False
           
            if currChrom != pChrom:
                o.close()
                out = '{}_{}.bed'.format(l[1], chip)
                o = open(out,'w')
           
           o.write(line)