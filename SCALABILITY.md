### logging at high load

If the number of requests becomes very high and the logging operation faces issues, there are several solutions, each with its own advantages and disadvantages.
The first solution is using FastAPI’s background task, which makes log sending asynchronous so it doesn’t slow down the system, but the drawback is that some logs may be lost.
Another solution is using a message broker, which creates a queue and sends requests through it, solving the problem but, it requires infrastructure and has its own complexity.
Another method is batching logs and sending them together, which reduces I/O operations. In this case, several logs are grouped together and sent at specific times in batches.

**In general, in production environments a combination of these methods is used. For example, before sending logs to ELK, buffers like Fluentd are used, where logs are first  asynchronously sent to buffer like fluentd or ...  in a desired format and then based on file size or a specific intervals, the buffer is flushed and data is sent in batches to the logging service such as ELK.**



### for multi instance issue

When multiple workers or multiple pods of current instances are going to run, the most important issue is the number of connections made to the database.
Postgres by default has 100 connections, and for each connection it creates a process. If the number of connections becomes high, it results in problems and slowness.
One method is managing the number of connections inside the instances themselves in the .env file, and another method at high level if needed, is using tools like **pgBouncer** so that our instances connect to the database through it for better connection management. 


### during campaign and high loads
During campaign execution or at any other time, the most important issue in a URL shortener service is that it has a high number of reads and a small number of writes. By adding a caching system such as Redis, we can increase system stability and reduce database hits.
Recent incoming requests can be stored in Redis with the short link as the key and the long link as the value.
Because the high number of read requests leads to updating the visit count of a specific link, Redis can be used to store view counts, and from time to time this cache can be flushed and saved to the database so that visit counts are stored.
Using rate limiting is also necessary so that users are not allowed more than a certain number of accesses based on their IP or other factors to prevent potential abuse. this also can be managed at high level by tools like **API Gateway** or **NGINX**.