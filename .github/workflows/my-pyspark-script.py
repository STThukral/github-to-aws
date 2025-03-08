import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

# Initialize Spark and Glue Context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Read data from the Glue Data Catalog
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database = "my_glue_database",  # Glue Data Catalog database
    table_name = "csv_data_csv",   # The table discovered by the crawler
    transformation_ctx = "dynamic_frame"
)

# Convert DynamicFrame to DataFrame for PySpark operations (if needed)
data_frame = dynamic_frame.toDF()

# Perform transformations on the DataFrame
transformed_df = data_frame.filter(data_frame['Quantity'] > 10)

# Convert DataFrame back to DynamicFrame if needed
transformed_dynamic_frame = DynamicFrame.fromDF(transformed_df, glueContext, "transformed_dynamic_frame")

# Write the transformed data to S3 or any other target  # For parquet
glueContext.write_dynamic_frame.from_options(transformed_dynamic_frame, 
                                              connection_type="s3", 
                                              connection_options={"path": "s3://my-example-s3-bucket-2025-output/"}, 
                                              format="parquet")

# Write the transformed data to S3 or any other target  # For csv file wihout compression
glueContext.write_dynamic_frame.from_options(transformed_dynamic_frame, 
                                              connection_type="s3", 
                                              connection_options={"path": "s3://my-example-s3-bucket-2025-output/"}, 
                                              format="csv",  # Specify CSV as the output format
                                              format_options={"compression": "NONE"}  # Ensure no compression is applied)
                                             )