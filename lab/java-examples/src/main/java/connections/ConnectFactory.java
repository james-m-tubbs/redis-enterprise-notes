package connections;

import redis.clients.jedis.Jedis;

public class ConnectFactory {

    String redis_host = "";
    int redis_port = ;
    String redis_password = "";


    Jedis jedis;
    public ConnectFactory() {
        jedis = new Jedis(redis_host, redis_port);
        jedis.auth(redis_password);
        System.out.println("Connected to Redis");
    }

    public Jedis getJedis() {
        return jedis;
    }
}
