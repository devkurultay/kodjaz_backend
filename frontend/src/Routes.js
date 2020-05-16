import React from 'react'
import { Switch, Route } from "react-router-dom"

import Cabinet from './Cabinet'
import Signup from './components/auth/signup'
import Login from './components/auth/login'
import ProtectedRoute from './components/auth/ProtectedRoute'


const Routes = () => {
  return (
    <Switch>
      <Route path="/login" component={Login} />
      <Route path="/signup" component={Signup} />
      <ProtectedRoute path="/" component={Cabinet} />
    </Switch>
  )
}

export default Routes
