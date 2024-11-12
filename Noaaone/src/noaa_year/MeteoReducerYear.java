package noaa_year;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import java.io.IOException;

public class MeteoReducerYear extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable averageTemperature = new IntWritable();

    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context) 
            throws IOException, InterruptedException {
        long sum = 0; // Changed to long to prevent potential overflow
        int count = 0;

        // Calculate sum and count of temperatures for each year
        for (IntWritable temp : values) {
            sum += temp.get();
            count++;
        }

        if (count > 0) {
            int average = (int) (sum / count); // Cast back to int after division
            averageTemperature.set(average);
            context.write(key, averageTemperature);
        }
    }
}