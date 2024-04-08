### As Docker Container

[See original post](https://hub.docker.com/r/codait/max-object-detector)

## Run Locally

1. [Build the Model](https://hub.docker.com/r/codait/max-object-detector#1-build-the-model)
2. [Deploy the Model](https://hub.docker.com/r/codait/max-object-detector#2-deploy-the-model)
3. [Use the Model](https://hub.docker.com/r/codait/max-object-detector#3-use-the-model)
4. [Run the Notebook](https://hub.docker.com/r/codait/max-object-detector#4-run-the-notebook)
5. [Development](https://hub.docker.com/r/codait/max-object-detector#5-development)
6. [Cleanup](https://hub.docker.com/r/codait/max-object-detector#6-cleanup)

### 1. Build the Model

Clone this repository locally. In a terminal, run the following command:

```bash
git clone https://github.com/IBM/MAX-Object-Detector.git
```

Change directory into the repository base folder:

```bash
cd MAX-Object-Detector
```

To build the docker image locally for Intel CPUs, run:

```bash
docker build -t max-object-detector .
```

To select a model, pass in the `--build-arg model=<desired-model>` switch:

```bash
docker build --build-arg model=faster_rcnn_resnet101 -t max-object-detector .
```

Currently we support two models, `ssd_mobilenet_v1` (default) and `faster_rcnn_resnet101`.

For ARM CPUs (eg Raspberry Pi), run:

```bash
docker build -f Dockerfile.arm32v7 -t max-object-detector .
```

All required model assets will be downloaded during the build process. _Note_ that currently this docker image is CPU only (we will add support for GPU images later).

### 2. Deploy the Model

To run the docker image, which automatically starts the model serving API, run:

```bash
docker run -it -p 5000:5000 max-object-detector
```

### 3. Use the Model

The API server automatically generates an interactive Swagger documentation page. Go to `http://localhost:5000` to load it. From there you can explore the API and also create test requests.

Use the `model/predict` endpoint to load a test image (you can use one of the test images from the `samples` folder) and get predicted labels for the image from the API. The coordinates of the bounding box are returned in the `detection_box` field, and contain the array of normalized coordinates (ranging from 0 to 1) in the form `[ymin, xmin, ymax, xmax]`.



You can also test it on the command line, for example:

```bash
curl -F "image=@samples/dog-human.jpg" -XPOST http://127.0.0.1:5000/model/predict
```

You should see a JSON response like that below:

```json
{
  "status": "ok",
  "predictions": [
      {
          "label_id": "1",
          "label": "person",
          "probability": 0.944034993648529,
          "detection_box": [
              0.1242099404335022,
              0.12507188320159912,
              0.8423267006874084,
              0.5974075794219971
          ]
      },
      {
          "label_id": "18",
          "label": "dog",
          "probability": 0.8645511865615845,
          "detection_box": [
              0.10447660088539124,
              0.17799153923988342,
              0.8422801494598389,
              0.732001781463623
          ]
      }
  ]
}
```

You can also control the probability threshold for what objects are returned using the `threshold` argument like below:

```bash
curl -F "image=@samples/dog-human.jpg" -XPOST http://127.0.0.1:5000/model/predict?threshold=0.5
```

The optional `threshold` parameter is the minimum `probability` value for predicted labels returned by the model. The default value for `threshold` is `0.7`.
