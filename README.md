# PASS Auto-Scaling

An implementation of the Predictive Auto-Scaling System (PASS) for AWS. This project combines an offline machine learning model to learn historical traffic patterns with a lightweight, online AWS Lambda function to proactively scale AWS Auto Scaling Groups (ASG) before traffic spikes occur.

## Project Structure

* `offlineModel.py`: The offline ML model. It uses a Random Forest Regressor to analyze historical traffic data and generates a weekly lookup table of expected loads
which is stored in dynamoDB for lookups by PASS algorithm. 
* `PASS_lamda.py`: The online prediction and scaling logic. This AWS Lambda function runs periodically, queries the offline lookup table in DynamoDB, and adjusts the ASG capacity proactively while keeping a reactive Queuing Theory (M/M/s) fallback for unexpected QoS violations.

## Prerequisites

* **Python 3.x**
* **AWS Account** with an active Auto Scaling Group.
* **DynamoDB Table** named `ScalingLookupTable` with a partition key `Timeslot` (String).
* **Libraries:** `boto3`, `pandas`, `scikit-learn`
