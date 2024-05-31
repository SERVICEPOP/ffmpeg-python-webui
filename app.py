from flask import Flask, request, jsonify, render_template, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scale_video', methods=['POST'])
def scale_video():
    input_file = request.form['input_file']
    output_file = request.form.get('output_file', 'out.mp4')
    resolution = request.form.get('resolution', '1920:1080')
    
    command = ['ffmpeg', '-i', input_file, '-filter:v', f'scale={resolution}', output_file]
    subprocess.run(command)
    return redirect(url_for('index'))

@app.route('/set_aspect_ratio', methods=['POST'])
def set_aspect_ratio():
    input_file = request.form['input_file']
    output_file = request.form.get('output_file', 'out.mp4')
    aspect_ratio = request.form.get('aspect_ratio', '16/9')
    
    command = ['ffmpeg', '-i', input_file, '-c', 'copy', '-aspect', aspect_ratio, output_file]
    subprocess.run(command)
    return redirect(url_for('index'))

@app.route('/reverse_video', methods=['POST'])
def reverse_video():
    input_file = request.form['input_file']
    output_file = 'reversed.mp4'
    
    command = ['ffmpeg', '-i', input_file, '-vf', 'reverse', '-af', 'areverse', output_file]
    subprocess.run(command)
    return redirect(url_for('index'))

@app.route('/concatenate_videos', methods=['POST'])
def concatenate_videos():
    input_file = request.form['input_file']
    reversed_file = 'reversed.mp4'
    mylist_file = 'mylist.txt'
    loopcropped_file = 'loopcropped.mp4'
    finished_product = request.form.get('output_file', 'finishedproduct.mp4')
    music_file = request.form['music_file']
    
    # Create reversed video
    subprocess.run(['ffmpeg', '-i', input_file, '-vf', 'reverse', '-af', 'areverse', reversed_file])
    
    # Create mylist.txt file
    with open(mylist_file, 'w') as f:
        f.write(f"file '{input_file}'\n")
        f.write(f"file '{reversed_file}'\n")
    
    # Concatenate videos
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', mylist_file, '-c', 'copy', loopcropped_file])
    os.remove(reversed_file)
    os.remove(mylist_file)
    
    # Loop and add music
    subprocess.run(['ffmpeg', '-stream_loop', '-1', '-i', loopcropped_file, '-i', music_file, '-c:v', 'copy', '-shortest', '-map', '0:v:0', '-map', '1:a:0', finished_product])
    os.remove(loopcropped_file)
    
    return redirect(url_for('index'))

@app.route('/extract_audio', methods=['POST'])
def extract_audio():
    input_file = request.form['input_file']
    output_file = request.form.get('output_file', 'output-audio.wav')
    
    command = ['ffmpeg', '-i', input_file, '-vn', '-acodec', 'copy', output_file]
    subprocess.run(command)
    return redirect(url_for('index'))

@app.route('/create_slow_motion_video', methods=['POST'])
def create_slow_motion_video():
    input_file = request.form['input_file']
    output_file = request.form.get('output_file', 'slow_motion.mp4')
    
    command = ['ffmpeg', '-i', input_file, '-filter:v', 'minterpolate', '-r', '120', output_file]
    subprocess.run(command)
    return redirect(url_for('index'))

@app.route('/create_video_from_image_and_audio', methods=['POST'])
def create_video_from_image_and_audio():
    image_file = request.form['image_file']
    audio_file = request.form['audio_file']
    output_file = request.form.get('output_file', 'out.mp4')
    
    command = ['ffmpeg', '-loop', '1', '-i', image_file, '-i', audio_file, '-c:v', 'libx264', '-tune', 'stillimage', '-c:a', 'aac', '-b:a', '192k', '-pix_fmt', 'yuv420p', '-shortest', output_file]
    subprocess.run(command)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
