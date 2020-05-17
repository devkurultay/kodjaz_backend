import React from 'react'
import { connect } from 'react-redux'
import { Switch, Route } from "react-router-dom"

import Cabinet from './Cabinet'
import Signup from './components/auth/signup'
import Login from './components/auth/login'
import ProtectedRoute from './components/auth/ProtectedRoute'


const Routes = ({isAuthenticated}) => {
  return (
    <Switch>
      <Route path="/login" component={Login} />
      <Route path="/signup" component={Signup} />
      <ProtectedRoute path="/" component={Cabinet} isAuthenticated={isAuthenticated} />
    </Switch>
  )
}

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.isAuthenticated
  }
}

export default connect(
  mapStateToProps
)(Routes)
