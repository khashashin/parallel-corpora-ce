FROM tensorflow/tensorflow:latest-gpu-py3

# Install additional packages
RUN pip install tensorflow_datasets

# Copy the train.py script and the data_ce_ru.txt file to the container
COPY train.py /app/
COPY data_ce_ru.txt /app/

# Set the working directory
WORKDIR /app

# Run the training script
CMD ["python", "train.py"]
