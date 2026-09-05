## **5. Where is the data stored?**

**What do we use for relational data?**: Amazon RDS.

**What is RDS?**: RDS is a managed relational database service used for databases such as MySQL, PostgreSQL, MariaDB, Oracle, and SQL Server.

**When do we use RDS?**: When the application needs structured relational data, SQL queries, relationships between tables, transactions, and database features.

**Examples**: User details, orders, payments, products, transactions.

**RDS architecture flow**: Application → RDS → Database.

**Why RDS instead of installing MySQL on EC2?**: RDS is managed by AWS, so AWS handles tasks such as infrastructure provisioning, backups, patching, and high-availability options.

---

### **S3**

**What do we use for files and objects?**: Amazon S3.

**What is S3?**: S3 is an object storage service used to store files such as images, videos, documents, backups, logs, and static website content.

**When do we use S3?**: When the application needs scalable object/file storage rather than relational database storage.

**Examples**: Product images, profile photos, PDFs, videos, application backups.

**S3 architecture flow**: Application → S3 → Objects.

**Why use S3 instead of storing files on EC2?**: S3 provides highly durable object storage and avoids depending on the local disk of an application server.

---

### **DynamoDB**

**What do we use for NoSQL data?**: DynamoDB.

**What is DynamoDB?**: DynamoDB is a managed NoSQL database designed for high-scale applications with fast and predictable performance.

**When do we use DynamoDB?**: When the application does not require a traditional relational database structure and needs highly scalable key-value or document storage.

**Examples**: User sessions, shopping-cart data, game data, high-volume application data.

**DynamoDB flow**: Application → DynamoDB → NoSQL data.

---

### **ElastiCache**

**What do we use for caching?**: ElastiCache.

**What is ElastiCache?**: ElastiCache is a managed in-memory caching service commonly used with Redis or Memcached.

**Why do we use caching?**: To store frequently accessed data in memory and reduce the number of requests going to the database.

**Example**: Frequently accessed product information can be stored in cache instead of querying RDS every time.

**Flow**: Application → ElastiCache → Cache hit → Response.

**Cache miss flow**: Application → ElastiCache → Cache miss → RDS → Store result in cache → Response.

---

### **RDS Multi-AZ**

**Why do we use Multi-AZ with RDS?**: To improve database availability and provide automatic failover in case the primary database instance becomes unavailable.

**Flow**: Application → RDS Primary → Failure → Standby → RDS automatically fails over.

---

### **Read Replica**

**What is a Read Replica?**: A read replica is a copy of a database used mainly to handle read traffic.

**Why do we use Read Replicas?**: To reduce the read load on the primary database and improve read scalability.

**Flow**: Application → Primary RDS for writes, Application → Read Replica for reads.

**Multi-AZ vs Read Replica**: Multi-AZ → High availability/failover, Read Replica → Read scalability.

---

## **How do you choose the storage?**

**Relational data**: RDS.

**Files/objects**: S3.

**NoSQL/key-value/document data**: DynamoDB.

**Frequently accessed temporary data**: ElastiCache.

**Static website files**: S3 + CloudFront.

---

## **Real-world e-commerce example**

**User/order/product database**: RDS.

**Product images**: S3.

**Frequently accessed product data**: ElastiCache.

**High-scale session/cart data when a NoSQL design fits**: DynamoDB.

**Static images/CSS/JavaScript delivery**: CloudFront + S3.

**Architecture flow**: User → CloudFront/WAF → ALB → Application → RDS/S3/ElastiCache/DynamoDB.

### **Most important interview memory**

**RDS**: Relational SQL data.

**S3**: Files and objects.

**DynamoDB**: NoSQL data.

**ElastiCache**: Fast in-memory cache.

**Multi-AZ**: High availability.

**Read Replica**: Read scaling.
