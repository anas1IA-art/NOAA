package noaa_year;



import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;

public class MeteoMapYear extends Mapper<Object, Text, Text, IntWritable> {
 private Text yearKey = new Text();
 private IntWritable temperature = new IntWritable();

 @Override
 protected void map(Object key, Text value, Context context) throws IOException, InterruptedException {
     String line = value.toString();

     try {
         // Extract just the year (positions 15-19)
         String year = line.substring(15, 19);
         int tempValue = Integer.parseInt(line.substring(87, 93).trim());

         if (tempValue != 9999) { // Filter invalid values
             // Use only year as key
             yearKey.set(year);
             temperature.set(tempValue/100);
             context.write(yearKey, temperature);
         }
     } catch (Exception e) {
         System.err.println("Error parsing line: " + line);
         context.getCounter("MeteoMap", "ParseErrors").increment(1);
     }
 }
}
