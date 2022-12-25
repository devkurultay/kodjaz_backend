import React, { useEffect, useState } from 'react'
import SortableTree, { changeNodeAtPath, addNodeUnderParent } from 'react-sortable-tree'
import FileExplorerTheme from 'react-sortable-tree-theme-minimal'
import Button from 'react-bootstrap/Button'
import ButtonGroup from 'react-bootstrap/ButtonGroup'
import Container from 'react-bootstrap/Container'
import Form from 'react-bootstrap/Form'
import InputGroup from 'react-bootstrap/InputGroup'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import { useHistory } from 'react-router-dom'

import EntityEditModal from '../form/EntityEditModal'

import './Tree.scss'

import { dataToTree } from './helpers.js'

const Tree = ({
  tracks,
  saveTrack,
  saveUnit,
  saveLesson,
  createTrack,
  createUnit,
  createLesson,
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
  const [ searchString, setSearchString ] = useState('')
  const [ searchFocusIndex, setSearchFocusIndex ] = useState(0)
  const [ searchFoundCount, setSearchFoundCount ] = useState(null)

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
  const customSearchMethod = ({ node, searchQuery }) =>
    searchQuery &&
    node.title.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1;

  const selectPrevMatch = () => {
    const value = searchFocusIndex !== null
      ? (searchFoundCount + searchFocusIndex - 1) % searchFoundCount
      : searchFoundCount - 1
    setSearchFocusIndex(value)
  }

  const selectNextMatch = () => {
    const value = searchFocusIndex !== null
      ? (searchFocusIndex + 1) % searchFoundCount
      : 0
    setSearchFocusIndex(value)
  }

  const handleSearchFinish = (matches) => {
    const focusIndex = matches.length > 0
      ? searchFocusIndex % matches.length
      : 0
    setSearchFoundCount(matches.length)
    setSearchFocusIndex(focusIndex)
  }

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
        return
      }
      // Redirect to exercise creation page (with lessonId in history state)
      history.push(`/create-exercise/`, { lessonId: node.lesson })
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
      <Form.Row className="d-flex justify-content-center align-items-center mb-2">
        <Col xs="auto">
          <InputGroup>
            <Form.Control
              type="text"
              placeholder="Search for nodes"
              value={searchString}
              onChange={(e) => setSearchString(e.target.value)}
            />
            <InputGroup.Append>
              <InputGroup.Text
                id="searchTextClear"
                onClick={(e) => {
                  setSearchString('')
                  handleSearchFinish([])
                }}
              >
                <i className="fa fa-fw fa-times" />
              </InputGroup.Text>
            </InputGroup.Append>
          </InputGroup>
        </Col>
        <Col xs="auto">
          <ButtonGroup>
            <Button
              onClick={selectPrevMatch}
              variant="outline-success">Prev</Button>
            <Button
              onClick={selectNextMatch}
              variant="outline-success">Next</Button>
          </ButtonGroup>
        </Col>
        <Col xs="auto">
          <span>
            &nbsp;
            {searchFoundCount > 0 ? searchFocusIndex + 1 : 0}
            &nbsp;/&nbsp;
            {searchFoundCount || 0}
          </span>
        </Col>
      </Form.Row>
      <SortableTree
        isVirtualized={false}
        treeData={nodes}
        onChange={setNodes}
        theme={FileExplorerTheme}
        generateNodeProps={({ node, path }) => ({
					buttons: getButtons(node, path)
        })}
        searchMethod={customSearchMethod}
        searchQuery={searchString}
        searchFocusOffset={searchFocusIndex}
        searchFinishCallback={handleSearchFinish}
      />
    </Container>
  )
}

export default Tree
