package helloredis;

import connections.ConnectFactory;
import redis.clients.jedis.Jedis;

public class HelloRedis {

    public static void main(String[] args) throws Exception {
        ConnectFactory connectFactory = new ConnectFactory();
        Jedis jedis = connectFactory.getJedis();
        System.out.println("Message: " + jedis.get("hello_world_msg"));
        System.out.println("Count: " + jedis.incr("hello_worldcnt"));
    }
}
