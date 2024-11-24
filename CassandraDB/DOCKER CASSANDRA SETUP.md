**SETUP APACHE CASSANDRA ON MAC USING DOCKER**

You first need to Install Docker on your Mac. Follow these steps from the terminal

### **Step 1: Verify Docker Installation**

Make sure Docker is installed and running on your machine. Verify by running:

bash  
Copy code  
`docker --version`

---

### **Step 2: Pull Cassandra Docker Image**

If the Cassandra image is not already downloaded, pull it from Docker Hub:

bash  
Copy code  
`docker pull cassandra:latest`

---

### **Step 3: Start Cassandra Container**

Run a new container with the Cassandra image:

bash  
Copy code  
`docker run --name my-cassandra -d cassandra:latest`

* `--name my-cassandra`: Assigns a name to the container for easier reference.  
* `-d`: Runs the container in detached mode (in the background).  
  ---

  ### **Step 4: Check Running Containers**

Verify that the Cassandra container is running:

bash  
Copy code  
`docker ps`

You should see `my-cassandra` in the list of running containers.

---

### **Step 5: Connect to Cassandra**

To interact with Cassandra, use the `cqlsh` (Cassandra Query Language Shell). Connect to the container:

bash  
Copy code  
`docker exec -it my-cassandra cqlsh`

This opens the Cassandra shell for database operations.

You can now connect from your python code this way:

 cluster \= Cluster(\["127.0.0.1"\])

 session \= cluster.connect()

