import React from 'react'
import Cookies from 'js-cookie'
import { Route, Redirect } from "react-router-dom"

import axiosInstance from '../../axiosApi'


const ProtectedRoute = ({ component: Component, ...rest }) => {
  const { isAuthenticated } = rest
  return (
    <Route {...rest} render={(props) => (
      isAuthenticated
        ? <Component {...props} />
        : <Redirect to={{ pathname: '/login', state: { from: props.location }}} />   
    )} />
  )
}

export default ProtectedRoute
