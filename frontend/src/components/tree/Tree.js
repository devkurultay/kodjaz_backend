import React, { useEffect, useState } from 'react'
import SortableTree from 'react-sortable-tree'

import './Tree.scss'

import axiosInstance from '../../axiosApi'
import { dataToTree } from './helpers.js'

const Tree = () => {
  const [ nodes, setNodes ] = useState([])

  useEffect(() => {
    axiosInstance.get('/v1/tracks/').then(r => {
      setNodes(dataToTree(r.data))
    })
  }, [])

  return (
    <div className="tree">
      <SortableTree
        treeData={nodes}
        onChange={console.log}
      />
    </div>
  )
}

export default Tree
