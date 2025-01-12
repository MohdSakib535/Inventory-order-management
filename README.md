# RabbitMQ with Django and Celery

This project demonstrates the integration of RabbitMQ with Django and Celery for task queuing, background processing, and periodic task scheduling. It includes essential features like inventory management, order processing, and sending email notifications using Celery tasks.

## Features
- Inventory management with stock reduction on orders.
- Order processing with email notifications.
- Background task handling using Celery.
- Periodic task scheduling with Celery Beat (daily sales reports).
- Flower dashboard for monitoring Celery tasks.

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- Docker
- Docker Compose

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rabbitmqwithdjango
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Configure your `.env` file with necessary environment variables (e.g., email settings).

4. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

5. Apply migrations and create a superuser:
   ```bash
   docker exec -it django python manage.py migrate
   docker exec -it django python manage.py createsuperuser
   ```

## Services in Docker Compose
The `docker-compose.yml` file defines the following services:

### 1. **rabbitmq**
   - **Purpose**: Acts as a message broker to facilitate communication between services.
   - **Image**: `rabbitmq:3-management`
   - **Ports**:
     - `5672`: RabbitMQ messaging port for communication.
     - `15672`: RabbitMQ Management UI port for monitoring.
   - **Environment Variables**:
     - `RABBITMQ_DEFAULT_USER`: Default username (`guest`).
     - `RABBITMQ_DEFAULT_PASS`: Default password (`guest`).

### 2. **django**
   - **Purpose**: Hosts the Django web application.
   - **Build Context**: The Django application directory.
   - **Ports**:
     - `8000`: Exposes the Django development server.
   - **Volumes**:
     - `.`: Maps the current project directory to the container.
     - `./media`: Shared directory for uploaded media files.
   - **Environment Variables**:
     - `DJANGO_SETTINGS_MODULE`: Specifies Django settings module.
     - `CELERY_BROKER_URL`: URL for RabbitMQ broker.
     - `CELERY_RESULT_BACKEND`: Backend for Celery task results.

### 3. **celery-worker**
   - **Purpose**: Processes background tasks defined in Django.
   - **Build Context**: The Django application directory.
   - **Volumes**:
     - `.`: Maps the current project directory to the container.
     - `./media`: Shared directory for uploaded media files.
   - **Environment Variables**:
     - Same as the `django` service.

### 4. **flower**
   - **Purpose**: Provides a web-based monitoring tool for Celery tasks.
   - **Image**: `mher/flower:latest`
   - **Ports**:
     - `5555`: Exposes the Flower monitoring dashboard.
   - **Environment Variables**:
     - `CELERY_BROKER_URL`: URL for RabbitMQ broker.
     - `CELERY_RESULT_BACKEND`: Backend for Celery task results.

### 5. **celery-beat**
   - **Purpose**: Handles periodic task scheduling for Celery.
   - **Build Context**: The Django application directory.
   - **Volumes**:
     - `.`: Maps the current project directory to the container.
   - **Environment Variables**:
     - Same as the `django` service.

## How It Works
1. **Task Queuing**:
   - Tasks (e.g., sending emails, updating inventory) are queued by the Django app and sent to RabbitMQ.
   - RabbitMQ acts as a broker, ensuring the tasks are distributed to the appropriate Celery workers.

2. **Task Processing**:
   - Celery workers fetch tasks from RabbitMQ and execute them asynchronously.
   - This allows the Django app to handle user requests without waiting for long-running tasks to complete.

3. **Periodic Task Scheduling**:
   - Celery Beat schedules periodic tasks (e.g., sending daily sales reports) and dispatches them to RabbitMQ.

4. **Monitoring**:
   - The RabbitMQ Management UI provides insights into the message queue.
   - Flower displays the status of tasks, workers, and queues in real-time.

## Usage
1. Access the Django app at: [http://localhost:8000](http://localhost:8000)
2. Access the RabbitMQ Management UI at: [http://localhost:15672](http://localhost:15672)
3. Access the Flower dashboard at: [http://localhost:5555](http://localhost:5555)

## Celery Tasks
- **Send Order Confirmation**: Sends an email confirmation for placed orders.
- **Update Inventory**: Updates inventory stock after an order.
- **Daily Sales Report**: Sends a daily sales report to the admin (scheduled with Celery Beat).

## File Structure
```
├── orders
│   ├── migrations
│   ├── templates
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tasks.py
│   ├── views.py
├── rabbitmqwithDjango
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
```

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.

