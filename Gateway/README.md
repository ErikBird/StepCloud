# StepCloud Gateway

The StepCloud Gateway is a component of the StepCloud System.
It is responsible to monitor the selected devices in the network and upload the data into the cloud.

The system is designed to be deployed on a Raspberry Pie.

## Development Mode

Run python with the interpreter options `-X dev` to enable the developer mode.
In the developer mode, the gateway announces to be reachable on 0.0.0.0:7353 whereas it usually has its own IP Adress at
port 80.

## Architecture

For information related to the gateway architecture, please refer to [Architecture.md](src/Architecture.md).

## Compilation

Since the deployment of a compiled code is faster and easier, the software is distributed as binary.

To be able to compile the code you should follow the following steps:

**1. Run Pyinstaller:**

`pyinstaller --onefile cli.spec`

**2. Change Metadata (with versioning):**

`create-version-file metadata.yml --outfile file_version_info.txt`

**3. Create the spec file:**

`pyi-makespec --onefile main.py`

The specfile needs to be extended with:

`hiddenimports=['uvicorn.lifespan.off','uvicorn.lifespan.on','uvicorn.lifespan',
'uvicorn.protocols.websockets.auto','uvicorn.protocols.websockets.wsproto_impl',
'uvicorn.protocols.websockets_impl','uvicorn.protocols.http.auto',
'uvicorn.protocols.http.h11_impl','uvicorn.protocols.http.httptools_impl',
'uvicorn.protocols.websockets','uvicorn.protocols.http','uvicorn.protocols',
'uvicorn.loops.auto','uvicorn.loops.asyncio','uvicorn.loops.uvloop','uvicorn.loops',
'uvicorn.logging'],`
