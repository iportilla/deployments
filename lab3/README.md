## Deploy on Code Engine

[Original instructions](https://hub.docker.com/r/codait/max-object-detector#deploy-on-code-engine)

You can also deploy the model on IBM Cloud's Code Engine platform which is based on the Knative serverless framework. Once authenticated with your IBM Cloud account, run the commands below.

Create a Code Engine project, give it a unique name

```bash
ibmcloud ce project create --name sandbox
```

Run the container by pointing to the quay.io image and exposting port 5000.

```bash
ibmcloud ce application create --name max-object-detector --image quay.io/codait/max-object-detector --port 5000
```

Open the resulting URL in a browser, append /app to view the app instead of the API.
