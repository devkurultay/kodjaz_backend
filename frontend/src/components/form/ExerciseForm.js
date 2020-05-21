import React, { useState, useEffect } from 'react'
import { useParams } from "react-router-dom"
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import AceEditor from "react-ace"

/*
 * Import modes depending on the exercise language
 * languages.forEach(lang => {
 *   require(`ace-builds/src-noconflict/mode-${lang}`)
 * })
 */

import "ace-builds/src-noconflict/mode-python"
import "ace-builds/src-noconflict/theme-github"

const ExerciseForm = ({ currentExercise, loadExercise }) => {
  const { id } = useParams()
  const [ exerciseData, setExerciseData ] = useState({})

  useEffect(() => {
    if (id !== undefined || id !== null) {
      loadExercise(id)
    }
  }, [])

  useEffect(() => {
    setExerciseData(currentExercise)
  }, [ currentExercise ])

  const handleFieldChange = (fieldName, value) => {
    setExerciseData({ ...exerciseData, [fieldName]: value })
  }

  return (
    <React.Fragment>
      <h4>Editing exercise #{ id }</h4>
      <hr />
      <Form>
        <Form.Group controlId="name">
          <Form.Label>Exercise name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Exercise name"
            onChange={(e) => handleFieldChange('name', e.target.value)}
            value={exerciseData?.name} />
        </Form.Group>
        <Form.Group controlId="lecture">
          <Form.Label>Lecture text</Form.Label>
          <Form.Control
            as="textarea"
            rows="3"
            onChange={(e) => handleFieldChange('lecture', e.target.value)}
            value={exerciseData?.lecture} />
        </Form.Group>
        <Form.Group controlId="instruction">
          <Form.Label>Instruction text</Form.Label>
          <Form.Control
            as="textarea"
            rows="3"
            onChange={(e) => handleFieldChange('instruction', e.target.value)}
            value={exerciseData?.instruction} />
        </Form.Group>
        <Form.Group controlId="hint">
          <Form.Label>Hint text</Form.Label>
          <Form.Control
            as="textarea"
            rows="3"
            onChange={(e) => handleFieldChange('hint', e.target.value)}
            value={exerciseData?.hint} />
        </Form.Group>
        <label className="form-label" htmlFor="defaultCode">Default code</label>
        <AceEditor
          mode="python"
          theme="github"
          onChange={(val) => handleFieldChange('default_code', val)}
          name="defaultCode"
          height="250px"
          value={exerciseData?.default_code}
          editorProps={{ $blockScrolling: true }}
        />
        <Form.Group controlId="keywordsShouldBePresented">
          <Form.Label>List of keywords which should be presented in the submitted code</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: def,print,Hello world!"
            onChange={(e) => handleFieldChange('input_should_contain', e.target.value)}
            value={exerciseData?.input_should_contain}
          />
        </Form.Group>
        <Form.Group controlId="keywordsShouldNotBePresented">
          <Form.Label>List of keywords which should NOT be presented in the submitted code</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: class,return,Hi world!"
            onChange={(e) => handleFieldChange('input_should_not_contain', e.target.value)}
            value={exerciseData?.input_should_not_contain}
            />
        </Form.Group>
        <Form.Group controlId="errorTextExpectedInputNotFound">
          <Form.Label>Error text shown when expected input was not found in the written code</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: Oops, did you forget to use print() statement?"
            onChange={(e) => handleFieldChange('input_error_text', e.target.value)}
            value={exerciseData?.input_error_text}
          />
        </Form.Group>
        <Form.Group controlId="keywordsShouldBeInOutput">
          <Form.Label>List of keywords which should be presented in the output</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: Hello world!"
            onChange={(e) => handleFieldChange('output_should_contain', e.target.value)}
            value={exerciseData?.output_should_contain}
          />
        </Form.Group>
        <Form.Group controlId="keywordsShouldNotBeInOutput">
          <Form.Label>List of keywords which should NOT be presented in the output</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: Bye, world!"
            onChange={(e) => handleFieldChange('output_should_not_contain', e.target.value)}
            value={exerciseData?.output_should_not_contain}
          />
        </Form.Group>
        <Form.Group controlId="errorTextExpectedOutputNotShown">
          <Form.Label>Error text shown when expected output doesn't show up</Form.Label>
          <Form.Control
            type="text"
            placeholder="Example: Oops, did you forget to print() Hello world!?"
            onChange={(e) => handleFieldChange('output_error_text', e.target.value)}
            value={exerciseData?.output_error_text}
          />
        </Form.Group>
        <label className="form-label" htmlFor="unitTestCode">Unit test code</label>
        <AceEditor
          mode="python"
          theme="github"
          name="unitTestCode"
          height="250px"
          onChange={(val) => handleFieldChange('unit_test', val)}
          value={exerciseData?.unit_test}
          editorProps={{ $blockScrolling: true }}
        />
        <Form.Group controlId="prevExercise">
          <Form.Label>Select previous exercise</Form.Label>
          <Form.Control type="text" />
        </Form.Group>
        <Form.Group controlId="isPublishedCheckbox">
          <Form.Check
            type="checkbox"
            id="is_published"
            checked={exerciseData?.is_published}
            onChange={(e) => handleFieldChange('is_published', e.target.checked)}
            label="Is the exercise published?"
          />
        </Form.Group>
        <Form.Group controlId="belongsToLesson">
          <Form.Label>Lesson the exercise belongs to</Form.Label>
          <Form.Control type="text" />
        </Form.Group>
        <Form.Group controlId="fileTxt">
          <Form.Label>If this field has a content, file.txt tab will be shown</Form.Label>
          <Form.Control
            as="textarea"
            rows="3"
            onChange={(e) => handleFieldChange('text_file_content', e.target.value)}
            value={exerciseData?.text_file_content} />
        </Form.Group>
      </Form>
      <Button variant="primary">
        Save Changes
      </Button>
    </React.Fragment>
  )
}

export default ExerciseForm
