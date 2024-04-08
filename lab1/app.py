from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2

'''
https://hub.docker.com/r/codait/max-object-detector
https://ml-exchange.org/models/max-object-detector/
https://www.ibm.com/topics/serverless
https://cloud.ibm.com/docs/codeengine?topic=codeengine-deploy-app&interface=ui

'''
app = Flask(__name__)

# Load the frozen inference graph
with tf.io.gfile.GFile('frozen_inference_graph.pb', 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())

# Load the label map
label_map = {}
with open('label_map.pbtxt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if 'name' in line:
            label = line.split(':')[-1].strip().replace("'", "")
        elif 'id' in line:
            label_id = int(line.split(':')[-1])
            label_map[label_id] = label

# Create a TensorFlow session and load the graph
tf.compat.v1.reset_default_graph()
sess = tf.compat.v1.Session()
tf.import_graph_def(graph_def, name='')
image_tensor = sess.graph.get_tensor_by_name('image_tensor:0')
detection_boxes = sess.graph.get_tensor_by_name('detection_boxes:0')
detection_scores = sess.graph.get_tensor_by_name('detection_scores:0')
detection_classes = sess.graph.get_tensor_by_name('detection_classes:0')
num_detections = sess.graph.get_tensor_by_name('num_detections:0')

@app.route('/detect_objects', methods=['POST'])
def detect_objects():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_np = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    image_expanded = np.expand_dims(image, axis=0)

    with sess.as_default():
        (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections],
                                                  feed_dict={image_tensor: image_expanded})

    # Mapping from Open Images Dataset identifiers to categories
    label_mapping = {
        "/m/01g317": "Person",
    # Add more mappings here
    }

    # Process detection results
    detections = []
    num = int(num[0])
    for i in range(num):
        class_id = int(classes[0][i])
        #label = label_map[class_id]
        label_id = label_map[class_id]
        label = label_mapping.get(label_id, label_id)  # Use the mapping to get the user-friendly label
        score = float(scores[0][i])
        box = [float(coord) for coord in boxes[0][i]]

        detection_info = {
            'label': label,
            'score': score,
            'box': box
        }
        detections.append(detection_info)

    return jsonify({'detections': detections})

if __name__ == '__main__':
    app.run(debug=True)
