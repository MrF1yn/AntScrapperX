
### 1. **API Layer**
   - **Publicly Exposed API & Load Balancing (1, 2)**
     - API for starting/stopping/pausing services (`/admin/start-service`, `/admin/stop-service`, `/admin/pause-service`)
     - User API endpoints (`/scrapper-service/fetchOne`, `/scrapper-service/fetchAll`)
     - API key validation for both user and admin

### 2. **Data Handling**
   - **Redis for Queueing & Bloom Filtering (5)**
     - Handles incoming data and manages deduplication
   - **S3 for Storage (7, 8, 10)**
     - Uploading and responding with results

### 3. **Processing Layer (Needs Modification)**
   - **Driver Script (6)**
     - Manages the queue and sends commands to the scraper
   - **Worker Nodes (Node Pool - Scrappers & Selenium)**
     - Different node pools for API bots and Selenium instances

### 4. **Kubernetes Cluster on DigitalOcean (a5, a6) (Needs Modification)**
   - Automated via commit
   - Commands to start, pause, and stop the Kubernetes cluster

### 6. **Database Integration**
   - **Supabase (PostgreSQL)**
     - For potential data processing and analytics

### Two-Week Plan

**Week 1:**
1. **API Layer**
   - Develop API endpoints for user and admin functionalities.
   - Implement API key validation for users and admins.
   - Might need to setup domain using Cloudflare with anti-DDoS protection and anti-bot protection.

2. **Data Handling**
   - Set up Redis instance for queueing and Bloom filtering.
   - Integrate S3 for uploading results.

3. **Digital Ocean Kubernetes Modification**
   - Configure node pools for scrapers and Selenium instances.
   - 
4. **Processing Layer**
   - Develop the driver script for queue management.
   - Containerize worker scripts and Selenium instances.
   - Deploy to EKS cluster with proper scaling policies.
   
**Week 2:**
1. **Testing & Integration**
   - Conduct end-to-end testing.
   - Prepare documentation for deployment and usage.

