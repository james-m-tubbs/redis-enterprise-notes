package pubsub;

import connections.ConnectFactory;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPubSub;

import java.util.ArrayList;

public class PubSub {
    private static ArrayList<String> messageContainer = new ArrayList<String>();

    public static void main(String[] args) throws Exception {
        ConnectFactory connectFactory = new ConnectFactory();
        Jedis jedis = connectFactory.getJedis();

        ArrayList<String> channels = new ArrayList<String>();
        channels.add("user_event:view");
        channels.add("process:terminate");

        System.out.println(jedis.pubsubChannels("*"));
        JedisPubSub pubSub = setupSubscriber();
        //jedis.subscribe(pubSub, "user_event:view");
        jedis.subscribe(pubSub, channels.toArray(new String[channels.size()]));
    }

    private static JedisPubSub setupSubscriber() {
        final JedisPubSub jedisPubSub = new JedisPubSub() {
            @Override
            public void onUnsubscribe(String channel, int subscribedChannels) {
                System.out.println("onUnsubscribe");
            }

            @Override
            public void onSubscribe(String channel, int subscribedChannels) {
                System.out.println("onSubscribe");
            }

            @Override
            public void onPUnsubscribe(String pattern, int subscribedChannels) {
            }

            @Override
            public void onPSubscribe(String pattern, int subscribedChannels) {
            }

            @Override
            public void onPMessage(String pattern, String channel, String message) {
            }

            @Override
            public void onMessage(String channel, String message) {
                messageContainer.add(message);
                System.out.println("Message received: " + message);
                if (message.contains("terminate")) {
                    System.exit(0);
                }
            }
        };
        return jedisPubSub;
    }
}
