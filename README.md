```
# 🚀 Flask App with Docker, Nginx & AWS EC2 Deployment

This guide walks through building, containerizing, and deploying a Flask app using Docker, Nginx, and AWS EC2. The project demonstrates best practices like using a reverse proxy, ECR for image hosting, and automation with shell scripts.

---

### 🧱 Project Structure

.
├── app.py  
├── requirements.txt  
├── Dockerfile  
├── nginx.conf  
├── start.sh (optional entrypoint script)

---

### ⚙️ 1. Local Development & Virtual Environment

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

---

### 🐳 2. Dockerize the App

#### Dockerfile

FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "app.py"]

#### Build and Run Locally

docker build -t flask-docker-app .
docker run -p 8080:8080 flask-docker-app

---

### 🌐 3. Set Up AWS

- Create an IAM user with ECR, EC2, and CloudWatch permissions.
- Configure AWS CLI:

aws configure
# Provide Access Key ID, Secret Access Key, region (e.g., eu-central-1), and output format

---

### 📦 4. Push Image to AWS ECR

#### Create Repo (or use AWS Console)

aws ecr create-repository --repository-name fadysapp

#### Authenticate Docker to ECR

aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.eu-central-1.amazonaws.com

#### Tag and Push

docker tag flask-docker-app:latest <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.eu-central-1.amazonaws.com/fadysapp:latest  
docker push <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.eu-central-1.amazonaws.com/fadysapp:latest

---

### 💻 5. Deploy on EC2

#### Launch EC2 Instance

- Use Ubuntu.  
- Add inbound rules for:
  - Port 22 (SSH)
  - Port 8080 (App)
  - Port 80 (Nginx)

#### SSH into the Instance

ssh -i your-key.pem ubuntu@<YOUR_EC2_PUBLIC_IP>

#### Install Docker

sudo apt update  
sudo apt install docker.io -y  
sudo usermod -aG docker ubuntu

#### Authenticate Docker on EC2

aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.eu-central-1.amazonaws.com

#### Pull & Run

docker pull <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.eu-central-1.amazonaws.com/fadysapp:latest  
docker run -d -p 8080:8080 <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.eu-central-1.amazonaws.com/fadysapp

---

### 🔁 6. Set Up Nginx (Reverse Proxy)

#### Install Nginx

sudo apt install nginx -y

#### Edit Config

sudo nano /etc/nginx/sites-available/default

Replace the location / block with:

location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

#### Restart Nginx

sudo systemctl restart nginx

---

### ✅ Test Your App

Visit http://<YOUR_EC2_PUBLIC_IP> — you should see your Flask app running!
```
