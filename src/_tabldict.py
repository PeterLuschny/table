from Tables import TablesList
from _tabltypes import Table
from _tabloeis import QueryOEIS
from _tablutils import SeqToString
from _tablpaths import GetRoot
from _tabltraits import AllTraits
from typing import Dict
import json

# #@


GlobalDict: Dict[str, Dict[str, int]] = {}


def ShowGlobalDict() -> None:
    global GlobalDict
    for tabl, dict in GlobalDict.items():
        print(f"*** Table {tabl} ***")
        for trait in dict:
            print(f"    {trait} -> {dict[trait]}")


def FilterDict(olddict: Dict[str, int] )  -> Dict[str, int]:
    anumlist: set[int] = set()
    newdict: Dict[str, int] = {}
    for k, v in olddict.items():
        if not v in anumlist: 
            newdict[k] = v
        anumlist.add(v)
    return newdict


def AddAnumsToSrcfile(name: str, dict: Dict[str, int] = {}) -> None:
    global GlobalDict

    if dict == {}:
        ReadJsonDict()
        dict = GlobalDict[name]

    srcpath = GetRoot(f"src/{name}.py")
    with open(srcpath, "a+", encoding="utf-8") as dest:
        d = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
        dest.write("\n\n" + r"'''" + " OEIS\n")
        for fullname, anum in d.items():
            if anum != 0:
                dest.write(f"    {fullname} -> https://oeis.org/A{anum}\n")
            else:
                dest.write(f"    {fullname} -> 0 \n")

        misses = len([v for v in d.values() if v == 0])
        hits = len(d.values()) - misses
        distincts = len(set(d.values()))

        dest.write(f"\n    {name}: Distinct: {distincts}, Hits: {hits}, Misses: {misses}")
        dest.write("\n" + r"'''" + "\n")


def AnumberDict(
    T: Table, 
    info: bool = False,
    addtoglobal: bool = False
) -> Dict[str, int]:
    """Collects the A-nunmbers of the traits of T present in the OEIS."""
    
    global GlobalDict
    print(f"*** Table {T.id} under construction ***")

    tdict: Dict[str, int] = {}
    for trid, tr in AllTraits.items():
        name = (T.id + "_" + trid).ljust(10 + len(T.id), " ")
        seq: list[int] = tr[0](T, tr[1]) 
        if seq != []:
            tdict[name] = QueryOEIS(seq, info)

    if addtoglobal:
        GlobalDict[T.id] = tdict

    return tdict

header = '<!DOCTYPE html lang="en"><head><title>Traits</title><meta charset="utf-8"><meta name="viewport" content="width=device-width"><script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"> window.MathJax = {loader: {load: ["[tex]/bbox"]}, tex: {packages: {"[+]": ["bbox"] } } }</script></head><body width="40%"><iframe name="OEISframe" scrolling="yes" width="58%" height="2200" align="left" title="Sequences"'

def DictToHtml(
    T: Table, 
    dict: Dict[str, int],
    info: bool = False
)  -> tuple[int, int, int]:
    """Transforms a dictionary {trait, anum} representing the Table T
        into two Html files: TNameTraits.html and TNameMissing.html.
        A trait is 'missing' if the anum in the dictionary is 0.
    """

    SRC = f'https://oeis.org/{T.sim[0]}'
    TID = (T.id).capitalize()
    SH = f'src={SRC}></iframe><p><span style="white-space: pre">     {TID}</span><br>'
    hitpath = GetRoot(f"docs/{T.id}Traits.html")
    mispath = GetRoot(f"docs/{T.id}Missing.html")
    head = header.replace("Traits", T.id)
    TeX = r"\(\bbox[yellow, 5px]{\color{DarkGreen} T_{n, k} \ = \ TTEX } \)" 
    TEX = TeX.replace("TTEX", T.tex)
    url = f"<a href='https://oeis.org/{T.sim[0]}' target='OEISframe'>{T.sim[0]}</a> "
    hits = misses = doubles = 0
    anumlist: set[int] = set()
    oldanum = T.sim[0] 

    with open(hitpath, "w+", encoding="utf-8") as oeis:
        with open(mispath, "w+", encoding="utf-8") as miss:
            oeis.write(head); oeis.write(SH); oeis.write(url + TEX)
            miss.write(head); miss.write(SH); miss.write(url + TEX)
            d = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}

            for fullname, anum in d.items():
                if info: 
                    print(f"    {fullname} -> {anum}") # prints sorted dict 
                
                traitfun, size, tex = AllTraits[fullname.split("_")[1]]
                seq = SeqToString(traitfun(T, size), 40, 20) 
                if anum == 0:
                    miss.write(f"<br>{tex} &nbsp;&#x27A4;&nbsp; {fullname.split("_")[1]} &nbsp;&#x27A4;&nbsp; " + seq)
                    misses += 1
                else:
                    if anum in anumlist: 
                        doubles += 1
                    Anum = 'A' + str(anum).rjust(6, "0")
                    if anum == oldanum:
                        url = '---------- '
                    else:
                        url = f"<a href='https://oeis.org/{Anum}' target='OEISframe'>{Anum}</a>"
                    oldanum = anum 
                    oeis.write(f"<br>{url} {tex} &nbsp;&#x27A4;&nbsp; {fullname.split("_")[1]} &nbsp;&#x27A4;&nbsp; " + seq)
                    hits += 1
                    anumlist.add(anum)

            L = "<a href='https://peterluschny.github.io/table/"
            A = f"{L}{T.id}Traits.html'>[online]</a>"
            B = f"{L}{T.id}Missing.html'>[missing]</a>"
            C = f"{L}index.html'>[index]</a>"

            oeis.write(f"<p style='color:blue'>{B}{C}</p></body></html>")
            miss.write(f"<p style='color:blue'>{A}{C}</p></body></html>")

    distincts = len(anumlist)
    print(f"{T.id:17}, Distinct: {distincts}, Hits: {hits}, Misses: {misses}")
    return (distincts, hits, misses)


indheader = "<!DOCTYPE html><html lang='en'><head><title>Index</title><meta name='viewport' content='width=device-width,initial-scale=1'><style type='text/css'>body{font-family:Calabri,Arial,sans-serif;font-size:18px;background-color: #804040; color: #C0C0C0}</style><base href='https://peterluschny.github.io/table/' target='_blank'></head><body><table><thead><tr><th align='left'>Sequence</th><th align='left'>OEIS</th><th align='left'>Missing</th></tr></thead><tbody><tr>"

def warn() -> None:
    print("Are you sure? This takes 3-4 hours.")
    print("Don't forget to update Tables.py first.")
    print("Delete the json file?")
    print("Hit return >")
    input()

def RefreshDatabase() -> None:
    """Use with caution."""
    #warn()
    
    global GlobalDict
    ReadJsonDict()

    indexpath = GetRoot(f"docs/index.html")
    with open(indexpath, "w+", encoding="utf-8") as index:
        index.write(indheader)

        for T in TablesList:
            dict = AnumberDict(T, True, True)  # type: ignore 
            DictToHtml(T, dict, False)         # type: ignore
            index.write(f"<tr><td align='left'>{T.id}</td><td align='left'><a href='{T.id}Traits.html'>[online]</a></td><td align='left'><a href='{T.id}Missing.html'>[missing]</a></td></tr>")

            AddAnumsToSrcfile(T.id, dict)

        index.write("</tbody></table></body></html>")
        index.flush()

    # Save to a JSON file
    jsonpath = GetRoot(f"data/AllTraits.json")
    with open(jsonpath, 'w') as fileson:
        json.dump(GlobalDict, fileson)


def ReadJsonDict() -> None:
    global GlobalDict
    jsonpath = GetRoot(f"data/AllTraits.json")
    try:
        with open(jsonpath, 'r') as file:
            GlobalDict = json.load(file)
    except FileNotFoundError:
        print("No file 'AllTraits.json' found.")
        GlobalDict = {}
        print("New GlobalDict created.")
        return

    print("GlobalDict loaded with file AllTraits.json!")


def AddTable(
    T: Table,
    dict: Dict[str, int] = {}
) -> Dict[str, int]:
    ReadJsonDict()

    if dict == {}:    #info, add2globalDict
        dict = AnumberDict(T, True, True)
    print("Dict length:", len(dict))
    DictToHtml(T, dict, True)
    jsonpath = GetRoot(f"data/AllTraits.json")
    with open(jsonpath, 'w+') as fileson:
        json.dump(GlobalDict, fileson)
    return dict


def RefreshHtml(filter: bool=False) -> None:
    global GlobalDict
    ReadJsonDict()
    for T in TablesList:
        try:
            dict = GlobalDict[T.id]
            if filter:
                dict = FilterDict(dict)
            DictToHtml(T, dict)    # type: ignore
            print(T.id, "dict length:", len(dict))
            T.set_impact(len(dict))
        except KeyError as e: 
            print("KeyError:", e)
            input()
            pass


def OccList() -> None:
    Occurences: Dict[int, list[str]] = {}
    ReadJsonDict()
    li: set[int] = set()
    for d in GlobalDict.values():
        for name, anum in d.items():
            li.add(anum)
            if anum in Occurences: 
                Occurences[anum].append(name)
            else: 
                Occurences[anum] = [name]

    for anum, names in Occurences.items():
        if len(names) > 10:
            print(str(anum).rjust(6, "0"), len(names))
    print(sorted(li), len(li))


if __name__ == "__main__":

    from Abel import Abel                # type: ignore
    from AbelInv import AbelInv          # type: ignore
    from Power import Power              # type: ignore
    from BinaryPell import BinaryPell    # type: ignore
    from FallingFactorial import FallingFactorial  # type: ignore
    from Divisibility import Divisibility  # type: ignore
    from Moebius import Moebius          # type: ignore
    from CatalanInv import CatalanInv    # type: ignore
    from WardSet import WardSet          # type: ignore
    from LahInv import LahInv            # type: ignore

    AddTable(LahInv) # type: ignore

    # OccList()
    # RefreshHtml(True)
    # RefreshDatabase()

    #for T in TablesList:
    #    print(T.id, T.tex)

    #ReadJsonDict()

    #for k, v in GlobalDict.items():
    #    print(k, len(v.values()))

    #AddAnumsToSrcfile("Fubini")

    #for k, v in dict.items():
    #    print(k, v)
