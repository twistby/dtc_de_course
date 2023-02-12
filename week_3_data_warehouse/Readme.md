
  
## Data Talk Club Data Engeniering Zoomcamp week three

  

### Data Warehouse and BigQuery

  

**OLTP vs. OLAP**


| OLTP | OLAP |
|-------------------------------------------|---------------------------------------------------|
| Online transaction processing | Online analytical processing |
| Handles recent operational data | Handles all historical data |
| Size is smaller, typically 100 Mb - 10 Gb | Size is lager, typically 1 Tb - 100 Pb |
| Goals is to perform day-to-day operation | Goals is to make decisions from large data source |
| Uses simple queries | Uses complex queries |
| Faster processing speed | Slower processing speed |
| Requires read/write operations | Requires only read operations |
  
  

**BigQuery**

 
- Serverless data warehouse

	- there are no servers to manage or database software to install

- Software as well as infrastructure including

	- scalability and high-availability

- Built-in features like

	- machine learning

	- geospatial analysis

	- business intelligence

- BigQuery maximizes flexibility by separating the compute engine that analyzes your data from your storage

  
  
 
**Partitioned table**

A partitioned table is **divided into segments**, called partitions, that make it **easier to manage and query** your data. By dividing a large table into smaller partitions, you can **improve query performance** and control costs by reducing the number of bytes read by a query. You partition tables by specifying a partition column which is used to segment the table.

*Consider partitioning a table in the following scenarios:*
- You want to improve the query performance by only scanning a portion of a table.
- Your table operation exceeds a quota, and you can scope the table operations to specific partition column values.
- You want to determine query costs before a query runs. BigQuery provides query cost estimates before the query is run on a partitioned table. Calculate a query cost estimate by pruning a partitioned table, then issuing a query dry run to estimate query costs.


*Consider clustering a table instead of partitioning a table in the following circumstances:*
- You need more granularity than partitioning allows.
- Your queries commonly use filters or aggregation against multiple columns.
- The cardinality of the number of values in a column or group of columns is large.
- You do not need strict cost estimates before query execution.


**Clustered tables**

Clustered tables in BigQuery are tables that have a user-defined **column sort** order using clustered columns. Clustered tables can **improve query performance** and reduce query costs.

In BigQuery, a clustered column is a user-defined table property that sorts storage blocks based on the values in the clustered columns. The storage blocks are adaptively sized based on the size of the table. A clustered table maintains the sort properties in the context of each operation that modifies it. Queries that filter or aggregate by the clustered columns only scan the relevant blocks based on the clustered columns instead of the entire table or table partition. As a result, BigQuery might not be able to accurately estimate the bytes to be processed by the query or the query costs, but it attempts to reduce the total bytes at execution.

*You might consider clustering in the following scenarios:*

- Your queries commonly filter on particular columns. Clustering accelerates queries because the query only scans the blocks that match the filter.
- Your queries filter on columns that have many distinct values (high cardinality). Clustering accelerates these queries by providing BigQuery with detailed metadata for where to get input data.
- You do not need strict cost estimates before query execution.

*You might consider alternatives to clustering in the following circumstances:*
- You need a strict query cost estimate before you run a query. The cost of queries over clustered tables can only be determined after the query is run.
- Your query tables are smaller than 1 GB. Typically, clustering does not offer significant performance gains on tables less than 1 GB.

Because clustering addresses how a table is stored, it's generally a good first option for improving query performance.

**Combining clustered and partitioned tables**

You can combine table **clustering** **with** table **partitioning** to achieve finely-grained sorting for further query optimization.

In a partitioned table, data is stored in physical blocks, each of which holds one partition of data. Each partitioned table maintains various metadata about the sort properties across all operations that modify it. The metadata lets BigQuery more accurately estimate a query cost before the query is run. However, partitioning requires BigQuery to maintain more metadata than with an unpartitioned table. As the number of partitions increases, the amount of metadata to maintain increases.

### Documentation

https://cloud.google.com/bigquery/docs