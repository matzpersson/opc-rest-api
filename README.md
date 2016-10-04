# OPC Rest Api
Python Rest API using OpenOPC to provide direct API access for any OS platform. This proxy has to be installed on a Windows box with Python and OpenOPC installed to provide a API Gateway to other platforms.

# Dependencies
This code is dependent on https://sourceforge.net/projects/openopc/files/ by Barry Barnreiter and Python 2.7

# Installation
On your Windows server, install OpenOpc. Make sure that OpenOPC connects properly to your OPC Server. Documentation for OpenOPC on http://openopc.sourceforge.net/. Once OpenOPC is connected, download http2opc code above and drop it in your preferred diretory.

# Usage
Run python main.py from the http2opc directory to start the API Daemon. Function documentation on http://headstation.com/archives/using-opc-rest-api/

# Copyright
Copyright 2016 Headstation. (http://headstation.com) All rights reserved. It is free software and may be redistributed under the terms specified in the LICENSE file (Apache License 2.0). 
