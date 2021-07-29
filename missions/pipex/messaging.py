from multiprocessing import Process, Queue
import sys
import os
import multiprocessing

import asyncio
import datetime
import random
import time
import json

def child_logic(r,s):
    # Add mission virtual environment
    global send
    global recv
    send = s
    recv = r
    
    try:
        sys.path.append('.\\data\\missions\\pipex\\Lib\\site-packages')
        
        import websockets
        start_server = websockets.serve(handler, "localhost", 8765)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        print(str(e))
        time.sleep(10)

async def consumer_handler(websocket, path):
    global send
    async for message in websocket:
        print(message)
        send.put(message)
    


async def producer_handler(websocket, path):
    global recv
    while True:
        while not recv.empty():
            d = str(recv.get())
            print("Got something")
            now = datetime.datetime.utcnow().isoformat() + "Z"
            await websocket.send(d)
        await asyncio.sleep(random.random())



async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()



########################################################################################################
def  HandleScriptStart(sim):
    global send
    global recv
    
    # Set the EXE to python instead of artemis
    if sim is not None:
        multiprocessing.set_executable(os.path.join(sys.exec_prefix, 'PyRuntime/python.exe'))
    # Create a shared message Queue
    #manager = multiprocessing.Manager()
    #passable_queue = manager.Queue()
    send = Queue()
    recv = Queue()

    print(os.path.join('./data/missions/pipex/lib/site-packages/websockets'))
    # spawn a child process running function sub
    # switch name on this side
    p = Process(target=child_logic, args=(send,recv,))
    p.start()
    send.put('{"msg":"start"}')
    print('started')

def  HandleScriptTick(sim, mission):
    global send
    global recv
    #start = time.perf_counter()
    while not recv.empty():
        d = recv.get()
        y = json.loads(d)
        print(d)
        if y['msg'] == 'create':
            e = mission.spawn_enemy(sim)
            send.put(f'{{"msg":"delete", "id" :{e.id}}}')
        elif y['msg'] == 'delete':
            print(f"delete {y['id']}")
            mission.remove_enemy(y['id'])
    # end = time.perf_counter()
    # # Only do this in Artemis
    # if sim is not None:
    #     print("Time consumed in tick: ",round(end - start, 5))

# This is just a test for running in python NOT artemis
if __name__ == '__main__':
    HandleScriptStart(None)



