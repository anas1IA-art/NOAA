// File: src/noaa_day/MeteoMapDay.java
package noaa_day;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;

public class MeteoMap_dayTest extends Mapper<LongWritable, Text, Text, IntWritable> {
    private Text dayKey = new Text();
    private IntWritable temperature = new IntWritable();

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        try {
            // Extract year, month, and day
            String year = line.substring(15, 19);
            String month = line.substring(19, 21);
            String day = line.substring(21, 23);
            int tempValue = Integer.parseInt(line.substring(87, 93).trim());

            if (tempValue != 9999) { // Filter invalid values
                // Create key as YYYY-MM-DD
                dayKey.set(year + "-" + month + "-" + day);
                temperature.set(tempValue/100);
                context.write(dayKey, temperature);
            }
        } catch (Exception e) {
            System.err.println("Error parsing line: " + line);
            context.getCounter("MeteoMap_dayTest", "ParseErrors").increment(1);
        }
    }
}