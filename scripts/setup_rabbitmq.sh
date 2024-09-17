#!/bin/bash

echo "Starting RabbitMQ setup..."

# RabbitMQ credentials and settings
RABBITMQ_HOST="rabbitmq"
RABBITMQ_USER="guest"
RABBITMQ_PASSWORD="guest"
EXCHANGE_NAME="taskiq"
QUEUE_NAME="taskiq"
ROUTING_KEY="#"
EXCHANGE_TYPE="topic"

# Wait for RabbitMQ to start up
echo "Waiting for RabbitMQ to start..."
sleep 10

# Delete the existing queue if it exists
echo "Deleting queue '$QUEUE_NAME' (if it exists)..."
rabbitmqadmin -H "$RABBITMQ_HOST" -u "$RABBITMQ_USER" -p "$RABBITMQ_PASSWORD" delete queue name="$QUEUE_NAME" || true
echo "Queue '$QUEUE_NAME' deleted (if existed)."

# Delete the existing exchange if it exists
echo "Deleting exchange '$EXCHANGE_NAME' (if it exists)..."
rabbitmqadmin -H "$RABBITMQ_HOST" -u "$RABBITMQ_USER" -p "$RABBITMQ_PASSWORD" delete exchange name="$EXCHANGE_NAME" || true
echo "Exchange '$EXCHANGE_NAME' deleted (if existed)."

# Declare exchange
echo "Declaring exchange '$EXCHANGE_NAME'..."
rabbitmqadmin -H "$RABBITMQ_HOST" -u "$RABBITMQ_USER" -p "$RABBITMQ_PASSWORD" declare exchange name="$EXCHANGE_NAME" type="$EXCHANGE_TYPE" durable=true
echo "Exchange '$EXCHANGE_NAME' declared."

# Wait for exchange declaration to be processed
echo "Waiting for exchange declaration to be processed..."
sleep 5

# Declare queue as durable
echo "Declaring queue '$QUEUE_NAME' as durable..."
rabbitmqadmin -H "$RABBITMQ_HOST" -u "$RABBITMQ_USER" -p "$RABBITMQ_PASSWORD" declare queue name="$QUEUE_NAME" durable=true
echo "Queue '$QUEUE_NAME' declared as durable."

# Bind queue to exchange
echo "Binding queue '$QUEUE_NAME' to exchange '$EXCHANGE_NAME' with routing key '$ROUTING_KEY'..."
rabbitmqadmin -H "$RABBITMQ_HOST" -u "$RABBITMQ_USER" -p "$RABBITMQ_PASSWORD" declare binding source="$EXCHANGE_NAME" destination_type="queue" destination="$QUEUE_NAME" routing_key="$ROUTING_KEY"
echo "Queue '$QUEUE_NAME' bound to exchange '$EXCHANGE_NAME' with routing key '$ROUTING_KEY'."
