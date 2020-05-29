import React, { useEffect, useState } from 'react'
import SortableTree, { changeNodeAtPath, addNodeUnderParent } from 'react-sortable-tree'
import FileExplorerTheme from 'react-sortable-tree-theme-minimal'
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import { useHistory } from 'react-router-dom'

import EntityEditModal from '../form/EntityEditModal'

import './Tree.scss'

import axiosInstance from '../../axiosApi'
import { dataToTree } from './helpers.js'

const Tree = ({
  tracks,
  saveTrack,
  saveUnit,
  saveLesson,
  createTrack,
  createUnit,
  createLesson,
  isSaveTrackPending,
  entityToPick = '',
  entityId = '',
  pickHandler = () => {}
}) => {
  const history = useHistory()
  const [ nodes, setNodes ] = useState([])
  const [ showModal, setShowModal ] = useState(false)
  const [ currentPath, setCurrentPath ] = useState([])
  const [ currentNode, setCurrentNode ] = useState({})
  const [ isShowAlert, setIsShowAlert ] = useState(false)

  useEffect(() => {
    setNodes(dataToTree(tracks))
  }, [tracks])

  const handleClose = () => {
    setShowModal(false)
    setIsShowAlert(false)
  }

  const handleShow = () => {
    setShowModal(true)
    setIsShowAlert(false)
  }

  const getNodeKey = ({ treeIndex }) => treeIndex

  const handleSave = () => {
    const { type, id } = currentNode
    if (type && type === 'Track') {
      const payload = {
        name: currentNode.title,
        description: currentNode.subtitle,
        is_published: currentNode.is_published,
        programming_language: currentNode.programming_language
      }
      if (id) {
        saveTrack(id, payload)
      } else {
        createTrack(payload)
      }
    } else if (type && type === 'Unit') {
      const payload = {
        name: currentNode.title,
        description: currentNode.subtitle,
        is_published: currentNode.is_published,
        track: currentNode.track,
      }
      if (id) {
        saveUnit(id, payload)
      } else {
        createUnit(payload)
      }
    } else if (type && type === 'Lesson') {
      const payload = {
        name: currentNode.title,
        is_published: currentNode.is_published,
        unit: currentNode.unit,
      }
      if (id) {
        saveLesson(id, payload)
      } else {
        createLesson(payload)
      }
    }
    const newNodes = changeNodeAtPath({
      treeData: nodes,
      path: currentPath,
      getNodeKey,
      newNode: currentNode
    })
    setNodes(newNodes)
    handleClose()
  }

  const createNewNode = (node) => {
    const nodesWithSubtitle = ['Track', 'Unit']
    const newNode = {
      type: node.childrenType,
      title: `New ${node.childrenType}`,
      is_published: false,
    }
    if (nodesWithSubtitle.includes(node.childrenType)) {
      newNode['subtitle'] = ''
    }
    if (node.childrenType === 'Track') {
      newNode['programming_language'] = node.programming_language
    }
    if (node?.id && node?.type) {
      const parentFieldName = node.type.toLowerCase()
      newNode[parentFieldName] = node.id
    }
    return newNode
  }

  const handleAddNewTrack = () => {
    const newNodes = addNodeUnderParent({
      treeData: nodes,
      parentKey: null,
      expandParent: false,
      getNodeKey,
      newNode: createNewNode({
        childrenType: 'Track',
        programming_language: ''
      }),
      addAsFirstChild: true
    }).treeData
    setNodes(newNodes)
  }

  const handleAddClick = (node, path) => {
    const newNodes = addNodeUnderParent({
      treeData: nodes,
      parentKey: path[path.length - 1],
      expandParent: true,
      getNodeKey,
      newNode: createNewNode(node),
      addAsFirstChild: true
    }).treeData
    setNodes(newNodes)
  }

  const handleEditClick = (node, path) => {
    const { type, id } = node
    if (type && type === 'Exercise') {
      if (id) {
        history.push(`/exercise/${id}/`)
      } else {
        // Redirect to exercise creation page (with lessonId in history state)
        history.push('/create-exercise/', { lessonId: node.lesson })
      }
      return
    }
    setCurrentNode(node)
    setCurrentPath(path)
    handleShow()
  }

  const handleFieldChange = (event, fieldName) => {
    let value = event.target.value
    if (fieldName === 'is_published') {
      value = event.target.checked
      if (value === false) {
        setIsShowAlert(true)
      } else {
        setIsShowAlert(false)
      }
    }
    const newNode = { ...currentNode, [fieldName]: value }
    setCurrentNode(newNode)
  }

  const getPickBtn = (node) => {
    return node.type === entityToPick && node.id !== Number(entityId)
      ? [
          <button onClick={() => pickHandler(node)}>
            Pick
          </button>
        ]
      : []
  }

  const getEditBtn = (node, path) => {
    const btns = [
      <Button variant="light" onClick={() => handleEditClick(node, path)}>
        {node?.id ? 'Edit' : 'Edit and create'}
      </Button>
    ]
    if (node.childrenType) {
      btns.push(
        <Button variant="light" onClick={() => handleAddClick(node, path)}>
          Add {node.childrenType}
        </Button>
      )
    }
    return btns
  }

  const getButtons = (node, path) => {
    return entityToPick
      ? getPickBtn(node)
      : getEditBtn(node, path)
  }

  return (
    <Container className="tree">
      <EntityEditModal
        showModal={showModal}
        currentNode={currentNode}
        handleSave={handleSave}
        handleClose={handleClose}
        handleFieldChange={handleFieldChange}
        isShowAlert={isShowAlert}
      />
      <Row className="justify-content-md-center">
        {entityToPick
          ? null
          : <Button
              className="tree__add-track-btn"
              onClick={handleAddNewTrack}
              variant="outline-primary">
              Add a new track
            </Button>
        }
      </Row>
      <SortableTree
        treeData={nodes}
        onChange={setNodes}
        theme={FileExplorerTheme}
        generateNodeProps={({ node, path }) => ({
					buttons: getButtons(node, path)
        })}
      />
    </Container>
  )
}

export default Tree
