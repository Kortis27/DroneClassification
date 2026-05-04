from ultralytics import YOLO

import os
from ultralytics import YOLO
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, recall_score, precision_score
import matplotlib.pyplot as plt
import numpy as np

def validate_model(
    labels_dir,
    model_path
):
    true_y = []
    pred_y = []
    for subdir in os.listdir(labels_dir):
        a, b = eval_dir(labels_dir + r'/' + subdir, model_path)
        true_y.extend(a)
        pred_y.extend(b)
    
    print(np.array(true_y).shape, np.array(pred_y).shape)
    cm = confusion_matrix(true_y, pred_y, labels=['burden', 'no_burden'])
    print(f'''
        Recall:\t{recall_score(true_y, pred_y, average=None, labels=['no_burden', 'burden'])}\t
        Precision:\t{precision_score(true_y, pred_y, average=None, labels=['no_burden', 'burden'])}
        Accuracy:\t{accuracy_score(true_y, pred_y)}
        ''')

    # Display with class names
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=['burden', 'no_burden']
    )

    disp.plot()
    plt.show()



def eval_dir(image_dir, model_path):
    model = YOLO(model_path)

    # Ground-truth label = directory name
    true_label = os.path.basename(os.path.normpath(image_dir))

    image_files = [
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    correct = 0
    total = 0
    pred_y = []
    true_y = [true_label for i in range(len(image_files))]

    for img_name in image_files:
        img_path = os.path.join(image_dir, img_name)

        results = model(img_path, verbose=False)[0]

        # Top-1 prediction
        probs = results.probs
        pred_class_id = int(probs.top1)
        
        # Map class index -> label string
        pred_label = model.names[pred_class_id]

        pred_y.append(pred_label)
        correct += 1 if pred_label == true_label else 0
        total += 1

    accuracy = correct / total if total > 0 else 0
    print(f"{true_label}:{accuracy}")
    return true_y, pred_y

weights = r"models\16_elm_84_rendered.pt"
dir = r"E:\Documents\AICapstoneData\elm_validation"

validate_model(dir, weights)