import tensorflow as tf

def vectorize(dir,filename):
    # Load image data
    image_data = tf.io.read_file(f'./{dir}/{filename}')
    image_tensor = tf.image.decode_jpeg(image_data, channels=3)
    # Resize image
    image_tensor = tf.image.resize(image_tensor, [224, 224])
    # Preprocess image for MobileNet
    image_tensor = tf.keras.applications.mobilenet_v2.preprocess_input(image_tensor)
    # Load MobileNet model
    mobilenet_model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    # Extract features from image
    features = mobilenet_model.predict(tf.expand_dims(image_tensor, axis=0))
    # Use global average pooling to reduce spatial dimensions of features
    pooled_features = tf.keras.layers.GlobalAveragePooling2D()(features)
    vectorized_image = pooled_features.numpy().tolist()[0]
    print(len(vectorized_image))
    return vectorized_image

