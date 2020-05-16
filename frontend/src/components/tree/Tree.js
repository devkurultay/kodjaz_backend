import React, { useEffect, useState } from 'react'
import Modal from 'react-bootstrap/Modal'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import SortableTree, { changeNodeAtPath } from 'react-sortable-tree'
import FileExplorerTheme from 'react-sortable-tree-theme-minimal'

import './Tree.scss'

import axiosInstance from '../../axiosApi'
import { dataToTree } from './helpers.js'

const Tree = () => {
  const [ nodes, setNodes ] = useState([])
  const [ showModal, setShowModal ] = useState(false)
  const [ currentPath, setCurrentPath ] = useState([])
  const [ currentNode, setCurrentNode ] = useState({})

  useEffect(() => {
    axiosInstance.get('/v1/tracks/').then(r => {
      setNodes(dataToTree(r.data))
    })
  }, [])

  const handleClose = () => {
    setShowModal(false)
  }

  const handleShow = () => {
    setShowModal(true)
  }

  const getNodeKey = ({ treeIndex }) => treeIndex

  const handleSave = () => {
    const newNodes = changeNodeAtPath({
      treeData: nodes,
      path: currentPath,
      getNodeKey,
      newNode: currentNode
    })
    setNodes(newNodes)
    handleClose()
  }

  const handleEditClick = (node, path) => {
    setCurrentNode(node)
    setCurrentPath(path)
    handleShow()
  }

  const handleTitleChange = (event) => {
    const title = event.target.value
    const newNode = { ...currentNode, title }
    setCurrentNode(newNode)
  }

  return (
    <div className="tree">
      <Modal show={showModal} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Editing {currentNode?.title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="formBasicEmail">
              <Form.Label>Title</Form.Label>
              <Form.Control
                type="input"
                value={currentNode?.title}
                onChange={handleTitleChange}
              />
            </Form.Group>
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
      <SortableTree
        treeData={nodes}
        onChange={setNodes}
        theme={FileExplorerTheme}
        generateNodeProps={({ node, path }) => ({
					buttons: [
						<button onClick={() => handleEditClick(node, path)}>
							Edit
						</button>
					]
        })}
      />
    </div>
  )
}

export default Tree
