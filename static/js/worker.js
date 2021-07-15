function sendResultToMainThread(someArgs) {
  // Joins arbitrary number of arguments
  var toLog = []
  for (var i = 0; i < arguments.length; i++) {
    toLog.push(arguments[i])
  }
  // ... and sends to main thread
  postMessage(toLog.join(' '))
}

onmessage = function(e) {
  var prog = e.data.prog
  prog = prog.split('console.log').join('sendResultToMainThread')
  eval(prog)
}
