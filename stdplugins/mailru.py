import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
import asyncio
import time
from sample_config import Config
from uniborg.util import admin_cmd
from datetime import datetime




@borg.on(admin_cmd(pattern=("mailru ?(.*)"))) # pylint:disable=E0602
async def _(event):
    url = event.pattern_match.group(1)
    if event.fwd_from:
        return
    event.pattern_match.group(1)
    datetime.now()
    try:
        time.time()
        await event.edit("Finish downloading to my local")
        command_to_exec = [
                "./bin/cmrudl.py",
                url,
                "-d",
                "./DOWNLOADS/"
                ]
        process = await asyncio.create_subprocess_shell(
        command_to_exec, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout.decode():
            std = stdout.decode()
            stds = std.split("\n")
            std1 = stds[1]
            std2 = stds[2]
            std3 = stds[3]
            out = str(std1)+"\n"+str(std2)+"\n"+str(std3)
            await event.edit(f"**{out}**")
        if stderr.decode():
            await event.edit(f"**{stderr.decode()}**")
            return
    except Exception as e:
        print(e)
