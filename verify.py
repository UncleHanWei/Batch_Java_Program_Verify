import os, sys
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
import pprint
from time import sleep

def testHW(id_and_name, file, file_path) :
    print('測試', id_and_name)
    result = []
    global allTestData, students
    Popen('javac -encoding cp950 "' +file+'"',  stdout=PIPE, stdin=PIPE, stderr=STDOUT, cwd=file_path, close_fds=True).communicate()
    Popen('javac -encoding utf8 "' +file+'"',  stdout=PIPE, stdin=PIPE, stderr=STDOUT, cwd=file_path, close_fds=True).communicate()
    
    if file[:file.find('.')] + '.class' not in os.listdir(file_path) :
        students[id_and_name] += ['編譯錯誤']
    else :
        for i in range(0, len(allTestData), 2) :
            input = ''.join(allTestData[i])
            output = ''.join(allTestData[i+1]).strip()
            try :
                p = Popen('java "' +file[:file.find('.')]+'"',  stdout=PIPE, stdin=PIPE, stderr=STDOUT, cwd=file_path)
                stdout = p.communicate(input=bytes(input, 'utf-8'), timeout=1)[0]
                execRes = stdout.decode('cp950').replace('\r', '').strip()
                result.append(execRes)
                if execRes != output :
                    students[id_and_name] += ['程式無法正確執行測資 '+str(i//2+1)]
            except TimeoutExpired as time_err :
                # print(time_err)
                students[id_and_name] += ['程式執行測資 ' + str(i//2+1) + ' Timeout']
                p.kill()
            except Exception as e:
                # print(e)
                students[id_and_name] += ['程式無法正確執行測資 '+str(i//2+1)]
        print(result)

def getTestData(dirName) :
    global allTestData
    allFiles = os.listdir(dirName)
    for file in allFiles :
        if file == 'info' :
            continue
        with open(dirName + '\\' + file, 'r', encoding='utf8') as f :
            data = f.readlines()
            allTestData.append(data)
    print(allTestData)

def main(argv) :
    global root, students
    # argv[0] : 當前檔案名稱
    # argv[1] : 作業資料夾名稱
    # argv[2] : 作業檔案名稱
    root = os.path.dirname(os.path.realpath(__file__))
    if len(argv) == 1 :
        HWDirName = input('輸入要改的作業的資料夾名稱:')
        source = root + '\\' + HWDirName
        fileName = input('輸入要改的作業的檔案名稱:')

    elif len(argv) == 3 :
        source = root + '\\' + argv[1]
        fileName = argv[2]

    for eachDir in sorted(os.listdir(source), reverse=True) :
        if eachDir.endswith('.zip') :
            continue
        if 'test_cases' in eachDir :
            getTestData(source + '\\' + eachDir)
        else :
            id_and_name = eachDir[0:13]
            for eachfile in os.listdir(source+'\\' + eachDir) :
                if eachfile.endswith('.java') :
                    file = eachfile
            # 把每個學生的位置先做好一個空的 list，以便之後放進檢查狀態
            students[id_and_name] = []
            if file != fileName+'.java' :
                students[id_and_name] += ['檔名錯誤']
            file_path = source+'\\' + eachDir
            testHW(id_and_name, file, file_path)
    pprint.PrettyPrinter(indent=0).pprint(students)

# global variables
students = dict()
root = None
allTestData = list()

if __name__ == '__main__' :
    main(sys.argv)