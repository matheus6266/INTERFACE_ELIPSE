import asyncio
import websockets
import time
async def test():
    async with websockets.connect('ws://169.254.62.198:6124') as websocket:
        i=0
        while 1:
            await websocket.send("{}".format(i))
            response = await websocket.recv()
            print(response)
            i=i+1
            time.sleep(0.2)
 
asyncio.get_event_loop().run_until_complete(test())