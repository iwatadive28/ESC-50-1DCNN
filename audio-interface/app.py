from flask import Flask, request, jsonify
from inference import load_inference_model, predict_audio, decode_predictions
import os

app = Flask(__name__)

# モデルロード
model = load_inference_model()
labels = ["Other", "People"]  # クラス名を定義

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # ファイルを受け取る
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # ファイル保存
        temp_path = f"/tmp/{file.filename}"
        file.save(temp_path)
        if not os.path.exists(temp_path):
            return jsonify({'error': f'Failed to save file: {temp_path}'}), 500

        # 推論実行
        predictions, predicted_class = predict_audio(temp_path, model)
        predicted_label = decode_predictions(predicted_class, labels)

        # 結果を返却（データ型を変換）
        return jsonify({
            'predicted_class': int(predicted_class),  # numpy.int64 を int に変換
            'predicted_label': predicted_label,
            'confidence': float(predictions[0][predicted_class])  # numpy.float を float に変換
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
