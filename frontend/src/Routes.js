import React from 'react'
import { Switch, Route } from "react-router-dom"

import Cabinet from './Cabinet'
import Signup from './components/auth/signup'
import Login from './components/auth/login'



const Routes = () => {
  return (
    <Switch>
      <Route path="/login" component={Login} />
      <Route path="/signup" component={Signup} />
      <Route path="/" component={Cabinet} />
    </Switch>
  )
}

export default Routes
