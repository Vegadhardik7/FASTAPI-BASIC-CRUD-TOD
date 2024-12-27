import time
import asyncio
from fastapi import FastAPI

app = FastAPI()

# --------------------------------------------------------------------

"""
When we start the app using uvicorn it starts a thread, it is refered to as main thread.
All the endpoints defined as coroutines that is using `async def` that runs directly in
the event loop which runs in the main thread.
"""

# --------------------------------------------------------------------

@app.get("/1")
async def endpoint1():   # Processed Sequentially
    print("Hello")
    time.sleep(5)  # Blocking I/O bound operation
    # Function execution cannot be paused instead the event loop is blocked while waiting for the result.
    print("Bye")

"""
- Runs in the main thread
- Contains no non-blocking I/O bound operation, so it cannot be paused in the middle.
- Therefor the request are handled in sequential order.
- Print statements are called in order no matter howmany times you hit the API. This means 1st request is
completed then it move on to the second request.
- example:
Hello
Bye

Hello
Bye
"""

# --------------------------------------------------------------------

@app.get("/2")
async def endpoint2():  # Processed Concurrently
    print("Hello")
    await asyncio.sleep(5) # Non-Blocking I/O bound operation
    # that means it can be awaited i.e the function execution pauses while the operation is finish
    # in this pause the event loop can handle other tasks such as processing and requests
    print("Bye")

"""
- Runs in the main thread
- Contains non-blocking I/O bound operation, so it can be paused in the middle.
- Therefor the request are handled in concurrently order.
- Function execution can be stoped while event loop is waiting for its results.
- example:
Hello
Hello
Bye
Bye
"""
# --------------------------------------------------------------------

@app.get("/3")
def endpoint3():    # Processed Parallely 
    print("Hello")
    time.sleep(5)
    print("Bye")

"""
- Runs in the seperate thread
- So when we call the second endpoint twice, 2 seperate threads were used, this why we saw 
request handled parallely.
- Took too much time
- example:
Hello
Hello
Bye
Bye
"""


"""
BEST PRACTICES
1. Use async def for endpoint with non-blocking I/O operations.
2. Don't use async def for endpoint with blocking I/O operations.
3. Use normal function for endpoints with blocking I/O operations.
"""