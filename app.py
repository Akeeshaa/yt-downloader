from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return 'YouTube Downloader API running!'

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [info])
            best_format = formats[-1]
            return jsonify({
                'title': info.get('title'),
                'download_url': best_format.get('url')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)