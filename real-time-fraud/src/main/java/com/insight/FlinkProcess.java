package com.insight;

import java.util.Properties;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.functions.FilterFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple3;
// import org.apache.flink.streaming.api.functions.sink.SinkFunction;
import org.apache.flink.api.java.tuple.Tuple;
import org.apache.flink.api.java.tuple.Tuple1;
import org.apache.flink.api.java.tuple.Tuple4;




import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;
import org.apache.flink.streaming.util.serialization.SimpleStringSchema;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

/*Read the data stream from topic transactions-forward in Kafka, make predictions with logistic classification,
 * then write the data stream to PostgreSQL;
 * If the prediction is fraud, compress the data to string and write to Kafka topic transactions-backward. 
 * The user simulator will give the true label of the transaction and update the data in PostgreSQL
 * 
 * The input is the data streaming of String from Kafka
 */
public class FlinkProcess {

    // *************************************************************************
    // PROGRAM
    // *************************************************************************
    public static void main(String[] args) throws Exception {

        // **************************************************
        // Parameters of logistic regression
        // **************************************************
        double[] w30 = new double[]{

            -1.1289703378295965,
            1.721698472278388,
            -0.24255950063396547,
            0.24892234577791233,
            1.9141632896069147,
            1.6672821738741157,
            -0.6738153672233783,
            -2.0272543599508,
            -2.257822378857633,
            -1.400879228345609,
            -2.759592866465892,
            2.495743641290426,
            -2.164850087938599,
            -0.4068735755971469,
            -4.28959155425175,
            0.9730412736842141,
            -1.4524196767355433,
            -2.6469344450945895,
            -1.1325173729393654,
            2.021227229253037,
            -2.092856154918522,
            0.38622384737940774,
            1.3171863423202503,
            -1.2101073166098935,
            0.7334094830753759,
            -0.45936346537755374,
            1.300548268038039,
            -0.9858705269679775,
            0.8449109972953374,
            2.983890059595085,
        };
        double b = -11.04842724;

        // **************************************************
        // create execution environment
        // **************************************************
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // create properties for Kafka
        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", "rtfs-kafka-1:9093");
        properties.setProperty("group.id", "myGroup");

        // read 'topic' from Kafka producer: Kafka topic is "transactions-forward"
        FlinkKafkaConsumer<String> kafkaConsumer = new FlinkKafkaConsumer<>(
                "transactions-forward",
                new SimpleStringSchema(),
                properties
        );

        // convert kafka stream to data stream
        DataStream<String> rawInputStream = env.addSource(kafkaConsumer);

        // **************************************************
        // Transform: String -> String[]
        // **************************************************
        DataStream<String[]> transformStream = rawInputStream.map(new MapFunction<String, String[]>() {
            @Override
            public String[] map(String value) {
                String[] row = new String[38];
                String[] inputs = value.split(","); // 34 elements
                double weightedSum = 0;
                long timeProduced = Long.parseLong(inputs[33]);
                long timeProcessed = System.currentTimeMillis();
                int latency = (int) (timeProcessed - timeProduced);

                for (int i = 0; i <= 37; ++i) {
                    if (i <= 2) {
                        row[i] = inputs[i]; // key and index
                    } else if (i <= 32) { // 30 features, 3, 4, .. 32, get the x_i, calculate weightedSum, write x_i to row
                        double x_i = Double.parseDouble(inputs[i]);
                        weightedSum += x_i * w30[i - 3];
                        row[i] = inputs[i];
                    } else if (i == 33) {
                        row[i] = inputs[i];
                    } else if (i == 34) {
                        row[i] = String.valueOf(timeProcessed);
                    } else if (i == 35) {
                        row[i] = String.valueOf(latency);
                    } else if (i == 36) {
                        weightedSum += b;
                        row[i] = (weightedSum > 0) ? "yes" : "no"; // fraud or non-fraud
                    } else {
                        row[i] = "noreply"; // no reply from customers
                    }
                }
                return row;
            }
        });

        // **************************************************
        // Sink: non-fraud to PostgreSQL, fraud to "transactions-backward" in Kafka
        // **************************************************
        DataStream<String[]> nonFraudStream = transformStream.filter(new FilterFunction<String[]>() {
            @Override
            public boolean filter(String[] row) {
                return "no".equals(row[36]);
            }
        });

        DataStream<String[]> fraudStream = transformStream.filter(new FilterFunction<String[]>() {
            @Override
            public boolean filter(String[] row) {
                return "yes".equals(row[36]);
            }
        });

        DataStream<String> strFraudStream = fraudStream.map(new MapFunction<String[], String>() {
            @Override
            public String map(String[] row) {
                StringBuilder stringBuilder = new StringBuilder();
                for (int i = 0; i <= row.length - 2; i++) {
                    stringBuilder.append(row[i]);
                    stringBuilder.append(",");
                }
                stringBuilder.append(row[row.length - 1]);
                return stringBuilder.toString();
            }
        });

        // Send the fraud to Kafka
        FlinkKafkaProducer<String> myProducer = new FlinkKafkaProducer<>(
                "transactions-backward",
                new SimpleStringSchema(),
                properties
        );

        // Send the non-fraud to PostgreSQL
        nonFraudStream.addSink(new PostgreSQLSink());
        strFraudStream.addSink(myProducer);

        System.out.println("I am running");
        env.execute("Kafka to Flink to PostgreSQL Streaming");
    }

    // Implement PostgreSQLSink as a custom SinkFunction
    public static class PostgreSQLSink extends RichSinkFunction<String[]> {
        @Override
        public void invoke(String[] value, Context context) throws Exception {
            // Implement the logic to write data to PostgreSQL
            // For example, using JDBC:
            Connection connection = DriverManager.getConnection("jdbc:postgresql://postgres:5432/frauddetection", "postgres", "azbycx567");
            String sql = "INSERT INTO transactions (col1, col2, ...) VALUES (?, ?, ...)";
            PreparedStatement stmt = connection.prepareStatement(sql);
            // Set parameters and execute
            stmt.executeUpdate();
            connection.close();
        }
    }
}
