import aiohttp, asyncio, time

def callback(y):
    print(y.text())

async def get(url):
    async with aiohttp.ClientSession() as session:
        return await session.get(url)

          

async def request():
    url = 'https://zsys-test.zuoshouyisheng.com/pharm_api/soi_chat/collect?chat_id=5108&auth_code=5d591d929fc842efa1e181607dca4614&__fr__1607248082456=1&platform=web'
    return await get(url)
    # import json
    # print(json.loads(result)["status"])

_now = lambda : time.time()
start = _now()
for _ in range(4):
    tasks = [asyncio.ensure_future(request()) for _ in range(25)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print(_now()-start)
print("Noagh", _now()-start)