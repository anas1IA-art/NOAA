package noaa_month;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;

public class MeteoMap_monthTest extends Mapper<Object, Text, Text, IntWritable> {
    private Text monthKey = new Text();
    private IntWritable temperature = new IntWritable();

    @Override
    protected void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();

        try {
            // Extract year, month, and day from fixed positions
            String year = line.substring(15, 19);
            String month = line.substring(19, 21);
            String day = line.substring(21, 23);
            int tempValue = Integer.parseInt(line.substring(87, 93).trim());

            if (tempValue != 9999) { // Filter invalid values
                // Format key as YYYY-MM for monthly averages
                monthKey.set(year + "-" + month); // Changed to group by month
                temperature.set(tempValue/100);
                
                context.write(monthKey, temperature);
            }
        } catch (Exception e) {
            System.err.println("Error parsing line: " + line);
            context.getCounter("MeteoMap", "ParseErrors").increment(1);
        }
    }
}
