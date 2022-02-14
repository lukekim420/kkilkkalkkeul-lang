import sys

class kkilkkalkkeul:
    def __init__(self):
        self.data=[0]*256
    
    def calc(self,code):
        if 'ㅋ' in code:
            var=code.split('ㅋ')[1]
            cmd=code.split('ㅋ')[2]
            dat=str(self.data[eval('*'.join(list(map(lambda cmd:str((self.data[cmd.count('낄')-1] if cmd.count('낄') else 0) + cmd.count('~') - cmd.count('.')), var.split(' ')))))-1])+'k'+cmd
            return eval('*'.join(list(map(lambda cmd:str((int(cmd.split('k')[0]) if 'k' in cmd else 0) + cmd.count('~') - cmd.count('.')), dat.split(' ')))))
        else:
            return eval('*'.join(list(map(lambda cmd:str((self.data[cmd.count('낄')-1] if cmd.count('낄') else 0) + cmd.count('~') - cmd.count('.')), code.split(' ')))))
    
    @staticmethod
    def getcmd(code):
        if '칼' in code:
            return 'IF'
        if '클' in code:
            return 'GOTO'
        if '끌' in code:
            return 'INPUT'
        if '킬' in code:
            if code[-3] == 'ㅋ':
                return 'ASCIIPRINT'
            if code[-3] != 'ㅋ' and code[-1] == 'ㅋ':
                return 'PRINT'
        if '깔' in code:
            return 'DEF'

    def compileline(self,code):
        if code == '':
            return None
        CMD=self.getcmd(code)

        if CMD=='DEF':
            var,cmd=code.split('깔')
            if 'ㅋ' in var:
                self.data[self.calc(var.split('ㅋ')[1])-1]=self.calc(cmd)
            else:
                self.data[var.count('낄')]=self.calc(cmd)
        elif CMD=='INPUT':
            if 'ㅋ' in code:
                self.data[self.calc((code.split('깔')[0]).split('ㅋ')[1])-1]=int(input())
            else:
                self.data[code.replace('깔','').count('낄')]=int(input())
        elif CMD=='PRINT':
            c=code[1:-1]
            print(self.calc(c),end='')
        elif CMD=='ASCIIPRINT':
            c=code[1:-3]
            value=self.calc(c)
            print(chr(value) if value else '\n',end='')
        elif CMD=='IF':
            cond,cmd=code.replace('칼','').split('?')
            if self.calc(cond)==0:
                return cmd
        elif CMD=='GOTO':
            return self.calc(code.replace('클',''))

    def compile(self,code,errors=100000):
        run = False
        recode = ''
        spliter = '!'
        code = code.rstrip().split(spliter)
        index = 0
        error = 0
        while index < len(code):
            errorline = index
            c = code[index].strip()
            res = self.compileline(c)
            if run:
                run = False
                code[index] = recode                
            if isinstance(res, int):
                index = res-2
            if isinstance(res, str):
                recode = code[index]
                code[index] = res
                index -= 1
                run = True

            index += 1
            error += 1
            if error == errors:
                raise RecursionError(str(errorline+1) + '번째 줄에서 무한 루프가 감지되었습니다.')
    def compilefile(self,path):
        with open(path,'r',encoding='UTF-8') as file:
            code="".join(file.readlines())
            self.compile(code)

a=kkilkkalkkeul()
a.compilefile("./2.txt")