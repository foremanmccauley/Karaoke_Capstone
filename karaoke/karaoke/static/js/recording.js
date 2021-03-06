let preview = document.getElementById("preview");
let recording = document.getElementById("recording");
let startButton = document.getElementById("startButton");
let stopButton = document.getElementById("stopButton");
let downloadButton = document.getElementById("downloadButton");
let logElement = document.getElementById("log");
let audio = document.getElementsByTagName("audio")[0];
let recordingTimeMS =1000;

audio.onloadedmetadata = function() {
  //alert(audio.duration);
 recordingTimeMS =((audio.duration+1)*1000);

};

function log(msg) {
    logElement.innerHTML += msg + "\n";
  }

function wait(delayInMS) {
    return new Promise(resolve => setTimeout(resolve, delayInMS));
  }

function startRecording(stream, lengthInMS) {
    let recorder = new MediaRecorder(stream);
    let data = [];
  
    recorder.ondataavailable = event => data.push(event.data);
    if (audio)
      audio.play();
    recorder.start();
    log(recorder.state + "! for " + (lengthInMS/1000) + " seconds...");
      log(recorder.state + "!");

  
    let stopped = new Promise((resolve, reject) => {
      recorder.onstop = resolve;
      recorder.onerror = event => reject(event.name);
    });
  
    let recorded = wait(lengthInMS).then(
     () => recorder.state == "recording" && recorder.stop()
    );
  
    return Promise.all([
      stopped,
      recorded
    ])
    .then(() => data);
  }


function stop(stream) {
    stream.getTracks().forEach(track => track.stop());
    if (audio)
      audio.pause();
  }

startButton.addEventListener("click", function() {
  
    navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true
    }).then(stream => {
      log(audio.duration);
      //recordingTimeMS=audio.duration;
      preview.srcObject = stream;
      downloadButton.href = stream;
      preview.captureStream = preview.captureStream || preview.mozCaptureStream;
      return new Promise(resolve => preview.onplaying = resolve);
    }).then(() => startRecording(preview.captureStream(), recordingTimeMS))
    .then (recordedChunks => {
      let recordedBlob = new Blob(recordedChunks, { type: "video/webm" });
      recording.src = URL.createObjectURL(recordedBlob);
      downloadButton.href = recording.src;
      downloadButton.download = "karaokevideo.webm";
  
      //log("Successfully recorded " + recordedBlob.size + " bytes of " +
         // recordedBlob.type + " media.");
         log("Successfully recorded ");
    })
    .catch(log);
  }, false);


stopButton.addEventListener("click", function() {
    stop(preview.srcObject);
    
  }, false);