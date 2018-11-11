import marshal
import sys
import os
import dis
import tempfile

def get_code(file):
    absfilename = os.path.abspath(file)
    fle = open(absfilename, 'rb')
    if sys.version_info.minor >= 7:
        ret = fle.read()[16:]
    else:
        ret = fle.read()[12:]
    fle.close()
    return marshal.loads(ret)

def get_dis(code):
    bts = bytes()
    fle = open('temp', 'w+')
    dis.dis(code, file=fle)
    fle.close()
    fle = open('temp', 'r')
    content = fle.read()
    fle.close()
    return f'''
{content}
    '''

def code_to_xml(code):
    if isinstance(code, str):
        return f'''
            {code}
        '''
    if not code:
        return ''
    return f''' <code>
        <co_argcount>{code.co_argcount}</co_argcount>
        <co_cellvars>{','.join(code.co_cellvars)}</co_cellvars>
        <co_code>{get_dis(code.co_code)}</co_code>
        <co_consts>{''.join(["<co_const>" + code_to_xml(x) + "</co_const>" for x in code.co_consts])}</co_consts>
        <co_filename>{code.co_filename}</co_filename>
        <co_firstlineno>{code.co_firstlineno}</co_firstlineno>
        <co_flags>{code.co_flags}</co_flags>
        <co_freevars>{','.join(code.co_freevars)}</co_freevars>
        <co_kwonlyargcount>{code.co_kwonlyargcount}</co_kwonlyargcount>
        <co_lnotab>{code.co_lnotab}</co_lntotab>
        <co_name>{code.co_name}</co_name>
        <co_names>{','.join(code.co_names)}</co_names>
        <co_nlocals>{code.co_nlocals}</co_nlocals>
        <co_stacksize>{code.co_stacksize}</co_stacksize>
        <co_varnames>{','.join(code.co_varnames)}</co_varnames>
    </code>'''

if __name__ == '__main__':
    pyc_file_name = sys.argv[1]
    out_file_name = sys.argv[2]
    pycode = get_code(pyc_file_name)
    xmlstring = code_to_xml(pycode)
    absoutname = os.path.abspath(out_file_name)
    out = open(absoutname, 'w')
    out.write(
            f'''<xml>
    {xmlstring}
</xml>'''
        )
    out.close()
    os.remove('temp')

