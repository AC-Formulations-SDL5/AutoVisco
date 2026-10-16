# 32-bit viscometer worker

`worker32.py` runs in a **32-bit Python** environment and talks to the Brookfield torquemeter through the
manufacturer's communication library `DVT_COM.dll`.

The DLL is proprietary to AMETEK Brookfield and is **not redistributed** in this repository.
Copy `DVT_COM.dll` from your Brookfield software installation into this folder before running the
hardware stack. Everything else (analysis, simulation, web interface in demo mode, tests) runs without it.
