#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 11:52:37 2021

@author: aline
"""

import pysftp

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# Make connection to sFTP
with pysftp.Connection(hostname,
                       username=sftp_username,
                       password=sftp_pw,
                       cnopts = cnopts
                       ) as sftp:
    sftp.isfile('directory/file.csv')) ## TRUE
    file = sftp.get('directory/file.csv', '/local/path/file.csv')
    print(file) ## None

sftp.close()