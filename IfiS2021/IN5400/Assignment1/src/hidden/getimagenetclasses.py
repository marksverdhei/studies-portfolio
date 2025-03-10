import json
import xml.etree.ElementTree as ET

root_path = '/home/binder/entwurf6/codes/tfplay/ai/imagenetdata'
filen = root_path + '/synset_words.txt'
nm = root_path + '/val/ILSVRC2012_val_00049999.xml'


def get_classes():
    with open("imagenetclasses.json", "r") as f:
        classes = json.load(f)
    return classes


def parsesynsetwords(filen):
    synsetstoclassdescriptions = {}
    indicestosynsets = {}
    synsetstoindices = {}
    ct = -1
    with open(filen) as f:
        for line in f:
            if (len(line) > 5):
                z = line.strip().split()
                descr = ''
                for i in range(1, len(z)):
                    descr = descr+' '+z[i]

                ct += 1
                indicestosynsets[ct] = z[0]
                synsetstoindices[z[0]] = ct
                synsetstoclassdescriptions[z[0]] = descr[1:]
    return indicestosynsets, synsetstoindices, synsetstoclassdescriptions


def test_parsesyn():
    indicestosynsets, synsetstoindices, synsetstoclassdescr = parsesynsetwords(
        filen)
    clsdict = get_classes()

    for i in range(1000):
        n1 = synsetstoclassdescr[indicestosynsets[i]]
        n2 = clsdict[i]

        if(n1 != n2):
            print(i)
            print('n1', n1, 'n2:', n2)


def testparse():
    tree = ET.parse(nm)
    root = tree.getroot()

    for obj in root.findall('object'):
        for name in obj.findall('name'):
            print(name.text)


def parseclasslabel(nm, synsetstoindices):
    tree = ET.parse(nm)
    root = tree.getroot()

    lbset = set()

    for obj in root.findall('object'):
        for name in obj.findall('name'):
            # print name.text
            ind = synsetstoindices[name.text]
            firstname = name.text
            lbset.add(ind)

    if len(lbset) != 1:
        print('ERR: len(lbset)!=1',  len(lbset))
        exit()

    for s in lbset:
        label = s
    return label, firstname


def test_parseclasslabel():
    (
        indicestosynsets, synsetstoindices, synsetstoclassdescr
    ) = parsesynsetwords(filen)

    label, firstname = parseclasslabel(nm, synsetstoindices)

    print(label, firstname,  synsetstoclassdescr[indicestosynsets[label]])
