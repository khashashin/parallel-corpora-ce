import tensorflow as tf

class TranslateModel:
    def __init__(self):
        self.model = tf.hub.load("tensorflow/t5", "model", version="0.5.1")

    def train(self):
        # Prepare the dataset
        dataset = tf.data.TextLineDataset(["data_ce_ru.txt"])
        dataset = dataset.map(lambda x: ({"inputs": x}, {"targets": x}))
        dataset = dataset.shuffle(1024).batch(32).prefetch(tf.data.AUTOTUNE)

        # Fine-tune the model on the dataset
        self.model.fine_tune(dataset, steps_per_epoch=1000, save_best_model_at="translate_chechen_to_russian")

if __name__ == "__main__":
    model = TranslateModel()
    model.train()
