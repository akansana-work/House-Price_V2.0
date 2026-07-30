# AWS Deployment Guide (Student Version)

This guide provides step-by-step instructions for deploying the **House Price Prediction** Machine Learning Flask application to a free-tier Amazon Web Services (AWS) EC2 instance.

## Step 1: Launch an EC2 Instance
1. Log in to your [AWS Management Console](https://aws.amazon.com/console/).
2. Search for **EC2** in the search bar and go to the EC2 Dashboard.
3. Click the **Launch instance** button.
4. **Name:** Give your instance a name (e.g., `House-Price-App`).
5. **OS Images (AMI):** Select **Ubuntu** (the default "Ubuntu Server 24.04 LTS" or similar is fine). Make sure it says *Free tier eligible*.
6. **Instance Type:** Keep it as **t2.micro** (or `t3.micro`), which is *Free tier eligible*.
7. **Key Pair:** 
   - Click **Create new key pair**.
   - Name it (e.g., `house-app-key`).
   - Choose **RSA** and **.pem** format.
   - Click **Create key pair**. (A file will download to your computer. Keep it safe!)
8. **Network Settings:**
   - Check **Allow SSH traffic from Anywhere** (Port 22).
   - Check **Allow HTTP traffic from the internet** (Port 80).
   - *Note: We will open Port 8000 later.*
9. Click **Launch instance** on the right panel.

## Step 2: Open Port 8000 for Gunicorn
By default, we will run Gunicorn on port 8000. We need to tell the AWS firewall to allow traffic on this port.
1. Go to your EC2 Instances list and click on your new instance.
2. At the bottom, select the **Security** tab and click on the **Security group** link (it will look like `sg-0abcd1234...`).
3. Click **Edit inbound rules**.
4. Click **Add rule**.
5. Set the following:
   - **Type:** Custom TCP
   - **Port range:** 8000
   - **Source:** Anywhere-IPv4 (`0.0.0.0/0`)
6. Click **Save rules**.

## Step 3: Connect to Your EC2 Server
1. Open your computer's terminal (Command Prompt on Windows, Terminal on Mac/Linux).
2. Navigate to the folder where you downloaded your `.pem` key file in Step 1.
3. Fix permissions on the key (Mac/Linux only):
   ```bash
   chmod 400 house-app-key.pem
   ```
4. SSH into the server (replace the IP with your EC2's "Public IPv4 address"):
   ```bash
   ssh -i "house-app-key.pem" ubuntu@<YOUR-EC2-PUBLIC-IP>
   ```
   *Type `yes` when prompted if you want to continue connecting.*

## Step 4: Prepare the Server
Run these commands one by one to update the server and install Python:
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
```

## Step 5: Download the Project
Clone your repository onto the server:
```bash
git clone https://github.com/KalyanMurapaka45/House-Price-Prediction.git
cd House-Price-Prediction
```
*(If your code is in a different repository, replace the link above with yours).*

## Step 6: Set up the Python Environment
Create an isolated virtual environment and install the required libraries:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 7: Run the Application
Start the Flask app using Gunicorn so it listens to public traffic:
```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

## Step 8: View Your Live App!
Open your web browser and go to:
```
http://<YOUR-EC2-PUBLIC-IP>:8000
```
You should now see the House Price Prediction web interface!

## Optional: Keep it Running After Closing the Terminal
If you use the command in Step 7, the app will shut down as soon as you close your SSH terminal. To keep it running in the background forever:

1. Press `Ctrl + C` to stop the current Gunicorn server.
2. Run this command instead:
   ```bash
   nohup gunicorn --bind 0.0.0.0:8000 app:app &
   ```
3. You can now safely close your terminal, and the app will remain online! To stop it in the future, use `pkill gunicorn`.
