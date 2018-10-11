Welcome to Redis Enterprise
===
Redis = remote dictionary server
source: https://github.com/antirez/redis
website: http://redis.io

probabalistic data structures (finding 1 record in a billion is tough, does a guess with standard error)
top growth amongst nosql dbs - a bunch of stuff about industry and why redis is great
big benefit of redis is speed speed speed, super fast. Up to 50mil concurent transactions with response time <1ms

why so fast?
- single threaded (no locks!)
- most commands are executed with O(1) complexity
- access to discrete elements within objects
- reduced bandwitdh/overhead
- highest throughput at lowest latency in high volume write scenarios
- least number of servers to provide 1mil writes/sec

Redis as an operational DBMS can support round trip of 100ms to end users (user -50ms-> apps -50ms-> redis) 
Spring can connect to redis for session management automagically
Find the architecture diagram where they basically ask you to redis everything

Some Code Examples
===

## Simple Cache
Problem:
- Multiple DB calls are not great for web responses
- SET key value pairs
- keys and values can be 512m which is a bit insane
- `SET userid:1 "8754"`
- `GET userid:1 -> "8754"`
- `EXPIRE userid:1 60` (expire in 60s from now)
- `DEL userid:1`

Eviction policy can delete records as default server policy

OR IN JAVA
- `jedis.set("userid:1","8754")`
- `jedis.get("userid:1")`
- `jedis.del("userid:1")`
- `jedis.expire("userid:1", 60)`

Ability to subscribe to certain keys, includes wildcards (so like `userid:*`?)

## User Session
- Maintain session state across multiple servers
- Multiple session vars
- High speed/low latency required

`HMSET (has multiset)`
`HMSET usersession:1 userid 8754 name dave ip 1.2.3.4:31 hits 1`

this creates a hash with key `usersession:1`
|key|value|
|---|---|
|userid|8754|
|name|dave|
|ip|1.2.3.4:31|
|hits|2|

`HMGET usersession:1 userid name ip hits` (creates hash for ya)
`HINCRBY usersession:1 hits 1` (instant incrememt of a value, super powerful!)
`HSET usersession:1 lastpage "home"`
`HGET usersession:1 lastpage`
`HDEL usersession:1 lastpage`

in java:
just create a hashmap, use hmset

## Managing Queues
Problem:
This went too fast

Can use LPUSH or RPUSH to add to a list
`LPUSH queue1 red`
`LPUSH queue1 green`
`LPUSH queue1 blue`
`RPUSH queue1 red`

RPOPLPUSH queue1 queue2 (push right record - in this case red - from queue1 to queue2)
ATOMIC OPERATION! this makes sure right pop happens before left push

## Real Time Recommendation Engine
Add values (articles) o sets (tags)
`SADD tag:1 article:3 article:1`
`SMEMBERS tag:1` (article:3 article:1)

## Sorted Sets for Leaderboards
`ZADD game:1 10 id:1`
`ZADD game:1 9 id:2`
`ZADD game:1 12 id:3`
`ZINCRBY game:1 2 id:3` (add 2 to id3)

Zsomething - get order incrementing, decrementing

## Pub/Sub
Publish and subscribe to specific keys (on a per client basis)

SUBSCRIBE weather:stockholm weather:madrid

If data is added that has either of these keys it will return to the client (how do consume this?)

But can redis do X?

Pipelining
===
Most redis commands are synchronous
Non-blocking commands
`BGSAVE`, `BGREWRITEAOF`
`UNLINK` (v4)

Client Blocking Commands
- `SUBSCRIBE`
- `BLPOP`, `BRPOP`, `BRPOPLPUSH`
- `MONITOR`
- `WAIT`

## Multiple COmmand Transactions
- `MULTI` to start transaction block
- `EXEC` to close transaction block
- `DISCARD` to abort transaction block

commands are queued until exec
all commands or no commands are applied
transactions can have errors
If errors happen transactions roll back

Conditional Execution/Optimistic Concurrency Control
WATCH to conditionally execute
UNWATCH to clear c
DISCARD to abort transaction block

example: doing a transfer, but checking if funds exist
start your transaction, watch for your debitkey
Order is:
- do a watch on a key
- multiexec
- do your transaction
- if the watch changed, abort txn

## Disk Based Persistence
- Redis serves from memory
- multiple persistence modes
-- snapshot (RDB): store a PIT copy every 30m, hourly, daily, tunable
-- Append-only-file (AOF): write to disk every second (fsync) OR on every write
-- provides durability of data across power loss

## Redis Enterprise Durability
Master + Replica(s)
Replica writes to disk

OR
Master + Replica(s)
Master writes to disk
a bit slower, but a bit safer

## Transactions Summary
Pipelines aren't transacitons but reduce roundtrips
-mostly- ACID
atomic
isolation

Redis Enterprise
===
Redis Enterprise Node 
- redis shards per enterprise node? 
- it clusters some functionality together + REST API & cluster mgmt
Redis Enterprise Cluster
- Acts like a router in front of multiple redis clusters
- shared nothing architecture
- fully compatible with open source commands

## Scalability & Rebalancing
- Database is sharded/scaled by cluster manager
- each chart runs it's own process

Tune keyspaces to remain on the same cluster