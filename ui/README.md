# Working with the VIoLET UI

This project comes with an easy to use web based management tool for setting up and monitoring the deployment.

## Steps to access the UI

1. Sudo privilege is needed to start the UI server.
2. Clone this repository into the Admin VM if not done already.
3. Go to the ui directory within the project (this directory) and execute the following command in a shell,
    
    ```
    $ sudo sh start_ui.sh
    ```
4. Navigate to the public IP address of the Admin VM in your browser to access the web based management tool.

## Using the UI

The UI currently allows the deployment of D25 configuration. The ability to deploy other predefined or custom configurations will be added in the future.

1. Please ensure that the container VMs are configured as per the instructions and are up and running.
2. The UI currently has four major steps or tasks in the order listed below,
   1. Generating Infra. Config - This step uses the infra_gen.json to create the infra_config.json file 
   2. Partition - This step executes the gpmetis partitioning tool in the Admin VM and creates the metis_partitions file.
   3. Deploy - This step starts the docker containers in the VMs and sets up the infrastructure and sensors.
   4. Benchmark - This step runs micro benchmark in the containers and generates a report. Only CPU benchmarking is supported as of now.
3. The UI will guide you through all these steps with relevant information like json file view, console output and charts.
