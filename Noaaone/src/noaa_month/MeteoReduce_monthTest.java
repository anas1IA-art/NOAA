

// MeteoReduce.java
package noaa_month;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import java.io.IOException;

public class MeteoReduce_monthTest extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable averageTemperature = new IntWritable();

    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context) 
            throws IOException, InterruptedException {
        int sum = 0;
        int count = 0;

        // Calculate sum and count of temperatures for each month
        for (IntWritable temp : values) {
            sum += temp.get();
            count++;
        }

        if (count > 0) {
            int average = sum / count;
            averageTemperature.set(average);
            context.write(key, averageTemperature);
        }
    }
}

