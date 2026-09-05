# **5. Where is the data stored? — Storage Topic**

For AWS interviews, don't think of storage as only **RDS**. AWS storage is mainly divided by **what kind of data you are storing and how you need to access it**.

---

# **1. What are the main AWS storage services?**

**Interview answer:**

> “AWS provides different storage services depending on the data and access requirements. I would use S3 for object storage, EBS for block storage attached to EC2, EFS for shared file storage, and database services such as RDS or DynamoDB when the data needs database capabilities.”

### Easy memory

`Files/Objects → S3`
`EC2 disk → EBS`
`Shared filesystem → EFS`
`Relational data → RDS`
`NoSQL data → DynamoDB`

---

# **2. What is S3?**

**Interview answer:**

> “Amazon S3 is a highly durable object storage service used to store objects such as images, videos, documents, backups, logs, and static website files. It is not a traditional filesystem or relational database.”

**Flow:** `Application → S3 → Object`

### Real-world example

`E-commerce application → S3 → Product images`

`Application → S3 → User documents`

`Backup → S3`

---

# **3. When do we use S3?**

**Interview answer:**

> “I use S3 when the application needs object storage rather than a filesystem or relational database. Typical use cases are images, videos, documents, backups, static assets, data lakes, and log archives.”

---

# **4. Why do we use S3 instead of storing files on EC2?**

**Interview answer:**

> “I prefer S3 for application files because it provides highly durable object storage and separates file storage from compute. If an EC2 instance is replaced or scaled out, the files remain available independently of that instance.”

This is especially important for horizontally scaled applications.

**Flow:** `EC2-1 → S3 ← EC2-2`

Both servers can access the same objects.

---

# **5. What is EBS?**

**Interview answer:**

> “Amazon EBS is block storage designed to be used with EC2 instances. It behaves like a disk volume where the operating system, application files, or database data can be stored.”

**Flow:** `EC2 → EBS Volume`

Think:

> **EBS = hard disk for EC2**

---

# **6. When do we use EBS?**

**Interview answer:**

> “I use EBS when an EC2 instance needs persistent block-level storage, such as an operating-system volume, application data, or workloads that require a disk-like filesystem.”

Example:

`EC2 → EBS → /data`

---

# **7. What happens to EBS when an EC2 instance is terminated?**

**Interview answer:**

> “It depends on the volume's DeleteOnTermination setting. A root EBS volume is commonly configured to be deleted when the instance is terminated, while a separate data volume can be configured to remain so that the data can be preserved.”

This is a good practical interview point.

---

# **8. What is EFS?**

**Interview answer:**

> “Amazon EFS is a managed shared file system that can be mounted by multiple compute instances. It is useful when multiple EC2 instances or workloads need to access the same files concurrently.”

**Flow:** `EC2-1 ↘`
`EC2-2 → EFS`
`EC2-3 ↗`

---

# **9. When do we use EFS instead of EBS?**

**Interview answer:**

> “I use EBS when the storage is primarily associated with one EC2 instance and I need block storage. I use EFS when multiple instances need shared file-system access to the same data.”

### Easy memory

`EBS → One EC2's disk`

`EFS → Shared filesystem for multiple instances`

---

# **10. S3 vs EBS vs EFS**

| Service | Think               |
| ------- | ------------------- |
| **S3**  | Object storage      |
| **EBS** | Block/disk storage  |
| **EFS** | Shared file storage |

### Real-world examples

`Product images → S3`

`EC2 OS/application disk → EBS`

`Shared uploads between multiple EC2 servers → EFS`

---

# **11. What is RDS?**

**Interview answer:**

> “Amazon RDS is a managed relational database service. I use it when the application requires structured relational data, SQL queries, transactions, and relationships between tables.”

**Flow:** `Application → RDS`

Examples:

`Users`

`Orders`

`Payments`

`Products`

---

# **12. Why don't we use S3 for user and order data?**

**Interview answer:**

> “S3 is object storage and does not provide relational database capabilities such as SQL queries, transactions, joins, and relational constraints. For structured transactional application data, I would use a database such as RDS.”

This is a very important distinction.

---

# **13. What is DynamoDB?**

**Interview answer:**

> “DynamoDB is a fully managed NoSQL database designed for high scalability and low-latency access. I would use it when the application has a suitable key-value or document data model and requires high scalability without traditional relational database features.”

---

# **14. When do we use RDS vs DynamoDB?**

**Interview answer:**

> “I use RDS when the application needs relational data, SQL, transactions, and relationships between tables. I use DynamoDB when the data model is suitable for NoSQL and the application requires highly scalable, low-latency access.”

### Easy memory

`SQL + Relationships + Transactions → RDS`

`NoSQL + Massive scalable key-value/document access → DynamoDB`

---

# **15. What is ElastiCache?**

**Interview answer:**

> “Amazon ElastiCache provides in-memory caching using engines such as Redis and Memcached. I use it to store frequently accessed data temporarily so that the application can respond faster and reduce load on the database.”

**Flow:** `Application → ElastiCache → Cache Hit`

If the data isn't cached:

`Application → ElastiCache → Cache Miss → RDS → Store result in cache`

---

# **16. Why do we need caching?**

**Interview answer:**

> “Caching reduces repeated database queries, improves application response time, and helps the application handle higher traffic without putting the same level of load on the primary database.”

---

# **17. What storage would you use for an e-commerce application?**

**Interview answer:**

> “I would use RDS for relational application data such as users, products, orders, and transactions. I would use S3 for product images and documents, ElastiCache for frequently accessed data, and EBS or EFS only when the application has a requirement for block or shared file storage.”

**Architecture:**
`Application → RDS`
`Application → S3`
`Application → ElastiCache`

---

# **18. What happens if traffic increases and the application has multiple EC2 servers?**

Suppose:

`ALB → EC2-1 / EC2-2 / EC2-3`

If files are stored locally:

`EC2-1 → local disk`
`EC2-2 → different local disk`
`EC2-3 → different local disk`

Now a user may upload a file to EC2-1 and later request it through EC2-3. The file may not exist there.

So for shared application files:

**Flow:** `EC2-1 / EC2-2 / EC2-3 → S3`

This is why **external shared storage** is often preferred for scalable applications.

---

# **19. What storage should we use for static website content?**

**Interview answer:**

> “I would store the static website files such as HTML, CSS, JavaScript, and images in S3 and use CloudFront as the CDN for global delivery and caching.”

**Flow:** `User → CloudFront → S3`

---

# **20. What storage should we use for database backups?**

**Interview answer:**

> “I can use S3 for long-term object storage of backup files and archives. For managed database backups, RDS also provides its own automated backup and snapshot capabilities.”

---

# **21. What is the difference between storage and database?**

**Interview answer:**

> “Storage services such as S3, EBS, and EFS are primarily used to store files, objects, blocks, or filesystem data. Database services such as RDS and DynamoDB provide data management capabilities such as querying, indexing, transactions or NoSQL access patterns.”

---

# **22. How do you choose the storage service in an interview?**

Ask yourself:

> **What kind of data is it?**

`Image / Video / Document / Backup → S3`

> **Does EC2 need a disk?**

`Yes → EBS`

> **Do multiple servers need the same filesystem?**

`Yes → EFS`

> **Does the application need SQL and relationships?**

`Yes → RDS`

> **Does it need scalable NoSQL?**

`Yes → DynamoDB`

> **Is the same data requested again and again?**

`Yes → ElastiCache`

---

# **Your storage mental map**

**`Static files → S3 → CloudFront`**

**`EC2 disk → EBS`**

**`Shared filesystem → EFS`**

**`SQL / transactions → RDS`**

**`NoSQL / key-value → DynamoDB`**

**`Frequently accessed data → ElastiCache`**

The most important interview sentence is:

> **“I choose the storage service based on the type of data and access pattern. S3 is for objects, EBS for block storage, EFS for shared filesystems, RDS for relational data, DynamoDB for NoSQL data, and ElastiCache for frequently accessed data that benefits from in-memory caching.”**

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
