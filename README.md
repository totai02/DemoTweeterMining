# DemoTweeterMining

##Install package:
    pip install -r requirements.txt
## Mining data:
    python src/downloader.py
## Training data:
### HF-IHU
    python src/trainning.py hfihu
### Naive Bayes
    python src/trainning.py nb
### Sentiment Analysis
    python src/trainning.py sa
## Testing
    python src/classifier.py
    (method: hfihu, nb, sa)