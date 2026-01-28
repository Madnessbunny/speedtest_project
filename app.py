from flask import Flask, render_template, Response, stream_with_context
import speedtest
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testar_stream')
def testar_stream():
    def generate():
        try:
            st = speedtest.Speedtest()
            yield f"data: {json.dumps({'log': 'Iniciando teste...'})}\n\n"
            st.get_best_server()
            yield f"data: {json.dumps({'log': 'Servidor encontrado!'})}\n\n"
            
            dl = st.download() / 1_000_000
            yield f"data: {json.dumps({'log': 'Download concluído.'})}\n\n"
            
            ul = st.upload() / 1_000_000
            yield f"data: {json.dumps({'log': 'Upload concluído.'})}\n\n"
            
            res = {
                'download': f"{dl:.2f}",
                'upload': f"{ul:.2f}",
                'ping': f"{st.results.ping:.0f}",
                'final': True
            }
            yield f"data: {json.dumps(res)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'log': f'Erro: {str(e)}'})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')
    
import os

if __name__ == '__main__':
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
