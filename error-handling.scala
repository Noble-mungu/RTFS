import org.apache.spark.sql.functions._

val safeUDF = udf((input: String) => {
  try {
    // Your UDF logic here, e.g., convert string to double
    input.toDouble
  } catch {
    case e: NumberFormatException => {
      // Log the error and return a default value (e.g., 0.0)
      println(s"Error converting string to double: $input")
      0.0
    }
    case other: Exception => {
      // Handle other unexpected exceptions
      println(s"Unexpected error in UDF: $input, Exception: ${other.getMessage}")
      // Consider returning a special value or skipping the row
      -1.0
    }
  }
})

// Apply safeUDF to your DataFrame
val transformedData = data.withColumn("outputColumn", safeUDF(col("inputColumn")))
