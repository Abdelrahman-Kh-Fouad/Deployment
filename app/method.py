from tensorflow import keras
import tensorflow as tf
import numpy as np

def build_test_tfrecord(img,test_tfrecord):  # Generate TFRecord of test set
    with tf.io.TFRecordWriter(test_tfrecord)as writer:
            image = open(img, 'rb').read()

            feature = {
                'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image])),
            }

            example = tf.train.Example(features=tf.train.Features(feature=feature))
            writer.write(example.SerializeToString())

def _parse_example(example_string):
    feature_description = {
        'image': tf.io.FixedLenFeature([], tf.string),
    }

    feature_dict = tf.io.parse_single_example(example_string, feature_description)
    feature_dict['image'] = tf.io.decode_png(feature_dict['image'], channels=3)
    feature_dict['image'] = tf.image.resize(feature_dict['image'], [224, 224]) / 255.0
    return feature_dict['image']

def get_test_dataset(test_tfrecord):
    raw_test_dataset = tf.data.TFRecordDataset(test_tfrecord)
    test_dataset = raw_test_dataset.map(_parse_example)

    return test_dataset


def data_Preprocessing(test_dataset):

    test_dataset = test_dataset.batch(32)
    test_dataset = test_dataset.prefetch(tf.data.experimental.AUTOTUNE)

    return test_dataset

img_size = 224
learning_rate = 0.0001
def InceptionResNetV2_model():
    incp_res_v2 = tf.keras.applications.InceptionResNetV2(weights='imagenet',include_top=False, input_shape=[img_size,img_size,3])
    incp_res_v2.trainable= True
    model = tf.keras.Sequential([
        incp_res_v2,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(8, activation='softmax')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss=tf.keras.losses.sparse_categorical_crossentropy,
        metrics=[tf.keras.metrics.sparse_categorical_accuracy]
    )

    return model

def test(test_dataset , mod ):
    
    predIdxs = mod.predict(test_dataset)
    predIdxs = np.argmax(predIdxs, axis=1)
    return predIdxs

def simulation(img_path ,mod ):
    test_tfrecord = 'test.tfrecords'
    build_test_tfrecord(img_path, test_tfrecord)
    test_dataset = get_test_dataset(test_tfrecord)
    test_dataset = data_Preprocessing(test_dataset) 
    return test(test_dataset ,mod ) 


     
