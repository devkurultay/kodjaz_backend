import React, { useEffect, useState } from 'react'
import SortableTree, { changeNodeAtPath } from 'react-sortable-tree'
import FileExplorerTheme from 'react-sortable-tree-theme-minimal'

import EntityEditModal from '../form/EntityEditModal'

import './Tree.scss'

import axiosInstance from '../../axiosApi'
import { dataToTree } from './helpers.js'

const Tree = () => {
  const [ nodes, setNodes ] = useState([])
  const [ showModal, setShowModal ] = useState(false)
  const [ currentPath, setCurrentPath ] = useState([])
  const [ currentNode, setCurrentNode ] = useState({})

  const getDataAndSetToState = () => {
    axiosInstance.get('/v1/tracks/').then(r => {
      setNodes(dataToTree(r.data))
    })
  }
  useEffect(() => {
    getDataAndSetToState()
  }, [])

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

  const handleTitleChange = (event) => {
    const title = event.target.value
    const newNode = { ...currentNode, title }
    setCurrentNode(newNode)
  }

  return (
    <div className="tree">
      <EntityEditModal
        showModal={showModal}
        currentNode={currentNode}
        handleSave={handleSave}
        handleClose={handleClose}
        handleTitleChange={handleTitleChange}
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
