# DemoTweeterMining

##Install package:
    pip install -r requirements.txt
## Mining data:
    python src/downloader.py
## Training data:
#### HF-IHU
    python src/training.py hfihu
#### Naive Bayes
    python src/training.py nb
#### Sentiment Analysis
    python src/training.py sa
## Testing
    python src/classifier.py
    (method: hfihu, nb, sa)
## Evaluation metric
    python src/evaluate.py