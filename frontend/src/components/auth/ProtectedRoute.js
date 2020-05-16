import React from 'react'
import Cookies from 'js-cookie'
import { Route, Redirect } from "react-router-dom"

import axiosInstance from '../../axiosApi'


const ProtectedRoute = ({ component: Component, ...rest }) => {
  axiosInstance.post(
    'token/verify/',
    { token: Cookies.get('access_token') }
  ).then(r => console.log(r))

  return (
    <Route {...rest} render={(props) => (
      // TODO: check if user is authenticated.
      // Use reducer
      true === true
        ? <Component {...props} />
        : <Redirect to={{ pathname: '/cabinet/login', state: { from: props.location }}} />   
    )} />
  )
}

export default ProtectedRoute
