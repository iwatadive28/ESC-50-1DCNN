from pydub import AudioSegment
import librosa
import numpy as np
from tensorflow.keras.models import load_model

# ハイパーパラメータ
SAMPLE_RATE = 16000
DURATION = 3  # 秒数
MODEL_SAVE_PATH = "/app/model/trained_1d_cnn_model.keras"

# 音声の前処理
def preprocess_audio(file_path):
    try:
        # m4aをwavに変換（pydub使用）
        if file_path.endswith('.m4a'):
            audio = AudioSegment.from_file(file_path, format="m4a")
            temp_wav_path = file_path.replace('.m4a', '.wav')
            audio.export(temp_wav_path, format="wav")
            file_path = temp_wav_path

        # librosaで音声読み込み
        y, sr = librosa.load(file_path, sr=SAMPLE_RATE)
    except Exception as e:
        raise ValueError(f"音声ファイルの読み込みに失敗しました: {e}")
    
    # 指定された長さに切り詰めるか、ゼロ埋め
    max_length = SAMPLE_RATE * DURATION
    if len(y) > max_length:
        y = y[:max_length]
    else:
        y = np.pad(y, (0, max_length - len(y)))

    # 正規化
    y = y / np.max(np.abs(y))

    # モデル入力形式に整形
    return y.reshape(1, -1, 1)

# 推論
def predict_audio(file_path, model):
    audio_input = preprocess_audio(file_path)
    predictions = model.predict(audio_input)
    predicted_class = np.argmax(predictions)
    return predictions, predicted_class

# ラベル変換
def decode_predictions(predicted_class, labels):
    return labels[predicted_class]

# モデルのロード
def load_inference_model():
    try:
        model = load_model(MODEL_SAVE_PATH)
        return model
    except Exception as e:
        raise ValueError(f"モデルのロードに失敗しました: {e}")
