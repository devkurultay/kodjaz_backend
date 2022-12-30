(function(payload){

  var APPEND_MODE = 'a'
  var OUTPUT_EL = document.getElementById('output')
  var w

  $(document).ready(writeEditorContentToFileTextArea)
  $('#run').on('click', runit)
  $('#hintToggle').on('click', function () {
    $('#hint').toggleClass('hidden')
  })

  var editor = ace.edit("code")
  editor.setTheme("ace/theme/vibrant_ink")
  if (payload.programmingLanguage == 'Python') {
    editor.session.setMode("ace/mode/python")
  }
  else if (payload.programmingLanguage === 'JavaScript') {
    editor.session.setMode("ace/mode/javascript")
  }
  else if (payload.programmingLanguage === 'TypeScript') {
    editor.session.setMode("ace/mode/typescript")
  }

  // Textarea for working with a "file"
  var fileTextAreaId = "file.txt"
  var fileTextArea = document.getElementById(fileTextAreaId)

  var fileEditor = ace.edit("file")
  fileEditor.setTheme("ace/theme/vibrant_ink")
  fileEditor.session.setMode("ace/mode/text")

  function writeEditorContentToFileTextArea() {
    var val = fileEditor.getValue()
    fileTextArea.innerHTML = val
  }

  fileEditor.on('change', function() {
    writeEditorContentToFileTextArea()
  })

  // Write text editor value to the textarea
  $('#file-tab').on('shown.bs.tab', function(e) {
    fileEditor.focus()
    fileEditor.resize()
    fileEditor.execCommand("gotolineend")
  })

  function outf(text) {
    var mypre = document.getElementById(payload.outputElementId)
    mypre.innerHTML = ''
    text = text.replace(/</g, '&lt;')
    mypre.innerHTML = mypre.innerHTML + text
  }

  function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
      throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
  }

  function filewrite(fileObj, x) {
    var fileTextAreaNode = document.getElementById(fileObj.name)
    var valueToWrite = x.v
    var mode = fileObj.mode.v
    var isAppendMode = mode === APPEND_MODE
    if (isAppendMode) {
      var currentText = fileTextAreaNode.innerHTML
      valueToWrite = currentText + valueToWrite
    }
    // Update fileTextArea and the editor content
    fileTextAreaNode.innerHTML = valueToWrite
    fileEditor.session.setValue(valueToWrite)
  }

  function writeToWebConsole(someArgs) {
    // Joins arbitrary number of arguments
    var toLog = []
    for (var i = 0; i < arguments.length; i++) {
      toLog.push(arguments[i])
    }
    var val = OUTPUT_EL.innerHTML
    val += toLog.join(' ') + '\n'
    OUTPUT_EL.innerHTML = val
  }

  function evalInMainThread(code) {
    var newCode = code.split('console.log').join('writeToWebConsole')
    eval(newCode)
  }

  function executeJsCode(prog, tsCode) {
    w = undefined
    OUTPUT_EL.innerHTML = ''
    if (typeof(Worker) !== "undefined") {
      w = new Worker(payload.worker)
      w.postMessage({prog: prog})
      w.onmessage = function(event){
        var val = OUTPUT_EL.innerHTML
        val += event.data + '\n'
        OUTPUT_EL.innerHTML = val
      }
      // Terminate webworker after 5 seconds
      setTimeout(() => {
        if (w !== "undefined") {
          w.terminate()
          w = undefined
        }
      }, 5 * 1000)
    } else {
      evalInMainThread(code)
    }
    if (checkInput(prog) && checkOutput()) {
      prog = tsCode || prog
      createSubmissionAndShowModal(prog, true);
    } else {
      createSubmissionAndShowModal(prog, false);
    }
  }

  function runit() {
    var prog = editor.getValue();
    if (payload.programmingLanguage === 'JavaScript') {
      executeJsCode(prog)
    }
    else if (payload.programmingLanguage === 'Python') {
      executePythonCodeOnBackend(prog)
      // executePythonCode(prog)
    }
    else if (payload.programmingLanguage === 'TypeScript') {
      var transpiled = ts.transpile(prog)
      executeJsCode(transpiled, prog)
    }
    else {
      alert('Кечирип коюңуз, бул тилди колдой элекпиз')
    }
  }

  function executePythonCodeOnBackend(prog) {
    $.ajax({
      url: payload.api_url_root + 'v1/submissions/',
      type: 'POST',
      data: {
        csrfmiddlewaretoken: payload.csrfToken,
        exercise: payload.objectId,
        submitted_code: prog
      }
    })
    .done(function (responseData) {
      outf(responseData?.console_output || '')
      if (responseData?.passed) {
        _toggleSuccessModal(true)
      } else {
        _toggleFailModal(responseData?.error_message || '', true)
      }
    })
  }

  function executePythonCode(prog) {
    var unitTest = document.getElementById('code_checker').value;
    var readyProg = prog + '\n' + unitTest;
    var outputElement = document.getElementById(payload.outputElementId);
    outputElement.innerHTML = '';
    Sk.pre = payload.outputElementId;
    Sk.configure({
      output: outf,
      inBrowser: true,
      read: builtinRead,
      nonreadopen: true,
      filewrite: filewrite,
      killableWhile: true,
      killableFor: true,
      __future__: Sk.python3,
    });
    (Sk.TurtleGraphics || (Sk.TurtleGraphics = {})).target = 'turtle-canvas';
    var evalPromise = Sk.misceval.asyncToPromise(function () {
      return Sk.importMainWithBody("<stdin>", false, readyProg, true);
    });
    evalPromise.then(function (mod) {
      if (checkInput(prog) && checkOutput()) {
        createSubmissionAndShowModal(prog, true);
      } else {
        createSubmissionAndShowModal(prog, false);
      }
    },
    function (err) {
      createSubmissionAndShowModal(prog, false, err.toString());
    });
  }

  function checkInput(codeText) {
    var positiveAssertionWords = payload.inputShouldContain
    var negativeAssertionWords = payload.inputShouldNotContain
    return _checkImpl(positiveAssertionWords, codeText, true) && _checkImpl(negativeAssertionWords, codeText, false)
  }

  function checkOutput() {
    var output = document.getElementById('output').innerHTML.trim();
    var positiveAssertionWords = payload.outputShouldContain
    var negativeAssertionWords = payload.outputShouldNotContain
    negativeAssertionWords.push('exception');
    negativeAssertionWords.push('Fail:');
    return _checkImpl(positiveAssertionWords, output, true) && _checkImpl(negativeAssertionWords, output, false)
  }

  function _checkImpl(assertionWords, textToCheck, positive) {
    var resultsInd = [];
    if (assertionWords.length >= 1 && assertionWords[0].length > 0) {
      for (var i = 0; i < assertionWords.length; i++) {
        resultsInd.push(textToCheck.indexOf(assertionWords[i]))
      }
    } else {
      return true
    }
    return positive ? resultsInd.indexOf(-1) === -1 : resultsInd.indexOf(-1) > -1;
  }

  function createSubmissionAndShowModal(prog, passed, err) {
    err === undefined ? err = '' : err;
    $.ajax({
      url: payload.path,
      type: 'POST',
      data: {
        csrfmiddlewaretoken: payload.csrfToken,
        exercise: payload.objectId,
        submitted_code: prog,
        text_file_content: fileEditor.getValue(),
        passed: passed
      }
    })
    .done(function (responseData) {
      if (responseData.saved) {
        passed ? _toggleSuccessModal(true) : _toggleFailModal(err, true)
      } else {
        responseData.not_logged_in
          ? passed ? _toggleSuccessModal(false) : _toggleFailModal(err, false)
          : $("#serverErrorModal").modal('toggle')
      }
    })
  }

  var notLoggedInMessageContainer = '<p id="notLoggedInMessage">' + payload.notLoggedInMessage + '</p>';
  var notLoggedInMessageElement = $("#notLoggedInMessage");
  var failModalRow = $(".bd-fail-modal-row");

  function _toggleSuccessModal(loggedIn) {
    failModalRow.children('p').remove()
    if(!loggedIn) {
      notLoggedInMessageElement.remove();
      $(".bd-success-modal-row").append(notLoggedInMessageContainer);
    }
    $("#successModal").modal('toggle')
  }

  function _toggleFailModal(err, loggedIn) {
    failModalRow.children('p').remove()
    if(err.length > 0) {
      failModalRow.append('<p id="parseError">' + err + '</p>');
    }
    if(!loggedIn) {
      notLoggedInMessageElement.remove();
      failModalRow.append(notLoggedInMessageContainer)
    }
    $("#failModal").modal('toggle');
  }

})(payload);
