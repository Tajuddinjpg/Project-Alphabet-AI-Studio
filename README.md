# Alphabet AI Studio

Draw a capital letter in the browser → a **from-scratch Artificial Neural Network** (NumPy) predicts A–Z and shows what happens inside it.

```
alphabet-ai-studio/
├── ann/                  ← the machine-learning code
│   ├── network.py        ← ANN: layers, ReLU, softmax, backprop, Adam, dropout
│   ├── training.py       ← training loop, early stopping, augmentation
│   ├── preprocessing.py  ← drawing → 28×28 (same recipe as EMNIST)  ★ key to correct answers
│   └── data.py           ← EMNIST loader + offline synthetic fallback
├── scripts/
│   ├── train.py          ← train + evaluate + save the model
│   ├── plots.py          ← graphs
│   └── make_report.py    ← builds docs/ANN_Lab_Report.docx from real results
├── webapp/               ← the website
│   ├── app.py            ← Flask API (/api/predict, /api/meta, /api/health)
│   ├── templates/index.html
│   └── static/{css,js}/
├── model/                ← trained weights + metrics (created by train.py)
├── data/                 ← EMNIST download goes here
├── tests/                ← unit tests (gradient check, preprocessing, API)
├── docs/                 ← report + figures
├── run.py                ← start the website
└── requirements.txt
```

## Run (Windows / VS Code)
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python run.py                 # open http://127.0.0.1:5000
```
The folder already contains a trained model in `model/`, so the site works immediately.

### ⚠ Train on the REAL handwriting dataset (recommended, do this once)
The bundled model was trained on font-based synthetic data because the dataset could not be downloaded in the build environment. For best accuracy on real handwriting run:
```powershell
python scripts/train.py --data emnist      # downloads EMNIST (~560 MB) then trains, ~10-15 min on CPU
python scripts/make_report.py              # optional: regenerate the lab report with your real numbers
python run.py
```
If the automatic download fails, download `gzip.zip` from the [NIST EMNIST page](https://www.nist.gov/itl/products-and-services/emnist-dataset) and save it as `data/emnist_gzip.zip`.

## Why the old project predicted wrong letters
| Problem | Fix |
|---|---|
| Logistic Regression = one **linear** layer, not an ANN | Multi-layer ANN (784→256→128→26) with ReLU + softmax |
| `StandardScaler` blew up empty border pixels of drawings | Plain 0–1 pixel scaling |
| Drawing was only shrunk, not centred like training images | `ann/preprocessing.py` crops, resizes to 20 px, centres by centre of mass, blurs |
| Only 30,000 of 124,800 training images used | Full dataset + shift augmentation |
| `train_model.py` crashed (`json` not imported) | Fixed |
| No way to see why a guess was wrong | UI shows all 26 probabilities, the 28×28 input, neuron activity |

## Tips for good predictions
Draw **big**, fill most of the canvas, one capital letter, clear strokes. EMNIST merges upper/lower case in one class, so both styles work.

## Tests
```powershell
python -m unittest discover tests -v
```
