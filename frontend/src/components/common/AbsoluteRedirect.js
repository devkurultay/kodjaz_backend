import React, { useEffect } from 'react'

const AbsoluteRedirect = ({ to }) => {
  useEffect(() => {
    window.location = to
  }, [])

  return null
}

export default AbsoluteRedirect
