import React from 'react'
import Alert from 'react-bootstrap/Alert'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'

const WarningModal = ({
  showModal,
  warningTitle,
  warningText,
  closeHandler,
  proceedHandler
}) => {
  return (
    <Modal show={showModal} onHide={closeHandler}>
      <Modal.Header closeButton>
        <Modal.Title>{warningTitle}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Alert variant="danger">{warningText}</Alert>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={closeHandler}>
          Close
        </Button>
        <Button variant="primary" onClick={proceedHandler}>
          Proceed
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

export default WarningModal
