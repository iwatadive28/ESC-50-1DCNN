import csv
import wave
import os
import numpy as np
from pydub import AudioSegment
import librosa
from tensorflow.keras.models import load_model
from plot_waveform import plot_waveform

# ハイパーパラメータ
SAMPLE_RATE = 16000
DURATION = 3  # 秒数
MODEL_SAVE_PATH = "/app/model/trained_1d_cnn_model.keras"

# ファイル名を安全に生成する関数
def generate_wav_filename(original_csv_path):
    """CSVファイル名を基にした安全なWAVファイル名を生成"""
    sanitized_name = os.path.basename(original_csv_path).replace(".csv", "").replace(" ", "_").replace("/", "_")
    return f"output/{sanitized_name}.wav"

# CSVをWAVに変換する関数
def csv_to_wav(csv_file_path, wav_file_path, sample_rate):
    try:
        # CSVファイルの読み込み
        with open(csv_file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            data = next(reader)  # 1行目を取得

        # 数値に変換（空文字列や不正なデータをフィルタリング）
        audio_data = []
        for value in data:
            if value.strip():  # 空文字を除外
                try:
                    audio_data.append(int(value))
                except ValueError:
                    raise ValueError(f"不正な値が見つかりました: {value}")

        # 配列に変換
        audio_data = np.array(audio_data, dtype=np.int16)

        # 正規化（-1.0〜1.0の範囲にスケール）
        audio_data = audio_data / np.max(np.abs(audio_data))

        # 出力ディレクトリの確認と作成
        os.makedirs(os.path.dirname(wav_file_path), exist_ok=True)

        # WAVファイルに書き込み
        with wave.open(wav_file_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # モノラル
            wav_file.setsampwidth(2)  # サンプル幅（16ビット）
            wav_file.setframerate(sample_rate)
            wav_file.writeframes((audio_data * 32767).astype(np.int16).tobytes())

        return wav_file_path
    except Exception as e:
        raise ValueError(f"CSVファイルをWAVに変換する際にエラーが発生しました: {e}")

# 音声の前処理
def preprocess_audio(file_path):
    try:
        # m4aをwavに変換（pydub使用）
        if file_path.endswith('.m4a'):
            audio = AudioSegment.from_file(file_path, format="m4a")
            temp_wav_path = file_path.replace('.m4a', '.wav')
            audio.export(temp_wav_path, format="wav")
            file_path = temp_wav_path

        elif file_path.endswith('.csv'):
            # csvをwavに変換
            temp_wav_path = generate_wav_filename(file_path)
            file_path = csv_to_wav(file_path, temp_wav_path, sample_rate=10000)

        # librosaで音声読み込み
        y, sr = librosa.load(file_path, sr=SAMPLE_RATE)
    except Exception as e:
        raise ValueError(f"音声ファイルの読み込みに失敗しました: {e}")

    # 出力ディレクトリの確認と作成
    os.makedirs("output", exist_ok=True)

    # 波形データとサンプルレートを渡してプロット
    plot_waveform(y, SAMPLE_RATE, file_path.replace('.wav', '.png'))

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
