from flask import current_app, Blueprint, render_template, jsonify, g, Response, send_file, request, send_from_directory
from pyWebCamWebServerMonitor import auth, main_dir, db
from pyWebCamWebServerMonitor.models.setting import Setting 
from pyWebCamWebServerMonitor.models.user import User
from datetime import datetime
from functools import wraps
import cv2 as cv 
import os
import subprocess
import json
import random
import string
import pathlib
import re
  
webcam = Blueprint('webcam', __name__, url_prefix='/api/webcam')

# Module Global Vars
is_record = False
is_live = False
stream_id = None
live_frame = None
recording_proc = None
encoding_proc = None
#lock = threading.Lock()
last_video_file = None
encoding_video_file = None


# Global Vars set from outside module
default_webcam = '/dev/video0'
is_encoding = True
frame_rate_no = 15
is_auto_naming = False
is_stream = False
default_size_for_cam = False


def auth_required(f):
  if request.endpoint in current_app.view_functions:
    view_func = current_app.view_functions[request.endpoint]
    if hasattr(view_func, 'exclude_auth'):
      @wraps(f)
      def decorated(*args, **kwargs):
        return f(*args, **kwargs)
      return decorated
    else:
      @wraps(f)
      @auth.login_required
      def decorated(*args, **kwargs):
        return f(*args, **kwargs)
      return decorated
 
def exclude_form_auth(func):
  func.exclude_auth = True
  return func

@webcam.before_request
def before_request():
  pass

 
def change_setting(setting, value):
  listSettings = ['default_webcam', 'frame_rate_no', 'is_encoding',
                  'is_auto_naming', 'default_size_for_cam', 'is_stream']
  if setting in listSettings:
    globals()[setting] = value
  else:
    print("Error Change Setting: Invalid setting name")


def _get_random_alphanumeric_string(letters_count, digits_count):
    sample_str = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))

    # Convert string to list and shuffle it to mix letters and digits
    sample_list = list(sample_str)
    random.shuffle(sample_list)
    final_string = ''.join(sample_list)
    return final_string

def _is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None

def _get_webcams():
    import glob
    cameras = []
    for camera in glob.glob("/dev/video?"):
      cap = cv.VideoCapture(camera) 
      if cap is None or not cap.isOpened():
        cameras.append( {'camera':camera, 'active':0} ) 
      else:
         cameras.append( {'camera':camera, 'active':1} ) 
    cap.release()
    return cameras

def _is_cam_ok(cam):
  cap = cv.VideoCapture(cam)
  if cap is None or not cap.isOpened():
    return False
  else:
    if cap is not None: cap.release()
    return True


def _clean_stream_dir():
  stream_dir = main_dir + '/stream/'
  files = os.listdir(stream_dir)
  for f in files:
    try:
      os.remove(stream_dir + f)
    except Exception:
      pass

def start_cap():
  if is_live is False: return  None
  
  #def live_thread():
  cam = default_webcam

  cap = cv.VideoCapture(cam)

  cap_size = default_size_for_cam.split('x')
  cap.set(cv.CAP_PROP_FRAME_WIDTH, int(cap_size[0]))
  cap.set(cv.CAP_PROP_FRAME_HEIGHT, int(cap_size[1]))

  while(is_live):
    #with lock:
      # Capture frame-by-frame
    ret, live_frame = cap.read()
    
    if live_frame is not None:
      (flag, encodedImage) = cv.imencode(".jpg", live_frame)

      # ensure the frame was successfully encoded
      if not flag:
        continue

    # yield the output frame in the byte format
    if 'encodedImage' in locals():
      
      yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
        bytearray(encodedImage) + b'\r\n')

  cap.release()
 
@webcam.route("/set/is-stream", methods=['POST'])
def set_default_is_stream():
  global is_stream
  stream = request.json.get('isStream')
  if stream is None:
    return  jsonify(error=True, msg='IsStream not set')
  stream = bool(stream)
  is_stream = stream
  db_is_stream = Setting.query.filter_by(name='is_stream').first()
  db_is_stream.value = ('False', 'True')[stream]
  db.session.commit()
  return  jsonify(error=False)
 
@webcam.route("/set/encoding", methods=['POST'])
def set_default_encoding():
  global is_encoding
  encoding = request.json.get('encoding')
  if encoding is None:
    return  jsonify(error=True, msg='No encoding submited')
  encoding = bool(encoding)
  is_encoding = encoding
  db_is_encoding = Setting.query.filter_by(name='is_encoding').first()
  db_is_encoding.value = ('False', 'True')[encoding]
  db.session.commit()
  return  jsonify(error=False)

@webcam.route("/set/framerate", methods=['POST'])
def set_default_framerate():
  global frame_rate_no 
  frame_rate  = request.json.get('framerate')
  if frame_rate is None:
    return  jsonify(error=True, msg='Framerate empty')
  frame_rate = int(frame_rate)
  if (frame_rate < 1) or (frame_rate > 200):
    return  jsonify(error=True, msg='Framerate invalid')
  frame_rate_no = frame_rate
  db_frame_rate_no = Setting.query.filter_by(name='frame_rate_no').first()
  db_frame_rate_no.value = frame_rate_no
  db.session.commit()
  return  jsonify(error=False)

 
@webcam.route("/set/auto-naming", methods=['POST'])
def set_default_auto_naming():
  global is_auto_naming 
  auto_naming  = request.json.get('naming')
  if auto_naming is None:
    return  jsonify(error=True, msg='Auto naming option empty')
  auto_naming = bool(auto_naming)
  is_auto_naming = auto_naming
  db_is_auto_naming = Setting.query.filter_by(name='is_auto_naming').first()
  db_is_auto_naming.value = ('False', 'True')[auto_naming]
  db.session.commit()
  return  jsonify(error=False)

@webcam.route("/set/default-webcam", methods=['POST'])
def set_default_webcam():
  global default_webcam
  cam = request.json.get('cam')
  if cam is None:
    return  jsonify(error=True, msg='No webcamera submited')
  cams = []
  for wCam in _get_webcams():
    cams.append(wCam['camera'])

  if cam not in cams:
    return  jsonify(error=True, msg=cam+' is not a valid webcamera on this system')
  default_webcam = cam
  db_default_webcam = Setting.query.filter_by(name='default_webcam').first()
  db_default_webcam.value = str(default_webcam)
  db.session.commit()
  return  jsonify(error=False)

@webcam.route("/get/default-webcam")
def get_defaut_cam():
  db_default_webcam = Setting.query.filter_by(name='default_webcam').first()
  if db_default_webcam is not None:
     return jsonify(error=False, camera=db_default_webcam.value)
  else:
     return jsonify(error=True, msg='Default camera row not found')

@webcam.route("/get/what-sizes-cam")
def get_sizes_cam(cam=None):
  if (request.args.get('cam') is None) and (cam is None):
    return  jsonify(error=True, msg='No webcam was given.')
  camera = (cam, request.args.get('cam') )[cam is None]
  video_camSizes_cmd = subprocess.run("ffmpeg -f video4linux2 -list_formats all -i {}".format(camera), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
  output = str(video_camSizes_cmd.stdout + video_camSizes_cmd.stderr)
  if 'Motion-JPEG : ' in output:
   sizes = output.split('Motion-JPEG : ')[1].split('\\')[0].split(" ")
   sizeResp = { 'sizes': sizes}
   return  Response(json.dumps(sizeResp),  mimetype='application/json')
  else:
    return  jsonify(error=True, msg='No sizes found maybe webcam invalid')
  return  jsonify(error=False, size=str(size), duration=str(video_duration_cmd.stdout))

@webcam.route("/get/def-cam-size")
def get_def_cam_size():
  return  jsonify(error=False, defCamSize=default_size_for_cam)

@webcam.route("/set/cam-maximum-size", methods=['POST'])
def set_cam_max_size(cam=None):
  global default_size_for_cam
  if ((request.json.get('cam') is None) ) and ( cam is None ):
    return  jsonify(error=True, msg='No webcam and size was given')
  camera = (cam,request.json.get('cam'))[ cam is None ]
  sizes = json.loads(get_sizes_cam(camera).get_data())["sizes"]
  sizes_dic = {}
  for size in sizes:
    sizes_dic = {**sizes_dic, **{ size: eval(size.replace('x', '+')) }}  
  key_max = max(sizes_dic.keys(), key=(lambda k: sizes_dic[k]))
  default_size_for_cam = key_max
  db_default_webcam = Setting.query.filter_by(name='default_size_for_cam').first()
  db_default_webcam.value = default_size_for_cam
  db.session.commit()
  return  jsonify(error=False, size=key_max)


@webcam.route("/set/cam-size", methods=['POST'])
def set_cam_size(cam=None, size=None):
  global default_size_for_cam
  if ((request.json.get('cam') is None) or ( request.json.get('size') is None )) and ((cam is None) or (size is None)):
    return  jsonify(error=True, msg='No webcam and size was given')
  camera = (cam,request.json.get('cam'))[ cam is None ]
  size = (cam,request.json.get('size'))[ size is None ] 
  if( size not in json.loads(get_sizes_cam(camera).get_data())["sizes"]):
    return  jsonify(error=True, msg='Size invalid for this cam')
  else:
    default_size_for_cam = size
    db_default_webcam = Setting.query.filter_by(name='default_size_for_cam').first()
    db_default_webcam.value = default_size_for_cam
    db.session.commit()
    return  jsonify(error=False)
  




@webcam.route("/video/feed")
@exclude_form_auth
def video_feed():
  cam = default_webcam
  responseHeaders = {
  'Cache-Control':'no-cache, no-store, must-revalidate',
   'Pragma' : 'no-cache',
   'Expires' : '0',
  }
  token = request.args.get('t')
  if (_is_cam_ok(cam) is False) or ( not User.verify_auth_token(token) ):
    return send_file(
                  main_dir + "/res/webcamBusy.png",
                  mimetype='image/png', cache_timeout=0
            )
  # return the response generated along with the specific media
  # type (mime type)
  return Response(start_cap(),
    mimetype = "multipart/x-mixed-replace; boundary=frame", headers=responseHeaders)
 


@webcam.route('stop/live')
def stop_live():
  global is_live
  print("in live")
  if (_is_cam_ok(default_webcam) is False) or (is_live is True ):
    print("stop live")
    is_live = False
    return  jsonify(error=False, msg="live url stoped")
  else:
    return  jsonify(error=True, msg="cam is not live")

@webcam.route('start/live')
def start_live():
  global is_live
  if (is_live is False) and (_is_cam_ok(default_webcam) is True) and (is_record is False):
    is_live = True
    return  jsonify(error=False, msg="live url started")
  else:
    return  jsonify(error=True, msg="webcam is busy")


@webcam.route('is/live')
def is_live_cam():
  return  jsonify(live=is_live)


#ffmpeg -f dshow -i -vcodec libx264 -preset ultrafast -tune zerolatency -r 10 -async 1 -acodec libmp3lame -ab 24k -ar 22050 -bsf:v h264_mp4toannexb -maxrate 750k -bufsize 3000k -f mpegts udp://192.168.5.215:48550
#ffmpeg -i http://<server_ip>:8090/0.mpg -vcodec libvpx http://localhost:8090/0_webm.ffm
#ffmpeg -f video4linux2 -standard ntsc -i /dev/video0 http://<server_ip>:8090/0.ffm

@webcam.route('record/video')
def record_webcam():
  global is_record
  global recording_proc
  global frame_rate_no
  global last_video_file
  global stream_id
  is_record = True
  encoding = ''
  if request.args.get('vidName') is not None:
    match = re.search(r'^[^_:\.\\\/\|<>*"?]+$', request.args.get('vidName'))
    if match:
      name = request.args.get('vidName').rstrip().lstrip()
    else:
      is_record = False
      return  jsonify(error=True, msg='Invalid file name')
  else:
    name = 'VID-'+_get_random_alphanumeric_string(3,3)
  cam = default_webcam
  dateAndTime = datetime.now().isoformat()
  dateAndTime = dateAndTime[:dateAndTime.find('.')]
  dateAndTime = dateAndTime.replace(":", "-")
  filename =  dateAndTime + '_'+ name #generated with more complexity in the actual code, but that isn't important
  if is_encoding is False:
    filename += '_notEnc'
    filename += '.mkv'
    encoding = '-c copy'
  else:
    encoding = '-preset veryfast'
    filename += '.mp4'
  last_video_file = filename
  outputPath = main_dir + '/videos/' + filename
  if not isinstance(frame_rate_no, int):
    frame_rate_no = 15
  
  #Posb stream
  #ffmpeg -i ... -c:v libx264 -c:a mp2 -f tee -map 0:v -map 0:a "archive-20121107.mkv|[f=mpegts]udp://10.0.1.255:1234/"
  #ffmpeg -i "http://host/folder/file.m3u8" -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 file.mp4
  #ffmpeg -f v4l2 -framerate 15 -video_size 1280x720 -input_format mjpeg -i /dev/video0 -c:v libx264 -f tee -map 0:v "test.mp4|[f=mpegts]test.m3u8"

  #filename_out = timestamp + 'something.mkv' #generated with more complexity in the actual code, but that isn't important
  #ffmpeg_cmd = 'ffmpeg -t {} -an -i {} -c:v libx264 -preset veryslow -crf 25 {}'.format(seconds, cam, filename).split()
  #ffmpeg -f v4l2 -list_formats all -i /dev/video0
  print("Starting Recoding")
  #yuyv422 -c copy
  if is_stream is False:
    ffmpeg_cmd = 'ffmpeg -f v4l2 -framerate {} -video_size {} -input_format mjpeg -i {} {} file:"{}"'.format(frame_rate_no, default_size_for_cam, cam, encoding, outputPath)
  else:
    
    if is_encoding is False:
      return  jsonify(error=False, recording=True)

    _clean_stream_dir()
    stream_id = _get_random_alphanumeric_string(8,0)
    stearmPath = main_dir + '/stream/s'+ stream_id +'.m3u8' 
    ffmpeg_cmd = 'ffmpeg -f v4l2 -framerate {} -video_size {} -input_format mjpeg -i {} {} -c:v libx264 -flags +cgop -g 5 -tune zerolatency -f tee -map 0:v "{}|[f=hls:hls_time=2:hls_list_size=10:hls_wrap=60:hls_delete_threshold=1:hls_flags=delete_segments]{}"'.format(frame_rate_no, default_size_for_cam, cam, encoding, outputPath, stearmPath)
  recording_proc = subprocess.Popen('exec ' + ffmpeg_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None, close_fds=True)
  '''
  while True:
    output = proc.stdout.readline()
    if proc.poll() is not None:
      break
    if output:
      emit('server-inst-stdout', {'data': output.strip()})
      #print(output.strip())
      print(is_record)
    if is_record is False:
      proc.terminate()
  rc = proc.poll()
  '''
  return  jsonify(error=False, recording=True)


@webcam.route('record/get-options')
def record_get_options():
  return  jsonify(encoding=is_encoding, autoNaming=is_auto_naming, stream=is_stream, frameRate=frame_rate_no)

@webcam.route('record/video-stop')
def record_video_stop():
  global is_record
  global recording_proc
  global stream_id
  if is_record:
    if recording_proc is not None:
      recording_proc.terminate()
      while True:
        if recording_proc.poll() is not None:
            break
    last_video_file=None
    is_record = False
    stream_id = None
  return  jsonify(recording=False)

@webcam.route('record/status')
def record_video_status():
  global is_record
  return  jsonify(recording=is_record)

@webcam.route('get/videos')
def get_videos():
  
  path = main_dir + '/videos/'
  files = os.listdir(path)

  encFile = False
  stream = False
  if is_record :
    if is_stream is False:
      if last_video_file is not None:
        files.remove(last_video_file)
    else:
      stream=last_video_file
  
  if encoding_video_file is not None:
    print(encFile)
    encFile = encoding_video_file.split('_notEnc')[0]+'.mp4'
    if encoding_video_file in files:
      files.remove(encoding_video_file)
    

  files = {"videos": files, 'stream': stream, 'streamId': stream_id, 'encode':encFile}
  return  Response(json.dumps(files),  mimetype='application/json')

@webcam.route('get/last-video-name')
def get_last_video_name():
  global last_video_file
  if last_video_file is None:
    return  jsonify(error=True, msg='There is no video active')
  else:
    return  jsonify(error=False, name=last_video_file)


@webcam.route('delete/video')
def delete_video():
  if request.args.get('vidName') is None:
    return  jsonify(error=True, msg='No video name was given.')
  vidName =request.args.get('vidName')
  filename = main_dir + '/videos/' + vidName
  videoFile = pathlib.Path(filename)
  if not videoFile.exists():
    return  jsonify(error=True, msg='This file doesn\'t exists')
  try:
    os.remove(filename)
    return jsonify(error=False, msg='File Deleted')
  except Exception as e:
    return jsonify(error=True, msg=str(e)) 

@webcam.route('download/video')
def download_video():
  if request.args.get('vidName') is None:
    return  jsonify(error=True, msg='No video name was given.')
  vidName = request.args.get('vidName')
  filename = main_dir + '/videos/' + vidName
  videoFile = pathlib.Path(filename)
  if not videoFile.exists():
    return  jsonify(error=True, msg='This file dosen\'t exists')
  try:
    return send_file(
                    filename,
                    attachment_filename=vidName,
                    mimetype='video/mp4',
                    as_attachment=True
              )
  except Exception as e:
    return jsonify(error=True, msg=str(e))


@webcam.route('feed-for/stream/<file_name>')
def feed_for_stream(file_name):
  file_dir = main_dir + '/stream/'
  try:
    return send_from_directory(file_dir, file_name, cache_timeout=-1)
  except Exception as e:
    return jsonify(error=True, msg=str(e))


@webcam.route('feed-for/video')
def feed_for_video():
  if request.args.get('vidName') is None:
    return  jsonify(error=True, msg='No video name was given.')
  vidName = request.args.get('vidName')
  filename = main_dir + '/videos/' + vidName
  videoFile = pathlib.Path(filename)
  if not videoFile.exists():
    return  jsonify(error=True, msg='This file dosen\'t exists')
  try:
    return send_from_directory( main_dir + '/videos/', vidName, cache_timeout=-1)
  except Exception as e:
    return jsonify(error=True, msg=str(e))

@webcam.route('encode/video', methods=['POST'])
def encode_video():
  global encoding_proc
  global encoding_video_file
  if request.json.get('vidName') is None:
    return  jsonify(error=True, msg='No video name was given.')
  vidName = request.json.get('vidName')
  filename = main_dir + '/videos/' + vidName
  videoFile = pathlib.Path(filename)
  if not videoFile.exists():
    return  jsonify(error=True, msg='This file dosen\'t exists')
  filename_output = filename.split('_notEnc')[0]+'.mp4'
  encoding_video_file = vidName
  ffmpeg_cmd = 'ffmpeg -i file:"{}" -c:v libx264 -preset veryfast file:"{}"'.format(filename, filename_output)
  encoding_proc = subprocess.Popen('exec ' + ffmpeg_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None, close_fds=True)
  return jsonify(error=False)


@webcam.route('is-encode/video')
def is_encode_video():
  global encoding_video_file
  global encoding_proc
  if encoding_proc is None:
    return jsonify(error=False, encoding=False)

  if encoding_proc.poll() is not None:
    encoding_proc = None
    if encoding_video_file is not None:
      videoFile =  main_dir + '/videos/' + encoding_video_file
      if pathlib.Path(videoFile).exists():
        os.remove(videoFile)
        temp_enc_file = encoding_video_file
        encoding_video_file = None
        return jsonify(error=False, encoding=False, file=temp_enc_file)
      else:
        return jsonify(error=False, encoding=False)
    else:
      return jsonify(error=False, encoding=False)
  else:
    return jsonify(error=False, encoding=True)

@webcam.route('getinfo/video')
def get_info_video():
  path = main_dir + '/videos/'
  if request.args.get('vidName') is None:
    return  jsonify(error=True, msg='No video name was given.')
  vidName = request.args.get('vidName')
  filename = path + vidName
  videoFile = pathlib.Path(filename)
  if not videoFile.exists():
    return  jsonify(error=True, msg='This file dosen\'t exists')
  size = videoFile.stat().st_size
  video_duration_cmd = subprocess.run("ffmpeg -i file:'{}' 2>&1 | grep 'Duration'| cut -d ' ' -f 4 | sed s/,//".format(filename), shell=True, stdout=subprocess.PIPE)
  return  jsonify(error=False, size=str(size), duration=str(video_duration_cmd.stdout))


@webcam.route('get/video-store-path')
def get_videos_store_path():
  return  jsonify(path= main_dir + '/videos/')

@webcam.route('check/devices')
def check_webcam():
  cameras = _get_webcams()
  return  Response(json.dumps(cameras),  mimetype='application/json')

@webcam.route('check/ffmpeg')
def check_ffmpeg():
  return  jsonify(check=_is_tool("ffmpeg"))

@webcam.route('inst/ffmpeg')
def index():
 
    def proc_emit_live(process):
      while True:
        output = process.stdout.readline()
        if process.poll() is not None:
          break
        if output:
          #socketio.emit('server-inst-stdout', {'data': output.strip()})
          print(output.strip())
      rc = process.poll()
      return jsonify(end="install ffmpeg executed")      

    try:
      is_admin = os.getuid() == 0
      print(is_admin)
    except Exception:
      pass
    
    if _is_tool('apt-get'):
      proc = subprocess.Popen('apt-get install -y ffmpeg', shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
      return proc_emit_live(proc)
    elif _is_tool('yum'):
      proc = subprocess.Popen('yum install -y ffmpeg', shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
      return proc_emit_live(proc)
    elif _is_tool('dnf'):
      proc = subprocess.Popen('dnf install -y ffmpeg', shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
      return proc_emit_live(proc)
   
    else: 
      return jsonify(error=True, msg="apt, apt-get, yum or dnf not present can't install ffmpeg")

 