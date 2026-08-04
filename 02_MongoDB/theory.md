## What is motor, from motor.motor_asyncio import AsyncIOMotorClient, async, await, from bson import ObjectId ?

### Answer
1.) Motor:
- Motor is the official asynchronous Python driver for MongoDB.
- If you were writing a standard, non-async Python script, you would use a library called PyMongo. 
However, because FastAPI relies on asynchronous code to handle thousands of requests quickly, 
PyMongo won't work well because it blocks the server while waiting for the database. 
Motor wraps around PyMongo to make all database operations non-blocking.

2.) from motor.motor_asyncio import AsyncIOMotorClient:
- This is the code that actually connects your Python application to your MongoDB instance.
- What it does: AsyncIOMotorClient is the class used to create a database client object.

3.) async and await:
- async -> Placed before a function definition (async def) to tell Python, "This function is going 
to perform tasks that take time (like database queries), so run it asynchronously."
- await -> Placed inside an async function right before an operation that takes time. It tells 
Python, "Pause execution of this specific function right here until the database responds, but 
feel free to go handle other user requests in the meantime."

- Example:
When a user clicks a button on your website to fetch their profile, their specific request has to 
wait for the database. There is no escaping that network delay.
Without async/await, User 1's delay forces User 2, 3, and 4 to lag too, because the server refuses
to look at them until User 1 is totally finished.
With async/await, only User 1 waits for their data, while Users 2, 3, and 4 get served in less than
a millisecond because the server didn't get stuck standing in line with User 1.

4.) from bson import ObjectId
- MongoDB doesn't use simple integers (like 1, 2, 3) for its document IDs. Instead, it automatically 
generates a unique, 12-byte identifier called an ObjectId for the _id field of every document.
- What it does: Python treats things like "65c2f3b8e4b0a1b2c3d4e5f6" as a plain string. But MongoDB
won't recognize it as an ID if you look it up as a string. You use ObjectId to convert that
string into the special format MongoDB expects.

----------------------------------------------------------------------------------------------

- async and await are built in Python keywords, hence, you do not require any additional library
to install them.

## If they are built-in, why do we need libraries like FastAPI or Motor?
### Answer
[ Python Language ]  ---> Provides the core engine ('async' and 'await' syntax)
          │
          ├──> [ FastAPI ]  ---> Uses that engine to handle incoming web traffic
          │                      from your users without freezing.
          │
          └──> [ Motor ]    ---> Uses that engine to talk to MongoDB over the
                                 network without freezing.

## Do we need to use them EVERY TIME we interact with a database?
### Answer
Motor.
Whenever your code has to leave your computer and travel across a wire (the network) to talk to a 
database, it takes time. Even if it takes only 10 milliseconds, that is a lifetime to a computer. 
If you don't use await, your entire server freezes for those 10 milliseconds, and no other users 
can use your app during that window.

## Are there any exceptions where we skip async and await ?
### Answer
(i) You are using a traditional synchronous setup: If you were using an older framework like Flask 
paired with a traditional driver like PyMongo, you wouldn't use async/await at all because 
Flask handles users by opening completely separate threads rather than using an event loop.
(ii) Synchronous helper methods: Some database tools have quick methods that don't actually talk 
to the network. For example, creating a blank local query object or converting data formats. 
If it doesn't cross the network, it doesn't need await.

But for inserting, finding, updating, or deleting data in a FastAPI + Motor project? Yes, 
every single time.