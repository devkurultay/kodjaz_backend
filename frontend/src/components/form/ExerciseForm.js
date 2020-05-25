import React, { useState, useEffect } from 'react'
import { useParams } from "react-router-dom"
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import Alert from 'react-bootstrap/Alert'
import InputGroup from 'react-bootstrap/InputGroup'
import AceEditor from "react-ace"

import Tree from '../tree/TreeContainer'
import WarningModal from './WarningModal'

/*
 * Import modes depending on the exercise language
 * languages.forEach(lang => {
 *   require(`ace-builds/src-noconflict/mode-${lang}`)
 * })
 */

import "ace-builds/src-noconflict/mode-python"
import "ace-builds/src-noconflict/theme-github"

const ExerciseForm = ({
  tracks,
  lessons,
  exercises,
  isSaveExercisePending,
  saveExerciseError,
  loadExercises,
  loadLessons,
  saveExercise
}) => {
  const { id } = useParams()
  const [ exerciseData, setExerciseData ] = useState({})
  const [ prevExercise, setPrevExercise ] = useState({})
  const [ nextExercise, setNextExercise ] = useState({})
  const [ exerciseToPick, setExerciseToPick ] = useState('')
  const [ lesson, setLesson ] = useState({})
  const [ newLesson, setNewLesson ] = useState({})
  const [ showModal, setShowModal ] = useState(false)
  const [ showWarningModal, setShowWarningModal ] = useState(false)
  const [ entityToPick, setEntityToPick ] = useState('')
  const [ entityToClear, setEntityToClear ] = useState('')

  useEffect(() => {
    loadExercises()
    loadLessons()
  }, [])

  const setLessonById = (id, cb) => {
    const currentLesson = lessons.filter(l => l.id === id)
    if (currentLesson) {
      cb(currentLesson?.[0])
    }
  }

  const getExerciseDataById = (idOfExerciseToFind) => {
    return exercises.filter(exercise => Number(exercise.id) === Number(idOfExerciseToFind))?.[0]
  }

  useEffect(() => {
    if (exercises.length) {
      const currentExercise = getExerciseDataById(id)
      const prev = getExerciseDataById(currentExercise?.previous_exercise)
      const next = getExerciseDataById(currentExercise?.next_exercise)
      setExerciseData(currentExercise)
      setPrevExercise(prev)
      setNextExercise(next)
      setLessonById(currentExercise?.lesson, setLesson)
    }
  }, [ exercises, lessons ])

  const handleFieldChange = (fieldName, value) => {
    setExerciseData({ ...exerciseData, [fieldName]: value })
  }

  const handleLessonPick = (node) => {
    setLessonById(node.id, setNewLesson)
  }

  const handleLessonProceed = () => {
    setLessonById(newLesson.id, setLesson)
    setNewLesson({})
    setExerciseData({
      ...exerciseData,
      lesson: newLesson.id,
      previous_exercise: '',
      next_exercise: ''
    })
    setPrevExercise({})
    setNextExercise({})
    handleModalClose()
  }

  const handleExercisePick = (node) => {
    const exerciseId = node.id
    const exercise = getExerciseDataById(exerciseId)
    if (exerciseToPick === 'previous_exercise') {
      setPrevExercise(exercise)
    } else if (exerciseToPick === 'next_exercise') {
      setNextExercise(exercise)
    }
    setExerciseData({ ...exerciseData, [exerciseToPick]: node.id })
    handleModalClose()
  }

  const handleSave = () => {
    saveExercise(id, exerciseData)
  }

  const handleModalShow = () => {
    setShowModal(true)
  }

  const handleModalClose = () => {
    setShowModal(false)
    setEntityToPick('')
    setExerciseToPick('')
  }

  const handleWarningModalShow = (fieldName) => {
    setEntityToClear(fieldName)
    setShowWarningModal(true)
  }

  const handleWarningModalClose = () => {
    setEntityToClear('')
    setShowWarningModal(false)
  }

  const handleEntityPick = (e, entityType, exerciseType = '') => {
    if (exerciseType.length) {
      setExerciseToPick(exerciseType)
    }
    setEntityToPick(entityType)
    handleModalShow()
    e?.target?.blur()
  }

  const entityPickers = {
    Lesson: handleLessonPick,
    Exercise: handleExercisePick
  }
  
  const entityIds = {
    Lesson: exerciseData.lesson,
    Exercise: exerciseData?.id
  }

  const handleFieldClear = (field) => {
    setExerciseData({
      ...exerciseData,
      [field]: ''
    })
    setEntityToClear('')
    setShowWarningModal(false)
    switch (field) {
      case 'lesson':
        setLesson({})
      case 'previous_exercise':
        setPrevExercise({})
      case 'next_exercise':
        setNextExercise({})
      default:
        return
    }
  }

  return (
    <React.Fragment>
      <Modal show={showModal} onHide={handleModalClose}>
        <Modal.Header closeButton>
          <Modal.Title>Picking another value for "{entityToPick}"</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Tree
            entityToPick={entityToPick}
            entityId={entityIds[entityToPick]}
            pickHandler={entityPickers[entityToPick]}
          />
        </Modal.Body>
        <Modal.Footer>
          {Object.keys(newLesson).length
            ? <Alert variant="danger">
                <div>If you choose a new lesson, previous and next exercise values will be lost. If you want to proceed, click "Proceed" button</div>
                <Button onClick={handleLessonProceed}>Proceed</Button>
              </Alert>
            : null
          }
          <Button variant="secondary" onClick={handleModalClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>

      <WarningModal
        showModal={showWarningModal}
        warningTitle="You are about to clear the field value"
        warningText="If you want to CLEAR the field, click Proceed. Otherwise, just close the modal."
        closeHandler={handleWarningModalClose}
        proceedHandler={() => handleFieldClear(entityToClear)}
      />

      <h4>Editing exercise #{ id }</h4>
      <hr />
      <Form>
        <Form.Group controlId="name">
          <Form.Label>Exercise name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Exercise name"
            onChange={(e) => handleFieldChange('name', e.target.value)}
            value={exerciseData?.name || ''} />
        </Form.Group>
        <Form.Group controlId="lecture">
          <Form.Label>Lecture text</Form.Label>
          <Form.Control
            as="textarea"
            rows="3"
            onChange={(e) => handleFieldChange('lecture', e.target.value)}
            value={exerciseData?.lecture || ''} />
        </Form.Group>
        <Form.Group controlId="instruction">
          <Form.Label>Instruction text</Form.Label>
          <Form.Control
            as="textarea"
            rows="3"
            onChange={(e) => handleFieldChange('instruction', e.target.value)}
            value={exerciseData?.instruction || ''} />
        </Form.Group>
        <Form.Group controlId="hint">
          <Form.Label>Hint text</Form.Label>
          <Form.Control
            as="textarea"
            rows="3"
            onChange={(e) => handleFieldChange('hint', e.target.value)}
            value={exerciseData?.hint || ''} />
        </Form.Group>
        <label className="form-label" htmlFor="defaultCode">Default code</label>
        <AceEditor
          mode="python"
          theme="github"
          onChange={(val) => handleFieldChange('default_code', val)}
          name="defaultCode"
          height="250px"
          value={exerciseData?.default_code || ''}
          editorProps={{ $blockScrolling: true }}
        />
        <Form.Group controlId="keywordsShouldBePresented">
          <Form.Label>List of keywords which should be presented in the submitted code</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: def,print,Hello world!"
            onChange={(e) => handleFieldChange('input_should_contain', e.target.value)}
            value={exerciseData?.input_should_contain || ''}
          />
        </Form.Group>
        <Form.Group controlId="keywordsShouldNotBePresented">
          <Form.Label>List of keywords which should NOT be presented in the submitted code</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: class,return,Hi world!"
            onChange={(e) => handleFieldChange('input_should_not_contain', e.target.value)}
            value={exerciseData?.input_should_not_contain || ''}
            />
        </Form.Group>
        <Form.Group controlId="errorTextExpectedInputNotFound">
          <Form.Label>Error text shown when expected input was not found in the written code</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: Oops, did you forget to use print() statement?"
            onChange={(e) => handleFieldChange('input_error_text', e.target.value)}
            value={exerciseData?.input_error_text || ''}
          />
        </Form.Group>
        <Form.Group controlId="keywordsShouldBeInOutput">
          <Form.Label>List of keywords which should be presented in the output</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: Hello world!"
            onChange={(e) => handleFieldChange('output_should_contain', e.target.value)}
            value={exerciseData?.output_should_contain || ''}
          />
        </Form.Group>
        <Form.Group controlId="keywordsShouldNotBeInOutput">
          <Form.Label>List of keywords which should NOT be presented in the output</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: Bye, world!"
            onChange={(e) => handleFieldChange('output_should_not_contain', e.target.value)}
            value={exerciseData?.output_should_not_contain || ''}
          />
        </Form.Group>
        <Form.Group controlId="errorTextExpectedOutputNotShown">
          <Form.Label>Error text shown when expected output doesn't show up</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: Oops, did you forget to print() Hello world!?"
            onChange={(e) => handleFieldChange('output_error_text', e.target.value)}
            value={exerciseData?.output_error_text || ''}
          />
        </Form.Group>
        <label className="form-label" htmlFor="unitTestCode">Unit test code</label>
        <AceEditor
          mode="python"
          theme="github"
          name="unitTestCode"
          height="250px"
          onChange={(val) => handleFieldChange('unit_test', val)}
          value={exerciseData?.unit_test || ''}
          editorProps={{ $blockScrolling: true }}
        />
        <Form.Group controlId="prevExercise">
          <Form.Label>Select previous exercise</Form.Label>
          <InputGroup>
            <InputGroup.Prepend>
              <InputGroup.Text
                id="previous_exercise"
                onClick={(e) => handleEntityPick(e, 'Exercise', 'previous_exercise')}
              >
                <i className="fa fa-fw fa-search" />
              </InputGroup.Text>
            </InputGroup.Prepend>
            <InputGroup.Prepend>
              <InputGroup.Text
                id="previous_exercise2"
                onClick={() => handleWarningModalShow('previous_exercise')}
              >
                <i className="fa fa-fw fa-times" />
              </InputGroup.Text>
            </InputGroup.Prepend>
            <Form.Control
              type="text"
              readOnly
              aria-describedby="lessonIcon"
              onFocus={(e) => handleEntityPick(e, 'Exercise', 'previous_exercise')}
              value={prevExercise?.name || ''} />
          </InputGroup>
        </Form.Group>
        <Form.Group controlId="nextExercise">
          <Form.Label>Select next exercise</Form.Label>
          <InputGroup>
            <InputGroup.Prepend>
              <InputGroup.Text
                id="next_exercise"
                onClick={(e) => handleEntityPick(e, 'Exercise', 'next_exercise')}
              >
                <i className="fa fa-fw fa-search" />
              </InputGroup.Text>
            </InputGroup.Prepend>
            <InputGroup.Prepend>
              <InputGroup.Text
                id="next_exercise2"
                onClick={() => handleWarningModalShow('next_exercise')}
              >
                <i className="fa fa-fw fa-times" />
              </InputGroup.Text>
            </InputGroup.Prepend>
            <Form.Control
              type="text"
              readOnly
              onFocus={(e) => handleEntityPick(e, 'Exercise', 'next_exercise')}
              value={nextExercise?.name || ''} />
          </InputGroup>
        </Form.Group>
        <Form.Group controlId="isPublishedCheckbox">
          <Form.Check
            type="checkbox"
            id="is_published"
            checked={!!exerciseData?.is_published}
            onChange={(e) => handleFieldChange('is_published', e.target.checked)}
            label="Is the exercise published?"
          />
        </Form.Group>
        <Form.Group controlId="belongsToLesson">
          <Form.Label>Lesson the exercise belongs to</Form.Label>
          <Form.Control
            type="text"
            readOnly
            onFocus={(e) => handleEntityPick(e, 'Lesson')}
            value={lesson?.name || ''} />
        </Form.Group>
        <Form.Group controlId="fileTxt">
          <Form.Label>If this field has a content, file.txt tab will be shown</Form.Label>
          <Form.Control
            as="textarea"
            rows="3"
            onChange={(e) => handleFieldChange('text_file_content', e.target.value)}
            value={exerciseData?.text_file_content || ''} />
        </Form.Group>
      </Form>
      {saveExerciseError.length
        ? saveExerciseError.map((msg, idx) => <Alert key={idx} variant="danger">{msg}</Alert>)
        : null
      }
      <Button
        disabled={isSaveExercisePending}
        variant="primary"
        onClick={handleSave}
        className="mb-5"
      >
        {isSaveExercisePending ? 'Saving…' : 'Save changes'}
      </Button>
    </React.Fragment>
  )
}

export default ExerciseForm
