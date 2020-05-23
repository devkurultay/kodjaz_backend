import React from 'react'
import { Switch, Route } from "react-router-dom"

import Cabinet from './components/home/CabinetContainer'
import Signup from './components/auth/Signup'
import Login from './components/auth/Login'
import ProtectedRoute from './components/auth/ProtectedRoute'

const Routes = ({isAuthenticated, checkIsAuth}) => {
  return (
    <Switch>
      <Route path="/login" component={Login} />
      <Route path="/signup" component={Signup} />
      <ProtectedRoute path="/" component={Cabinet} />
    </Switch>
  )
}

export default Routes
