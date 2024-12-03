**Lab 1 Instructions**



1. Provision VM in preferred cloud environment
2. Login with:
	1. ssh azureuser@XX.xxx.xxx.xxx
    OR
	3. ssh ubuntu@xx.xxx.xxx.xxx
    
   cd to your <HOME_DIRECTORY>
 
3. Create [conda](https://saturncloud.io/blog/how-to-create-a-conda-environment-with-a-specific-python-version/) environment -> See conda [Installation guide](https://docs.anaconda.com/free/miniconda/)
```bash
conda create --name detector python=3.10
```
4. Activate the conda environment
```bash 
conda activate detector
```
5. Clone git repo:
```bash
git clone https://github.com/iportilla/deployments.git
```
6. cd to lab 1 directory:
   ```bash
	cd deployments\lab1
   ```
7. Install Google drive download tool:
   ```bash
   	pip install gdown
   ```
8. Download the TF frozen model:
   ```bash
   	gdown FILE_ID
   ```
9. Get TF frozen model:
   ```bash
	cp {[PATH]}/frozen_inference_graph.pb .
   ```
 10. Install dependencies:
```bash
pip install flask
pip install opencv-python
```
11. Install requirements.txt
```bash
pip install -r requirements.txt
```
12. Run flask app:
```bash
python app.py
```
13. In another shell window, Test object detector with:
```bash
curl -F "image=@./dog-human.jpg" -XPOST http://localhost:5000/detect_objects
```
14. Verified inference message:
    
```bash
{
  "detections": [
    {
      "box": [
        0.08475469052791595,
        0.13658037781715393,
        0.8857864737510681,
        0.8216303586959839
      ],
      "label": "\"/m/01g317\"",
      "score": 0.9996463060379028
    },
    {
      "box": [
        0.13790792226791382,
        0.10156621783971786,
        0.8754037618637085,
        0.5871166586875916
      ],
      "label": "\"/m/01g317\"",
      "score": 0.9947457313537598
    }
  ]
}
```


*Watch for conda environment name and/or FLASK port conflicts with other students lab work*
