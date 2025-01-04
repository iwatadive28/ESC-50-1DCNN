import librosa
import numpy as np
from tensorflow.keras.models import load_model
from tkinter import Tk, filedialog
import sounddevice as sd
import soundfile as sf
import os

# ハイパーパラメータ
SAMPLE_RATE = 16000
DURATION = 3  # 秒数
MODEL_SAVE_PATH = "/app/model/trained_1d_cnn_model.keras"

# 音声録音
def record_audio():
    print("録音を開始します...")
    audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()  # 録音終了まで待機
    output_file = "recorded_audio.wav"
    sf.write(output_file, audio_data, SAMPLE_RATE)
    print(f"録音が完了しました: {output_file}")
    return output_file

# 音声ファイルのアップロード（ファイル選択ウィンドウ）
def upload_audio():
    file_path = input("音声ファイルのフルパスを入力してください: ").strip()
    if not os.path.exists(file_path):
        print("ファイルが存在しません。正しいパスを指定してください。")
        exit(1)
    print(f"指定されたファイル: {file_path}")
    return file_path

# 音声の前処理
def preprocess_audio(file_path):
    try:
        # 音声ファイルを読み込み
        y, sr = librosa.load(file_path, sr=SAMPLE_RATE)
    except Exception as e:
        print(f"音声ファイルの読み込みに失敗しました: {e}")
        exit(1)
    
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
    predicted_label = labels[predicted_class]
    return predicted_label

# メイン処理
def main():
    # モデルのロード
    print("モデルをロードしています...")
    model = load_model(MODEL_SAVE_PATH)
    print("モデルをロードしました。")

    # ラベル定義（必要に応じて変更）
    labels = ["クラス1", "クラス2"]  # クラス名を定義

    # 音声録音またはアップロードを選択
    print("音声ファイルをアップロードしますか？:0 , 音声を録音しますか？:1")
    choice = input("選択: ").strip()

    if choice == '1':
        file_path = record_audio()
    elif choice == '0':
        file_path = upload_audio()
    else:
        print("無効な選択です。終了します。")
        return

    # 推論
    print("推論を開始します...")
    predictions, predicted_class = predict_audio(file_path, model)
    predicted_label = decode_predictions(predicted_class, labels)

    print(f"推論結果: クラス {predicted_class} ({predicted_label})")
    print(f"信頼スコア: {predictions[0][predicted_class]:.4f}")

# 実行
if __name__ == "__main__":
    main()
