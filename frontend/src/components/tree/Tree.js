import React, { useEffect, useState } from 'react'
import SortableTree, { changeNodeAtPath } from 'react-sortable-tree'
import FileExplorerTheme from 'react-sortable-tree-theme-minimal'

import EntityEditModal from '../form/EntityEditModal'

import './Tree.scss'

import axiosInstance from '../../axiosApi'
import { dataToTree } from './helpers.js'

const Tree = ({ tracks, loadTracks }) => {
  const [ nodes, setNodes ] = useState([])
  const [ showModal, setShowModal ] = useState(false)
  const [ currentPath, setCurrentPath ] = useState([])
  const [ currentNode, setCurrentNode ] = useState({})

  useEffect(() => {
    loadTracks()
  }, [])

  useEffect(() => {
    setNodes(dataToTree(tracks))
  }, [tracks])

  const handleClose = () => {
    setShowModal(false)
  }

  const handleShow = () => {
    setShowModal(true)
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
      axiosInstance.put(`/v1/tracks/${id}/`, payload).then(() => getDataAndSetToState())
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

  const handleEditClick = (node, path) => {
    setCurrentNode(node)
    setCurrentPath(path)
    handleShow()
  }

  const handleFieldChange = (event, fieldName) => {
    let value = event.target.value
    if (fieldName === 'is_published') {
      value = event.target.checked
    }
    const newNode = { ...currentNode, [fieldName]: value }
    setCurrentNode(newNode)
  }

  return (
    <div className="tree">
      <EntityEditModal
        showModal={showModal}
        currentNode={currentNode}
        handleSave={handleSave}
        handleClose={handleClose}
        handleFieldChange={handleFieldChange}
      />
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
