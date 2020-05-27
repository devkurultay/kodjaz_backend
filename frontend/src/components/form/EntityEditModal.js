import React from 'react'

import Modal from 'react-bootstrap/Modal'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Alert from 'react-bootstrap/Alert'

const EntityEditModal = ({
  showModal,
  currentNode,
  handleSave,
  handleClose,
  handleFieldChange,
  isShowAlert
}) => {
  return (
    <Modal show={showModal} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Editing {currentNode?.title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group controlId="formTitle">
            <Form.Label>Title</Form.Label>
            <Form.Control
              type="input"
              value={currentNode?.title}
              onChange={(e) => handleFieldChange(e, 'title')}
            />
          </Form.Group>
          {Object.keys(currentNode).includes('subtitle')
            ? <Form.Group controlId="formDescription">
                <Form.Label>Description</Form.Label>
                <Form.Control
                  type="input"
                  value={currentNode?.subtitle}
                  onChange={(e) => handleFieldChange(e, 'subtitle')}
                />
              </Form.Group>
            : null
          }
          <Form.Group controlId="formIsPublishedCheckbox">
            <Form.Check
              type="checkbox"
              id="is_published"
              checked={currentNode?.is_published}
              onChange={(e) => handleFieldChange(e, 'is_published')}
              label="Is the track published?"
            />
          </Form.Group>
          {isShowAlert && (
            <Alert variant="danger">
              <div>Unpublishing this element may lead to unexpected consequences. Are you sure?</div>
            </Alert>
          )}
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="primary" onClick={handleSave}>
          Save Changes
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

export default EntityEditModal
