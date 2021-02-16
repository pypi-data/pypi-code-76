import tensorflow as tf
from face_recog.net import get_resnet


#images = tf.placeholder(name='img_inputs', shape=[None, 112, 112, 3], dtype=tf.float32)
#dropout_rate = tf.placeholder(name='dropout_rate', dtype=tf.float32)
w_init_method = tf.contrib.layers.xavier_initializer(uniform=False)

image_height, image_width = 112, 112
input_string = tf.placeholder(tf.string, shape=[None], name='string_input')
decode = lambda raw_byte_str: tf.image.resize_images(
                                        tf.cast(
                                            tf.image.decode_jpeg(raw_byte_str, channels=3, name='decoded_image'),
                                                tf.uint8), 
                                        [image_height, image_width])
input_images = tf.map_fn(decode, input_string, dtype=tf.float32) - 127.5
input_images = input_images / 127.5

net = get_resnet(input_images, 50, type='ir', w_init=w_init_method, trainable=False)
embedding_tensor = net.outputs

saver = tf.train.Saver()
session = tf.Session()
saver.restore(session, "/home/model/facerecog/ckpt_model_d/InsightFace_iter_best_710000.ckpt")
print ("===============")


############  serving model procedure #################
builder = tf.saved_model.builder.SavedModelBuilder('/home/model/facerecog/ckpt_model_d/serving2/')

# Create aliase tensors
# tensor_info_x: for input tensor
# tensor_info_y: for output tensor
tensor_info_x = tf.saved_model.utils.build_tensor_info(input_string)
tensor_info_y = tf.saved_model.utils.build_tensor_info(embedding_tensor)

# create prediction signature
prediction_signature = tf.saved_model.signature_def_utils.build_signature_def(
        inputs={'input': tensor_info_x},
        outputs={'output': tensor_info_y},
        method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME)

# build frozen graph
legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')
builder.add_meta_graph_and_variables(
    session, [tf.saved_model.tag_constants.SERVING],
    signature_def_map={
        'serving_default':
        prediction_signature
    },
    legacy_init_op=legacy_init_op)
builder.save()
