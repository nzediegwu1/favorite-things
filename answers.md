#### How long did you spend on the coding test below? What would you add to your solution if you had more time?

1. I spent one month on the coding test and approximately 30 working hours in total. This was due to challenge combining it with my heavy responsibilities at work. I am strong with ReactJS and Flask, but had to quickly ramp up on Django and Vue.js for the test. Deployment also caused me a lot of troubles and time. Glad to have learnt!

2. If I had more time, I would add the following features:
    - Implement recycle bin for deleted favourites/categories
    - Implement functionality to restore deleted favourites/categories from recycle bin
    - Implement pagination when retrieving favorites
    - Integrate elastic search in backend and refactor implemented functionality to search favourites by category correspondingly
    - Implement logging for keeping track of, and easier debugging of production issues when they occur
    - Implement Continuous Deployment using Circleci to automatically deploy github master branch to AWS

#### What was the most useful feature that was added to the latest version of your chosen language? Please include a snippet of code that shows how you've used it.
Answer: Python [asyncio](https://docs.python.org/3/library/asyncio.html) library for asynchronous processing in Python 3.7
```
    import asyncio
    import time


    async def say_after(delay, what):
        await asyncio.sleep(delay)
        return what


    async def main():
        print(f"started at {time.strftime('%X')}")

        # Wait until the three tasks are completed
        # Should take around 2 seconds instead of 6 seconds for the three calls
        [task1, task2, task3] = await asyncio.gather(
            say_after(2, 'hello'), say_after(2, 'world'), say_after(2, 'anaeze'))

        print(task1, task2, task3)
        
        print(f"finished at {time.strftime('%X')}")


    asyncio.run(main())

```

#### How would you track down a performance issue in production? Have you ever had to do this?
1. How would you track down a performance issue in production?
    - Implement logging for keeping track of, and easier debugging of production issues when they occur
    - Define complex user behavior with multiple steps and transactions, loops, conditionals and custom code, using load testing tools like [Locust](https://locust.io/) (python) and [Artilery](https://artillery.io/) (nodejs)
    - Swarm the system with millions of simultaneous requests, to replicate production user behaviour.
    - Use the statistical result presented (times/latency percentiles, requests per second, concurrency, throughput, etc) to track down performance of individual endpoints tested
    - Use assertions and expectations on the responses to track custom application-specific metrics using javascript/python code
2. Have you ever had to do this?
    - Partially. I used [winston](https://www.npmjs.com/package/winston) to log http requests, events and exceptions/errors that happen in production
    - I then implemented a JSON endpoint: `GET /logs` for retrieval of logs for futher analysis and debugging of production issues