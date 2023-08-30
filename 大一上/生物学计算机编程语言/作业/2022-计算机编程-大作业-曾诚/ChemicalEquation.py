from sympy import Matrix, symbols
from sympy import solve_linear_system
import re
from functools import reduce
from math import gcd


def getFormulaList(chemicalEquation):
    chemicalEquation1,chemicalEquation2=chemicalEquation.replace(" ","").split('=') #按=拆开
    leftFormulaList=chemicalEquation1.split('+')
    rightFormulaList=chemicalEquation2.split('+')
    return leftFormulaList,rightFormulaList

def getFormulaListTransform(chemicalEquation):
    chemicalEquation1,chemicalEquation2=chemicalEquation.replace(" ","").split('=')
    leftFormulaList=chemicalEquation1.split('+')
    rightFormulaList=chemicalEquation2.split('+')
    leftFormulaList = [Transform(x) for x in leftFormulaList]
    rightFormulaList = [Transform(x) for x in rightFormulaList]
    return leftFormulaList,rightFormulaList

def Transform(formula):
    #去除括号，作相应变化  Fe2(SO4)3 => Fe2SO4SO4SO4
    if "(" in formula:
        elemContent = re.match(r".*\((.*)\).*", formula).group(1)
        elemCount =re.findall(r'(\d+)',formula)[-1]
        formula = formula.replace(f"({elemContent}){elemCount}",elemContent*int(elemCount))
    #继续作变换 Fe2SO4SO4SO4 => FeFeSOOOOSOOOOSOOOO
    pattern="[A-Z]"
    elemList=re.sub(pattern,lambda x:" "+x.group(0),formula)
    elemList = elemList.split()
    for j in range(len(elemList)):
        e = elemList[j]     
        for i in range(len(e)):
            if e[i].isnumeric():
                elemList[j]=e[:i]*int(e[i:])
                break
    return ''.join(elemList)   


def getElem(FormulaList):
    elemList = []
    for f in FormulaList:
        for w in f:
            if w.isupper():
                elemList.append(w)
            if w.islower():
                elemList[-1]+=w
    return set(elemList)



def checkChemicalEquation(chemicalEquation):
    ok=True
    message=""
    illegalWordList =list("`~!@$%^&*_-[];',./\{\}:'|<>，。！￥…——《》\"")
    #判断是否存在非法字符
    for word in illegalWordList:
        if word in chemicalEquation:
            ok=False
            message="Error:exist a illegal word %s"%(word)
    #判断是否存在唯一的=
    if chemicalEquation.count("=")!=1:
            ok=False
            message="Error:more than one \'=\'"
    leftFormulaList,rightFormulaList=getFormulaListTransform(chemicalEquation)
    leftElem=getElem(leftFormulaList)
    rightElem=getElem(rightFormulaList)
    #判断左右元素是否一致
    if leftElem!=rightElem:
        ok=False
        message="Error:Reactant and product contain different elements"
    return message,ok

#获取分母
def getDenominator(ans):
    vals = ans.values()
    denominatorList = []     
    #例如  b/2  那么获取分母为2
    for v in vals:
        if '/' in v:
            denominatorList.append(int(v.split('/')[-1]))
    return denominatorList

def getLcm(numbers):
    return reduce((lambda x, y: int(x * y / gcd(x, y))), numbers)


def getBalanceCoefficient(leftFormulaList,rightFormulaList,elemList):
    #获取线性方程组系数矩阵
    M=[]
    L=[]
    for e in elemList:
        for f in leftFormulaList:
            L.append(f.count(e))
        for f in rightFormulaList:
            L.append(-f.count(e))
        L.append(0)
        M.append(L)
        L=[]
    M = Matrix(M)
    
    count = M.shape[1]-1
    sml = []
    for i in range(count):
        sml.append(symbols(chr(i+97)))							
    cmd = "res = solve_linear_system(M,"
    for i in range(count):
        cmd += "sml[" +str(i)+"]" +','
    cmd = cmd[:-1]+")"
    exec(cmd)
    rr = locals()['res']
    res_dict={}
    for k,v in rr.items():
        res_dict[str(k)] = str(v)
    denominatorList=getDenominator(res_dict)
    lcm=getLcm(denominatorList)
    for alph in res_dict['a']:
        if alph.isalpha():
            break
    for k,v in res_dict.items():
        exp = str(v).replace(alph,str(lcm))
        val = int(eval(exp))
        res_dict[k] = val
    res_dict[alph] = lcm
    resList = sorted(res_dict.keys())
    ans = [res_dict[i] for i in resList]
    return ans



def balancerChemicalEquation(chemicalEquation):
    formulaList1,formulaList2=getFormulaList(chemicalEquation)
    leftFormulaList,rightFormulaList=getFormulaListTransform(chemicalEquation)
    elemList=getElem(rightFormulaList)
    coefficientList=getBalanceCoefficient(leftFormulaList,rightFormulaList,elemList)
    #获得系数后，给化学方程式配平
    ans = ''
    for i,c in enumerate(formulaList1):
        coe = ''
        if coefficientList[i] != 1:
            coe = coefficientList[i]
        ans+=str(coe) + c + " + "
    ans = ans[:-2]
    ans += "= "
    for i,c in enumerate(formulaList2):
        coe = ''
        if coefficientList[i+len(formulaList1)] != 1:
            coe = coefficientList[i+len(formulaList1)]
        ans+=str(coe) + c + " + "
    ans = ans[:-2]
    return ans


def getBalancerAnswer(chemicalEquation):
    message,ok=checkChemicalEquation(chemicalEquation)
    if ok==False:
        return message
    return balancerChemicalEquation(chemicalEquation)


