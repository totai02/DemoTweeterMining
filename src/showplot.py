import matplotlib.pyplot as plt
import json

hfihuFile = "hfihu_evaluate.json"
nbFile = "nb_evaluate.json"

if __name__ == '__main__':

    with open(nbFile, 'r') as f:
        precision = json.loads(f.readline())
        precision_x = [int(num) for num in precision.keys()]
        precision_y = [num*100 for num in precision.values()]

        precision_x = precision_x[:1] + precision_x[10:]
        precision_y = precision_y[:1] + precision_y[10:]

        plt.figure()

        plt.plot(precision_x, precision_y, label= "Precision", marker= "s")

        plt.ylim(0, 100)
        plt.xlabel('Number of Ranked Recommendations')
        plt.ylabel('Recall: %Ground Truth Hashtags Matched by\nRecommendations')

        plt.title("Precision")

        plt.legend()

        plt.figure(2)

        plt.plot(precision_x, precision_y, label="Precision", marker="s")

        plt.xlabel('Number of Ranked Recommendations')
        plt.ylabel('Recall: %Ground Truth Hashtags Matched by\nRecommendations')

        plt.title("Recall")

        plt.legend()

        plt.show()